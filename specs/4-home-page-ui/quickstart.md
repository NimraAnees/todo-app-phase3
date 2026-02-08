# Quickstart: Home Page UI Enhancement

**Feature**: 4-home-page-ui
**Time to Implement**: ~30-60 minutes
**Difficulty**: Low

## Prerequisites

- [ ] Node.js and npm installed
- [ ] Frontend dependencies installed (`cd frontend && npm install`)
- [ ] Development server can start (`npm run dev`)
- [ ] Access to a web browser for testing

## Quick Implementation Guide

### Step 1: Start Development Server

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 in your browser.

### Step 2: Modify the Home Page

Edit `frontend/app/page.tsx` with the new design:

```tsx
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center min-h-screen px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          {/* App Name */}
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            <span className="block">Todo App</span>
            <span className="block text-blue-600 text-3xl sm:text-4xl md:text-5xl mt-2">
              Get Things Done
            </span>
          </h1>

          {/* Tagline */}
          <p className="max-w-xl mx-auto text-lg text-gray-600 sm:text-xl md:text-2xl">
            Organize your tasks. Boost your productivity.
            A simple and elegant way to manage your daily tasks.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
            <Link
              href="/auth/signup"
              className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-white bg-blue-600 border border-transparent rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 min-h-[44px] transition-colors"
            >
              Get Started Free
            </Link>
            <Link
              href="/auth/login"
              className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 min-h-[44px] transition-colors"
            >
              Sign In
            </Link>
          </div>

          {/* Feature Highlights (Optional) */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-16 pt-8 border-t border-gray-200">
            <div className="text-center">
              <div className="text-3xl mb-2">📝</div>
              <h3 className="font-semibold text-gray-900">Simple</h3>
              <p className="text-gray-600 text-sm">Easy to use, no learning curve</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🔒</div>
              <h3 className="font-semibold text-gray-900">Secure</h3>
              <p className="text-gray-600 text-sm">Your data is private and protected</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">📱</div>
              <h3 className="font-semibold text-gray-900">Responsive</h3>
              <p className="text-gray-600 text-sm">Works on any device</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
```

### Step 3: Test Responsive Design

Test at these viewports:
- **Mobile**: 320px, 375px (iPhone SE, iPhone 12)
- **Tablet**: 768px (iPad)
- **Desktop**: 1024px, 1280px, 1920px

Use Chrome DevTools (F12 → Toggle Device Toolbar) to test.

### Step 4: Verify Checklist

- [ ] App name visible above the fold
- [ ] Tagline clearly communicates purpose
- [ ] "Get Started" button is prominent
- [ ] "Sign In" button is accessible
- [ ] No horizontal scroll on mobile
- [ ] Buttons are at least 44px tall
- [ ] Text is readable without zooming

## Common Issues & Solutions

### Issue: Buttons not stacking on mobile
**Solution**: Use `flex-col sm:flex-row` to stack on mobile, row on larger screens.

### Issue: Text too small on mobile
**Solution**: Use responsive sizing like `text-4xl sm:text-5xl md:text-6xl`.

### Issue: Content not centered
**Solution**: Use `flex items-center justify-center` on the container.

### Issue: Horizontal scroll appears
**Solution**: Ensure no fixed widths exceed viewport, use `max-w-full` on containers.

## Testing Commands

```bash
# Start dev server
cd frontend && npm run dev

# Build production (check for errors)
npm run build

# Run linting
npm run lint
```

## Files Changed

| File | Change Type | Description |
|------|-------------|-------------|
| `app/page.tsx` | Modified | New hero section design |

## Rollback

If issues occur, revert `page.tsx` to the original:

```bash
git checkout HEAD -- frontend/app/page.tsx
```
