# Templates

This directory contains template files for project generation.

## Structure

```
templates/
├── java/           # Java/Gradle templates
├── python/         # Python/uv templates
└── common/         # Common templates (LICENSE, README, etc.)
```

## Usage

Templates are currently embedded in the generator classes for simplicity.
External template files can be added here for customization.

## Customization

To customize templates:

1. Add your template file to the appropriate directory
2. Modify the corresponding generator class to use the external template
3. Use `{variable}` placeholders for dynamic content
