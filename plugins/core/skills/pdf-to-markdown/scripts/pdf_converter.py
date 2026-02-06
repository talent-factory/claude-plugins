#!/usr/bin/env python3
"""
PDF to Markdown Converter
=========================
Dual-mode converter supporting both fast text extraction and vision-based analysis.

Modes:
    fast    - PyMuPDF-based text extraction (default, very fast)
    vision  - Prepare images for Claude Code analysis OR use direct API

Usage:
    python pdf_converter.py input.pdf [output.md] [--mode fast|vision] [options]

Requirements:
    Fast mode:   pip install PyMuPDF Pillow
    Vision mode: pip install pdf2image Pillow
                 + poppler (brew install poppler / apt install poppler-utils)
    Direct API:  pip install anthropic (additional, for --use-api)
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# ============================================================================
# FAST MODE (PyMuPDF)
# ============================================================================


def fix_latex_umlauts(text: str) -> str:
    """Fix LaTeX-style umlauts and convert ß to ss (Swiss German)."""
    replacements = {
        "¨a": "ä",
        "¨o": "ö",
        "¨u": "ü",
        "¨A": "Ä",
        "¨O": "Ö",
        "¨U": "Ü",
        "¨ a": "ä",
        "¨ o": "ö",
        "¨ u": "ü",
        "¨ A": "Ä",
        "¨ O": "Ö",
        "¨ U": "Ü",
        "ß": "ss",
        "``": '"',
        "''": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def convert_fast(
    pdf_path: Path,
    output_path: Path,
    extract_images: bool = True,
) -> tuple[str, Optional[str]]:
    """
    Convert PDF using PyMuPDF (fast mode).

    Returns:
        tuple: (markdown_path, images_dir) or raises exception
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Error: PyMuPDF not installed. Run: pip install PyMuPDF")
        sys.exit(1)

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = pdf_path.stem
    images_dir = output_dir / f"{base_name}_images"

    print(f"📄 Converting (fast mode): {pdf_path.name}")

    doc = fitz.open(str(pdf_path))
    markdown_lines = [f"# {base_name}\n\n"]
    image_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        markdown_lines.append(f"## Page {page_num + 1}\n\n")

        # Extract text
        text = page.get_text("text")
        if text.strip():
            text = fix_latex_umlauts(text)
            markdown_lines.append(text)
            markdown_lines.append("\n\n")

        # Extract images
        if extract_images:
            image_list = page.get_images()
            if image_list:
                images_dir.mkdir(parents=True, exist_ok=True)

                for img in image_list:
                    xref = img[0]
                    image_count += 1

                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    image_filename = f"image_{image_count:03d}.png"
                    image_path = images_dir / image_filename

                    if image_ext != "png":
                        try:
                            from PIL import Image
                            import io
                            img_pil = Image.open(io.BytesIO(image_bytes))
                            img_pil.save(str(image_path), "PNG")
                        except ImportError:
                            image_filename = f"image_{image_count:03d}.{image_ext}"
                            image_path = images_dir / image_filename
                            with open(image_path, "wb") as f:
                                f.write(image_bytes)
                    else:
                        with open(image_path, "wb") as f:
                            f.write(image_bytes)

                    relative_path = f"{base_name}_images/{image_filename}"
                    markdown_lines.append(f"![Image {image_count}]({relative_path})\n\n")

    doc.close()

    # Write output
    output_path.write_text("".join(markdown_lines), encoding="utf-8")

    print(f"✅ Created: {output_path}")
    if image_count > 0:
        print(f"✅ Extracted {image_count} images to: {images_dir}")
        return str(output_path), str(images_dir)

    return str(output_path), None


# ============================================================================
# VISION MODE - PDF to Images (for Claude Code analysis)
# ============================================================================


