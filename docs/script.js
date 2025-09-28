// Brainrot Lang Documentation Scripts
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scrolling for navigation
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add syntax highlighting for code blocks (basic implementation)
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(block => {
    // Add line numbers
    const lines = block.textContent.split('\n');
    if (lines.length > 1) {
      const numberedLines = lines.map((line, index) => {
        return `<span class="line-number">${index + 1}</span>${line}`;
      }).join('\n');
      block.innerHTML = numberedLines;
    }
  });

  // Add copy-to-clipboard functionality for code blocks
  codeBlocks.forEach(block => {
    const button = document.createElement('button');
    button.textContent = 'Copy';
    button.className = 'copy-btn';
    button.style.cssText = `
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;
      background: var(--rule);
      color: var(--fg);
      border: 1px solid var(--rule);
      border-radius: 4px;
      padding: 0.25rem 0.5rem;
      cursor: pointer;
      font-size: 0.8rem;
    `;
    
    const pre = block.parentElement;
    pre.style.position = 'relative';
    pre.appendChild(button);
    
    button.addEventListener('click', function() {
      navigator.clipboard.writeText(block.textContent).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => {
          button.textContent = 'Copy';
        }, 2000);
      });
    });
  });

  // Add search functionality
  const searchInput = document.createElement('input');
  searchInput.type = 'text';
  searchInput.placeholder = 'Search documentation...';
  searchInput.style.cssText = `
    width: 100%;
    padding: 0.5rem;
    margin: 1rem 0;
    background: var(--codebg);
    border: 1px solid var(--rule);
    border-radius: 4px;
    color: var(--fg);
    font-size: 1rem;
  `;
  
  const header = document.querySelector('header');
  header.appendChild(searchInput);
  
  searchInput.addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const sections = document.querySelectorAll('section');
    
    sections.forEach(section => {
      const text = section.textContent.toLowerCase();
      if (query === '' || text.includes(query)) {
        section.style.display = 'block';
      } else {
        section.style.display = 'none';
      }
    });
  });

  // Add table of contents
  const toc = document.createElement('nav');
  toc.innerHTML = '<h3>Table of Contents</h3><ul></ul>';
  toc.style.cssText = `
    position: fixed;
    top: 2rem;
    right: 2rem;
    width: 200px;
    background: var(--codebg);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 1rem;
    max-height: 80vh;
    overflow-y: auto;
    z-index: 1000;
  `;
  
  const sections = document.querySelectorAll('section[id]');
  const tocList = toc.querySelector('ul');
  
  sections.forEach(section => {
    const link = document.createElement('a');
    link.href = `#${section.id}`;
    link.textContent = section.querySelector('h2').textContent;
    link.style.cssText = `
      display: block;
      padding: 0.25rem 0;
      color: var(--fg);
      text-decoration: none;
    `;
    
    const li = document.createElement('li');
    li.appendChild(link);
    tocList.appendChild(li);
  });
  
  document.body.appendChild(toc);
});
