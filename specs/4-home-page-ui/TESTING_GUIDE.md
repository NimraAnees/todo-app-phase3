# Home Page UI Testing Guide

**Feature**: Home Page UI Enhancement (spec-4)
**Branch**: `4-home-page-ui`
**Date**: 2026-02-07
**Status**: Ready for Manual Testing

## Overview

This guide provides step-by-step instructions for completing the remaining manual testing tasks (T018-T029) for the Home Page UI Enhancement feature.

## Prerequisites

- [ ] Development server is running: `cd frontend && npm run dev`
- [ ] Browser DevTools accessible (F12)
- [ ] Access to multiple browsers (Chrome, Firefox, Safari, Edge)

## Test Checklist

### Phase 4: Mobile User Access (US2)

#### T018: Mobile Viewport Testing (320px, 375px)

**Objective**: Verify no horizontal scrolling on small mobile devices

**Steps**:
1. Open http://localhost:3000 in Chrome
2. Open DevTools (F12) → Toggle Device Toolbar (Ctrl+Shift+M)
3. Test 320px viewport:
   - Set device to "iPhone SE" or custom 320x568
   - Scroll through entire page
   - Verify: No horizontal scroll bar appears
   - Verify: All content fits within viewport
   - Verify: Text is readable without zooming
4. Test 375px viewport:
   - Set device to "iPhone 12 Pro" or custom 375x667
   - Repeat verification steps above

**Expected Results**:
- [ ] No horizontal scroll at 320px
- [ ] No horizontal scroll at 375px
- [ ] All buttons are tappable (44px+ height)
- [ ] Text is legible (16px minimum)
- [ ] Content is centered and properly padded

**Pass/Fail**: ___________

---

### Phase 5: Tablet and Desktop Responsiveness (US3)

#### T023: Desktop Viewport Testing (768px, 1024px, 1280px, 1920px)

**Objective**: Verify proper scaling across all desktop viewports

**Steps**:
1. Open http://localhost:3000 in Chrome
2. Open DevTools → Responsive Design Mode
3. Test each viewport:

   **768px (iPad)**:
   - Set to 768x1024
   - Verify: Content uses available width with margins
   - Verify: Buttons display side-by-side (not stacked)

   **1024px (iPad Pro)**:
   - Set to 1024x1366
   - Verify: Heading scales up appropriately
   - Verify: Max-width constraint prevents stretching

   **1280px (Desktop)**:
   - Set to 1280x720
   - Verify: Content is centered with max-width
   - Verify: Typography is large and readable

   **1920px (Full HD)**:
   - Set to 1920x1080
   - Verify: Content doesn't stretch excessively
   - Verify: Hero section remains centered

**Expected Results**:
- [ ] Layout adjusts smoothly at each breakpoint
- [ ] Content is centered on large screens
- [ ] No awkward gaps or stretching
- [ ] Typography scales appropriately

**Pass/Fail**: ___________

---

#### T024: Smooth Layout Transitions

**Objective**: Verify smooth transitions when resizing browser window

**Steps**:
1. Open http://localhost:3000 in Chrome (full screen)
2. Slowly drag browser window from wide (1920px) to narrow (320px)
3. Observe layout changes at breakpoints:
   - Buttons transition from row to column layout
   - Typography scales smoothly
   - Spacing adjusts without jumps
4. Reverse: drag from narrow to wide
5. Repeat in Firefox

**Expected Results**:
- [ ] No visual glitches during resize
- [ ] No content overflow or clipping
- [ ] Breakpoint transitions are smooth
- [ ] No layout jumping or stuttering

**Pass/Fail**: ___________

---

### Phase 6: Polish & Cross-Cutting Concerns

#### T025: WCAG AA Color Contrast Compliance

**Objective**: Verify text contrast meets accessibility standards

**Steps**:
1. Open http://localhost:3000
2. Use contrast checking tool:
   - Option 1: Chrome DevTools → Inspect text → Contrast ratio
   - Option 2: WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/)
3. Check the following elements:

   **Text to Check**:
   - [ ] App name (gradient text on dark background)
   - [ ] Tagline (onyx-300 on onyx-900)
   - [ ] Body text (onyx-300 on onyx-900)
   - [ ] Button text ("Get Started" - black on emerald-500)
   - [ ] Button text ("Sign In" - onyx-300 on onyx-800)
   - [ ] Feature titles (onyx-50 on onyx-900)
   - [ ] Feature descriptions (onyx-400 on onyx-900)

**Required Ratios**:
- Normal text (< 18pt): 4.5:1 minimum
- Large text (≥ 18pt): 3:1 minimum

**Expected Results**:
- [ ] All text meets WCAG AA standards
- [ ] No contrast failures identified
- [ ] Gradient text is readable

**Pass/Fail**: ___________

**Issues Found**: ___________________________________________

---

#### T026: Lighthouse Accessibility Audit

**Objective**: Achieve 90+ accessibility score

**Steps**:
1. Open http://localhost:3000 in Chrome (Incognito mode recommended)
2. Open DevTools (F12) → Lighthouse tab
3. Configure audit:
   - Categories: Accessibility, Performance
   - Device: Mobile & Desktop
4. Run audit
5. Review results:
   - Accessibility score
   - Performance score
   - Identified issues

**Expected Results**:
- [ ] Accessibility score: ≥ 90
- [ ] Performance score: ≥ 90
- [ ] No critical issues
- [ ] All interactive elements have accessible names
- [ ] Focus indicators are visible

