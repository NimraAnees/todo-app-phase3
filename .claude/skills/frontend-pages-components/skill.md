---
name: frontend-pages-components
description: Build responsive frontend pages, reusable components, layouts, and styling for modern web applications.
---

# Frontend Page & Component Development

## Instructions

1. **Page structure**
   - Semantic HTML structure
   - Clear sectioning (header, main, footer)
   - Accessible markup (ARIA where needed)

2. **Component design**
   - Reusable UI components
   - Props-driven and modular design
   - Separation of concerns (logic vs UI)

3. **Layout system**
   - Responsive grid / flexbox layouts
   - Mobile-first approach
   - Consistent spacing and alignment

4. **Styling**
   - Clean, scalable CSS (Tailwind / CSS Modules / SCSS)
   - Design tokens (colors, spacing, typography)
   - Dark/light mode support (optional)

5. **Interactivity**
   - Hover and focus states
   - Smooth transitions
   - Basic animations for UX feedback

---

## Best Practices
- Build reusable components first
- Keep styles consistent across pages
- Prefer composition over duplication
- Ensure responsiveness on all screen sizes
- Optimize for performance and accessibility

---

## Example Structure
```html
<main class="container">
  <header class="page-header">
    <h1 class="title">Page Title</h1>
    <p class="subtitle">Short description of the page</p>
  </header>

  <section class="grid-layout">
    <div class="card component">
      <h2>Component Title</h2>
      <p>Component description</p>
      <button class="primary-button">Action</button>
    </div>
  </section>
</main>
