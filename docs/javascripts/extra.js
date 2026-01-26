// Custom JavaScript for Talent Factory Claude Plugins documentation

document.addEventListener('DOMContentLoaded', function() {
  // Add copy button functionality to command examples
  const commandExamples = document.querySelectorAll('.command-syntax');
  commandExamples.forEach(function(example) {
    example.style.cursor = 'pointer';
    example.title = 'Click to copy';
    
    example.addEventListener('click', function() {
      const text = this.textContent;
      navigator.clipboard.writeText(text).then(function() {
        // Show feedback
        const original = example.textContent;
        example.textContent = '✓ Copied!';
        setTimeout(function() {
          example.textContent = original;
        }, 1000);
      });
    });
  });

  // Add external link indicators
  const externalLinks = document.querySelectorAll('a[href^="http"]');
  externalLinks.forEach(function(link) {
    if (!link.hostname.includes('talent-factory.github.io')) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });

  // Smooth scroll for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Update URL without jumping
        history.pushState(null, null, '#' + targetId);
      }
    });
  });

  // Add version badge to plugin cards
  const pluginCards = document.querySelectorAll('.grid.cards li');
  pluginCards.forEach(function(card) {
    const versionMatch = card.textContent.match(/Version:\s*(\d+\.\d+\.\d+)/);
    if (versionMatch) {
      const badge = document.createElement('span');
      badge.className = 'plugin-badge';
      badge.textContent = 'v' + versionMatch[1];
      card.querySelector('h3, h4')?.appendChild(badge);
    }
  });
});