**Actual Results**:
- Accessibility Score: ___________
- Performance Score: ___________
- Issues Found: ___________________________________________

**Pass/Fail**: ___________

---

#### T027: Keyboard Navigation Testing

**Objective**: Verify all interactive elements are keyboard accessible

**Steps**:
1. Open http://localhost:3000
2. Click in address bar, then press Tab
3. Navigate through page using only keyboard:
   - Press Tab to move forward
   - Press Shift+Tab to move backward
   - Press Enter/Space to activate buttons

**Elements to Verify**:
- [ ] "Get Started" button receives focus (visible ring)
- [ ] "Sign In" button receives focus (visible ring)
- [ ] All feature cards are in tab order (if applicable)
- [ ] Focus indicators are clearly visible
- [ ] Tab order is logical (top to bottom, left to right)
- [ ] No keyboard traps (can tab through entire page)
- [ ] Enter key activates buttons correctly

**Expected Results**:
- [ ] All interactive elements are reachable via keyboard
- [ ] Focus indicators are visible (2px ring)
- [ ] Tab order matches visual order
- [ ] No elements are skipped

**Pass/Fail**: ___________

---

#### T028: Page Load Performance (3G Throttling)

**Objective**: Verify page loads in < 3 seconds on slow connections

**Steps**:
1. Open Chrome DevTools (F12) → Network tab
2. Enable network throttling:
   - Throttling: "Slow 3G"
   - Download: 400 Kbps
   - Upload: 400 Kbps
   - Latency: 2000ms
3. Reload page (Ctrl+Shift+R for hard reload)
4. Measure timing:
   - DOMContentLoaded (blue line)
   - Load (red line)
   - First Contentful Paint
   - Largest Contentful Paint

**Expected Results**:
- [ ] DOMContentLoaded: < 2 seconds
- [ ] Full page load: < 3 seconds
- [ ] First Contentful Paint: < 1.5 seconds
- [ ] Largest Contentful Paint: < 2.5 seconds

**Actual Results**:
- DOMContentLoaded: ___________
- Full Load: ___________
- FCP: ___________
- LCP: ___________

**Pass/Fail**: ___________

---

#### T029: Cross-Browser Testing

**Objective**: Verify consistent rendering across major browsers

**Steps**:
1. Test in each browser:

   **Chrome** (v120+):
   - [ ] Page loads successfully
   - [ ] Layout renders correctly
   - [ ] Buttons work correctly
   - [ ] Animations are smooth

   **Firefox** (v120+):
   - [ ] Page loads successfully
   - [ ] Layout renders correctly
   - [ ] Buttons work correctly
   - [ ] Gradient text displays properly

   **Safari** (v17+):
   - [ ] Page loads successfully
   - [ ] Layout renders correctly
   - [ ] Buttons work correctly
   - [ ] Webkit-specific styles work

   **Edge** (v120+):
   - [ ] Page loads successfully
   - [ ] Layout renders correctly
   - [ ] Buttons work correctly
   - [ ] Chromium rendering consistent

**Expected Results**:
- [ ] Consistent appearance across all browsers
- [ ] No browser-specific bugs
- [ ] All functionality works identically
- [ ] No console errors in any browser

**Issues Found**:
- Chrome: ___________________________________________
- Firefox: ___________________________________________
- Safari: ___________________________________________
- Edge: ___________________________________________

**Pass/Fail**: ___________

---

## Summary Report

### Test Results Overview

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| T018 | Mobile viewports (320px, 375px) | ⬜ | |
| T023 | Desktop viewports (768px-1920px) | ⬜ | |
| T024 | Smooth layout transitions | ⬜ | |
| T025 | WCAG AA color contrast | ⬜ | |
| T026 | Lighthouse accessibility audit | ⬜ | |
| T027 | Keyboard navigation | ⬜ | |
| T028 | Page load performance (3G) | ⬜ | |
| T029 | Cross-browser testing | ⬜ | |

**Legend**: ✅ Pass | ❌ Fail | ⬜ Not Tested

### Overall Status

- [ ] All tests passed
- [ ] Some tests failed (see notes above)
- [ ] Testing incomplete

### Issues to Address

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

### Next Steps

- [ ] Fix any identified issues
- [ ] Retest failed tests
- [ ] Update tasks.md with test results
- [ ] Create PR when all tests pass

---

## Quick Reference

### Useful Tools

- **Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Lighthouse**: Chrome DevTools → Lighthouse tab
- **Responsive Design**: Chrome DevTools → Toggle Device Toolbar (Ctrl+Shift+M)
- **Network Throttling**: Chrome DevTools → Network tab → Throttling dropdown

### Common Issues & Solutions

**Issue**: Horizontal scroll on mobile
- **Solution**: Check for hardcoded widths, ensure all elements use max-w-full

**Issue**: Poor contrast ratio
- **Solution**: Darken background or lighten text color

**Issue**: Focus indicators not visible
- **Solution**: Ensure focus:ring-2 classes are applied

**Issue**: Slow page load
- **Solution**: Optimize images, reduce JavaScript bundle size

---

## Completion Checklist

Before marking spec-4 as complete:

- [ ] All 8 manual tests completed
- [ ] All tests passed (or issues documented)
- [ ] Testing guide filled out completely
- [ ] Issues logged in GitHub (if any)
- [ ] tasks.md updated with test results
- [ ] Screenshots captured for documentation
- [ ] PR created with test results

**Tester Name**: ___________
**Date Completed**: ___________
**Signature**: ___________