def convert_vision_prepare(
    pdf_path: Path,
    output_dir: Path,
    dpi: int = 150,
    page_range: Optional[tuple[int, int]] = None,
) -> list[str]:
    """
    Convert PDF pages to images for Claude Code to analyze.

    Returns:
        list: Paths to generated images
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image not installed. Run: pip install pdf2image")
        print("Also install poppler: brew install poppler (macOS)")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = pdf_path.stem
    images_dir = output_dir / f"{base_name}_pages"
    images_dir.mkdir(parents=True, exist_ok=True)

    print(f"📄 Converting PDF to images: {pdf_path.name}")
    print(f"   DPI: {dpi}")

    # Convert PDF to images
    images = convert_from_path(str(pdf_path), dpi=dpi)
    total_pages = len(images)
    print(f"   Found {total_pages} pages")

    # Handle page range
    start_page = 1
    end_page = total_pages
    if page_range:
        start_page = max(1, page_range[0])
        end_page = min(total_pages, page_range[1])

    print(f"   Processing pages {start_page}-{end_page}")

    image_paths = []
    for i, image in enumerate(images[start_page - 1:end_page], start=start_page):
        image_path = images_dir / f"page_{i:03d}.png"
        image.save(str(image_path), "PNG")
        image_paths.append(str(image_path))
        print(f"   ✓ Page {i}")

    print(f"\n✅ Created {len(image_paths)} page images in: {images_dir}")
    return image_paths


# ============================================================================
# VISION MODE - Direct API (optional, requires ANTHROPIC_API_KEY)
# ============================================================================

DEFAULT_VISION_PROMPT = """Analysiere diese Buchseite und konvertiere den gesamten Inhalt in gut strukturiertes Markdown.

Beachte folgende Regeln:
1. **Struktur bewahren**: Überschriften, Absätze, Listen korrekt formatieren
2. **Code-Blöcke**: Alle Code-Snippets in ```java oder ```python etc. einschliessen
3. **Tabellen**: Als Markdown-Tabellen formatieren
4. **Sidebars/Hinweisboxen**: Als Blockquotes (>) oder mit passenden Überschriften markieren
5. **Bilder/Illustrationen**: Kurz beschreiben als [Bild: Beschreibung]
6. **Handschriftliche Notizen**: Falls vorhanden, als *kursiv* oder in separatem Block
7. **Multi-Spalten**: Logisch zusammenführen, Lesefluss beachten
8. **Fussnoten/Seitenzahlen**: Ignorieren, ausser sie sind inhaltlich relevant

Gib NUR das Markdown aus, ohne zusätzliche Erklärungen oder Einleitungen."""


def convert_vision_api(
    pdf_path: Path,
    output_path: Path,
    model: str = "claude-sonnet-4-20250514",
    dpi: int = 200,
    page_range: Optional[tuple[int, int]] = None,
    prompt: str = DEFAULT_VISION_PROMPT,
    api_key: Optional[str] = None,
) -> str:
    """
    Convert PDF using Claude Vision API directly (requires API key).

    Returns:
        str: Path to markdown file
    """
    try:
        import anthropic
        from pdf2image import convert_from_path
        from PIL import Image
        from tqdm import tqdm
    except ImportError as e:
        print(f"Error: Missing dependency: {e}")
        print("Install with: pip install anthropic pdf2image Pillow tqdm")
        sys.exit(1)

    import base64
    import io
    import time

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📄 Converting (direct API mode): {pdf_path.name}")
    print(f"   Model: {model}, DPI: {dpi}")

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)
    max_image_size = 1568

    def image_to_base64(image: Image.Image) -> tuple[str, str]:
        if max(image.size) > max_image_size:
            ratio = max_image_size / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        return base64.standard_b64encode(buffer.getvalue()).decode("utf-8"), "image/jpeg"

    # Convert PDF to images
    images = convert_from_path(str(pdf_path), dpi=dpi)
    total_pages = len(images)
    print(f"   Found {total_pages} pages")

    # Handle page range
    start_page = 1
    end_page = total_pages
    if page_range:
        start_page = max(1, page_range[0])
        end_page = min(total_pages, page_range[1])

    selected_images = images[start_page - 1:end_page]
    print(f"   Processing pages {start_page}-{end_page}")

    # Convert each page
    markdown_parts = []
    iterator = list(enumerate(selected_images, start=start_page))
    iterator = tqdm(iterator, desc="🔄 Converting", unit="page", ncols=80)

    for page_num, image in iterator:
        try:
            base64_image, media_type = image_to_base64(image)

            message = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }],
            )

            markdown = message.content[0].text
            markdown_parts.append(f"<!-- Page {page_num} -->\n\n{markdown}")
            time.sleep(0.5)  # Rate limiting

        except anthropic.RateLimitError:
            print(f"\n⚠️  Rate limit at page {page_num}. Waiting 60s...")
            time.sleep(60)
            # Retry
            base64_image, media_type = image_to_base64(image)
            message = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_image}},
                        {"type": "text", "text": prompt},
                    ],
                }],
            )
            markdown_parts.append(f"<!-- Page {page_num} -->\n\n{message.content[0].text}")

        except Exception as e:
            print(f"\n❌ Error on page {page_num}: {e}")
            markdown_parts.append(f"<!-- Page {page_num} -->\n\n[Fehler bei der Konvertierung: {e}]")

    # Build final markdown
    header = f"""# {pdf_path.stem}

