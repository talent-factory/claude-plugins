# Handoff Examples

## Example 1: Minimal (Bug Fix)

```markdown
# Handoff: RBAC Regression Fix

**Date**: 2026-01-14 15:30
**Branch**: feature/TF-177-rbac-regression-exam-creation
**Linear Issue**: TF-177 - RAG Exam Creator Premium Feature Bug

## Original Task

RAG Exam Creator displays "Premium Feature" upgrade prompt despite Full Deployment Mode.

## Completed Work

- Modified `.env.example` (documented DEPLOYMENT_MODE variables)
- Investigated `packages/core/backend/main.py` (identified RBAC logic)
- Analyzed frontend component loading

## Current State

**Modified Files** (uncommitted):

- `.env.example` - New variables documented
- `packages/core/backend/main.py` - Debug logging added

## Subsequent Steps

1. **Verify RBAC logic**: `packages/core/backend/main.py:712`
2. **Test frontend premium loading**: `packages/core/frontend/src/pages/Exams.tsx:45`
3. **Write integration test**: New test for RBAC + Deployment Mode

## For the Subsequent Agent

Backend appears correctly configured. The issue likely resides in frontend component loading. Examine `Exams.tsx` for premium import logic and how `deploymentMode` is retrieved from the context.
```

## Example 2: Comprehensive (Feature Development)

```markdown
# Handoff: Dark Mode Implementation

**Date**: 2026-01-14 18:45
**Branch**: feature/dark-mode-toggle
**Linear Issue**: TF-234 - Dark Mode for Settings Page

## Original Task

Implement a Dark Mode toggle in the application settings. The mode shall be persistently stored and affect all components.

**Business Value**: User feedback indicates high demand (47% of support tickets mention eye strain during nighttime usage).

## Completed Work

### Changes

| File                                      | Modification                 | Status      |
| ----------------------------------------- | ---------------------------- | ----------- |
| `src/contexts/ThemeContext.tsx`           | New context for theme state  | Committed   |
| `src/hooks/useTheme.ts`                   | Custom hook for theme access | Committed   |
| `src/components/Settings/ThemeToggle.tsx` | Toggle component             | Uncommitted |
| `src/styles/themes/dark.css`              | Dark mode CSS variables      | Uncommitted |

### Successful Approaches

1. **CSS Custom Properties for Theming**
   - Implementation: All colors defined as CSS variables
   - Rationale for success: Simple switching without component re-renders
   - Relevant files: `src/styles/themes/light.css`, `dark.css`

2. **localStorage for Persistence**
   - Implementation: Store theme preference in localStorage
   - Rationale for success: Functions without backend modification

## Failed Attempts

### Attempt 1: Styled-Components ThemeProvider

**Approach**: Inject theme via Styled-Components ThemeProvider

**Error Message**:
```

Warning: Cannot update a component while rendering a different component
Error in useLayoutEffect when theme changes

```

**Failure Analysis**: Race condition between theme change and component render. Styled-Components requires re-rendering of all components.

**Lessons Learned**: CSS variables are more performant for global theming.

### Attempt 2: System Preference Detection

**Approach**: Use `prefers-color-scheme` media query as default

**Issue**: Functioned correctly, but user setting override was complex

**Rationale for Abandonment**: User preference should always take precedence. Media query only serves as initial default.

## Current State

### Git Status

```

On branch feature/dark-mode-toggle
Changes not staged for commit:
modified: src/components/Settings/ThemeToggle.tsx
modified: src/styles/themes/dark.css

Untracked files:
src/components/Settings/ThemeToggle.test.tsx

````

### Modified Files

| File | Description of Changes |
|------|------------------------|
| `ThemeToggle.tsx` | Toggle UI complete, animation pending |
| `dark.css` | 80% of variables defined, sidebar pending |

### Environment

- **Services**: Dev server running on localhost:3000
- **Dependencies**: No new dependencies required
- **Browser Support**: CSS variables supported from IE11 (polyfill available)

## Subsequent Steps

### Priority 1: Complete Dark Theme for Sidebar

**Objective**: Define CSS variables for sidebar components

**Location**: `src/styles/themes/dark.css:45-80`

**Approach**:
1. Add sidebar background variable
2. Adjust sidebar border color
3. Configure active item highlight for dark mode

**Acceptance Criteria**:
- [ ] Sidebar displays correct dark mode background
- [ ] Contrast ratio minimum 4.5:1 (WCAG AA)
- [ ] Hover states visible

### Priority 2: Toggle Animation

**Objective**: Smooth transition during theme change

**Location**: `src/components/Settings/ThemeToggle.tsx:23`

**Approach**:
1. Apply CSS transition to body/html element
2. Use 200ms ease-in-out for color and background-color
3. Prevent flash on initial load (avoid FOUC)

### Priority 3: Unit Tests

**Objective**: Tests for ThemeContext and useTheme hook

**Location**: `src/contexts/ThemeContext.test.tsx` (create new file)

**Approach**:
1. Test: Initial theme from localStorage
2. Test: Theme toggle functionality
3. Test: System preference as fallback

## Important References

### Relevant Files

| File | Lines | Relevance |
|------|-------|-----------|
| `src/contexts/ThemeContext.tsx` | 1-45 | Central theme logic |
| `src/styles/themes/light.css` | - | Reference for variable names |
| `src/App.tsx` | 12-15 | ThemeProvider must wrap here |

### Documentation

- [CSS Custom Properties Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [WCAG Contrast Requirements](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

### Code Patterns

```tsx
// Standard theme usage pattern in this project:
import { useTheme } from '@/hooks/useTheme';

function MyComponent() {
  const { theme, toggleTheme } = useTheme();
  return <button onClick={toggleTheme}>Current: {theme}</button>;
}
````

## Important Notes

- **Prevent FOUC**: Script in `<head>` must set theme before render (refer to `public/index.html:15`)
- **Avoid `!important`**: All styles via CSS variables, no overrides
- **Test in Safari**: Safari has a bug with CSS variables in pseudo-elements

## For the Subsequent Agent

Theme system is implemented and functional. Primary remaining work involves CSS refinement for sidebar and animation. The ThemeContext in `src/contexts/ThemeContext.tsx` is the central location. Begin with `dark.css:45` for the missing sidebar variables.

````

## Example 3: With Linear Issue

```markdown
# Handoff: API Rate Limiting

**Date**: 2026-01-14 12:00
**Branch**: feature/TF-456-api-rate-limiting
**Linear Issue**: [TF-456](https://linear.app/team/issue/TF-456) - Implement API Rate Limiting

## Original Task

From Linear Issue TF-456:
> Implement rate limiting for the Public API. Maximum 100 requests/minute per API key. Return 429 response when exceeded.

**Acceptance Criteria from Linear**:
- [ ] Redis-based token bucket
- [ ] Configurable limits per endpoint
- [ ] Proper 429 response with Retry-After header

## Completed Work

- Redis client setup in `src/lib/redis.ts`
- Rate limiter middleware skeleton
- Unit tests for token bucket algorithm

## Current State

**Linear Status**: In Progress
**Blocker**: Redis connection in staging environment not configured

## Subsequent Steps

1. **Contact DevOps**: Request Redis for staging
2. **Complete middleware**: `src/middleware/rateLimiter.ts:45`
3. **Integration tests**: After Redis setup

## For the Subsequent Agent

Rate limiter logic is complete but not testable without Redis in staging. Coordinate with DevOps (ticket TF-457 created) or test locally with Docker Redis.
````
