# UI/UX Framework Design

### Color System
```
Primary Colors:
- Deep Blue (#1E3A8A)     # Authority, trust
- Ocean Blue (#3B82F6)    # Action, interaction
- Soft Slate (#64748B)    # Text, subtle elements

Accent Colors:
- Emerald (#059669)       # Success, positive
- Amber (#D97706)        # Warning, attention
- Ruby (#DC2626)         # Error, important

Background Scale:
- Pure White (#FFFFFF)    # Main background
- Ghost White (#F8FAFC)   # Panels, cards
- Slate 50 (#F8FAFC)     # Subtle divisions
- Slate 100 (#F1F5F9)    # Hover states
```

### Typography
```
Font Stack:
- Inter for UI
- SF Pro Display for headings
- Mono font for code/numbers

Scale:
xs: 0.75rem   # Helper text
sm: 0.875rem  # Secondary text
base: 1rem    # Body text
lg: 1.125rem  # Emphasized text
xl: 1.25rem   # Small headings
2xl: 1.5rem   # Section headings
3xl: 1.875rem # Page headings
4xl: 2.25rem  # Hero text
```

### Spacing System
```
4px grid base:
1: 0.25rem (4px)   # Minimal spacing
2: 0.5rem  (8px)   # Tight spacing
3: 0.75rem (12px)  # Form elements
4: 1rem    (16px)  # Standard spacing
6: 1.5rem  (24px)  # Section spacing
8: 2rem    (32px)  # Major divisions
12: 3rem   (48px)  # Layout blocks
16: 4rem   (64px)  # Hero sections
```

### Component Architecture
```
1. Base Components:
   - Buttons (primary, secondary, text)
   - Forms (inputs, selects, checkboxes)
   - Cards/Panels
   - Navigation
   - Tables
   - Alerts/Messages

2. Composite Components:
   - Calendar views
   - Schedule grids
   - Data tables
   - Modal dialogs
   - Dropdown menus

3. Page Templates:
   - Dashboard layout
   - Calendar layout
   - Form pages
   - List views
   - Detail views
```

### HTMX Integration
```
Core Patterns:
1. Dynamic Loading:
   - Table pagination
   - Filtered results
   - Schedule updates
   - Form submission

2. Partial Updates:
   - Schedule changes
   - Status updates
   - Notifications
   - Counter updates

3. Polling:
   - Real-time updates
   - Status checks
   - Notification fetching
```

### Responsive Strategy
```
Breakpoints:
sm: 640px   # Mobile landscape
md: 768px   # Tablets
lg: 1024px  # Small laptops
xl: 1280px  # Laptops/Desktops
2xl: 1536px # Large screens

Layout Principles:
1. Mobile-first design
2. Fluid typography
3. Flexible grids
4. Progressive enhancement
```

### Animation Guidelines
```
Micro-interactions:
- Button states: 150ms
- Hover effects: 200ms
- Page transitions: 300ms
- Modal dialogs: 250ms

Properties:
- Transform for performance
- Opacity for visibility
- Scale for emphasis
- Translate for movement
```

### Django Template Structure
```
templates/
├── base/
│   ├── base.html          # Core template
│   ├── layout.html        # Page structure
│   └── components/        # Reusable parts
│       ├── navigation.html
│       ├── sidebar.html
│       ├── footer.html
│       └── messages.html
├── calendar/
│   ├── base.html         # Calendar base
│   ├── month.html
│   ├── week.html
│   └── components/       # Calendar parts
└── shared/
    ├── forms/
    ├── modals/
    └── widgets/
```

### Best Practices
```
1. Performance:
   - Lazy loading images
   - Deferred scripts
   - CSS critical path
   - HTMX for dynamics

2. Accessibility:
   - ARIA labels
   - Keyboard navigation
   - Color contrast
   - Focus management

3. Progressive Enhancement:
   - Core functionality without JS
   - HTMX as enhancement
   - Fallback patterns

4. State Management:
   - Clear loading states
   - Error handling
   - Empty states
   - Success feedback
```

Want me to detail any aspect or create specifications for specific components?