> Automatisch konvertiert aus PDF mit Claude Vision API
> Seiten: {start_page}-{end_page} von {total_pages}

"""
    full_markdown = header + "\n\n---\n\n".join(markdown_parts)

    # Write output
    output_path.write_text(full_markdown, encoding="utf-8")
    print(f"\n✅ Created: {output_path}")

    return str(output_path)


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown (dual-mode)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Fast mode (default) - good for simple PDFs
    python pdf_converter.py document.pdf

    # Vision mode - prepare images for Claude Code
    python pdf_converter.py textbook.pdf --mode vision

    # Vision mode with direct API (requires ANTHROPIC_API_KEY)
    python pdf_converter.py textbook.pdf --mode vision --use-api

    # Vision mode with page range
    python pdf_converter.py book.pdf --mode vision --pages 1-10

    # Fast mode without image extraction
    python pdf_converter.py document.pdf --no-images
""",
    )

    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", nargs="?", help="Output path (default: input_name.md or input_name_pages/)")
    parser.add_argument(
        "--mode", "-m",
        choices=["fast", "vision"],
        default="fast",
        help="Conversion mode: fast (PyMuPDF) or vision (image-based)",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip image extraction (fast mode only)",
    )

    # Vision mode options
    vision_group = parser.add_argument_group("Vision mode options")
    vision_group.add_argument(
        "--use-api",
        action="store_true",
        help="Use direct Anthropic API instead of Claude Code (requires ANTHROPIC_API_KEY)",
    )
    vision_group.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="DPI for PDF rendering (default: 150, use 200+ for --use-api)",
    )
    vision_group.add_argument(
        "--pages",
        help="Page range, e.g., '1-10' or '5-5' for single page",
    )

    # Direct API options
    api_group = parser.add_argument_group("Direct API options (--use-api)")
    api_group.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Claude model (default: claude-sonnet-4-20250514)",
    )
    api_group.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    )

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    if not input_path.suffix.lower() == ".pdf":
        print(f"❌ Not a PDF file: {input_path}")
        sys.exit(1)

    # Parse page range
    page_range = None
    if args.pages:
        try:
            parts = args.pages.split("-")
            page_range = (int(parts[0]), int(parts[1]))
        except (ValueError, IndexError):
            print(f"❌ Invalid page range: {args.pages}")
            print("   Use format: START-END (e.g., 1-10)")
            sys.exit(1)

    # Run conversion based on mode
    if args.mode == "fast":
        output_path = Path(args.output) if args.output else input_path.with_suffix(".md")
        convert_fast(
            pdf_path=input_path,
            output_path=output_path,
            extract_images=not args.no_images,
        )

    elif args.mode == "vision":
        if args.use_api:
            # Direct API mode
            output_path = Path(args.output) if args.output else input_path.with_suffix(".md")
            try:
                convert_vision_api(
                    pdf_path=input_path,
                    output_path=output_path,
                    model=args.model,
                    dpi=args.dpi if args.dpi != 150 else 200,  # Higher default for API
                    page_range=page_range,
                    api_key=args.api_key,
                )
            except Exception as e:
                if "AuthenticationError" in str(type(e)):
                    print("❌ Invalid API key. Set ANTHROPIC_API_KEY or use --api-key")
                else:
                    print(f"❌ Error: {e}")
                sys.exit(1)
        else:
            # Claude Code mode - just prepare images
            output_dir = Path(args.output) if args.output else input_path.parent
            image_paths = convert_vision_prepare(
                pdf_path=input_path,
                output_dir=output_dir,
                dpi=args.dpi,
                page_range=page_range,
            )
            print(f"\n📋 Next step: Let Claude Code analyze the images:")
            print(f"   Images are in: {input_path.stem}_pages/")
            print(f"   Claude Code can read these with the Read tool")


if __name__ == "__main__":
    main()
