# EduLearn Frontend

A modern, responsive learning management system built with React and modular CSS.

## 🎨 CSS Architecture

This project uses a modular CSS architecture with reusable components and utility classes.

### File Structure

```
src/
├── styles/
│   └── components.css    # Reusable component styles
├── index.css            # Base styles and utilities
└── ...
```

### CSS Organization

#### 1. Base Styles (`index.css`)
- **Reset and base styles**: Global resets and base typography
- **Layout utilities**: Flexbox, Grid, and positioning classes
- **Spacing utilities**: Margin, padding, and gap classes
- **Typography utilities**: Font sizes, weights, and text alignment
- **Color utilities**: Text and background color classes
- **Border utilities**: Border styles and radius classes
- **Shadow utilities**: Box shadow classes
- **Responsive utilities**: Media query breakpoints
- **Animation utilities**: Keyframes and animation classes

#### 2. Component Styles (`styles/components.css`)
- **Button components**: Multiple button variants and sizes
- **Card components**: Course cards, stats cards, and general cards
- **Form components**: Inputs, selects, and form layouts
- **Navigation components**: Header, nav links, and breadcrumbs
- **Loading components**: Spinners and loading states
- **Badge components**: Status and category badges
- **Avatar components**: User avatars with different sizes

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## 🎯 Component Usage

### Buttons

```jsx
// Primary button
<button className="btn btn-primary">Primary Action</button>

// Secondary button
<button className="btn btn-secondary">Secondary Action</button>

// Outline button
<button className="btn btn-outline">Outline Button</button>

// Danger button
<button className="btn btn-danger">Delete</button>

// Button sizes
<button className="btn btn-primary btn-sm">Small</button>
<button className="btn btn-primary btn-lg">Large</button>
<button className="btn btn-primary btn-full">Full Width</button>
```

### Cards

```jsx
// Basic card
<div className="card">
  <div className="card-body">
    <h3>Card Title</h3>
    <p>Card content goes here</p>
  </div>
</div>

// Course card
<div className="course-card">
  <img src="course-image.jpg" className="course-card-image" />
  <div className="course-card-content">
    <div className="course-card-header">
      <span className="course-category">Programming</span>
      <div className="course-rating">
        <Star className="w-4 h-4 fill-current" />
        <span>4.8</span>
      </div>
    </div>
    <h3 className="course-title">Course Title</h3>
    <p className="course-description">Course description</p>
    <div className="course-meta">
      <span className="course-meta-item">
        <Clock className="w-4 h-4" />
        8 weeks
      </span>
    </div>
  </div>
</div>

// Stats card
<div className="stats-card">
  <div className="stats-card-content">
    <div className="stats-icon blue">
      <BookOpen className="w-6 h-6" />
    </div>
    <div className="stats-info">
      <div className="stats-label">Enrolled Courses</div>
      <div className="stats-value">5</div>
    </div>
  </div>
</div>
```

### Forms

```jsx
// Form group
<div className="form-group">
  <label className="form-label">Email</label>
  <input type="email" className="form-input" placeholder="Enter your email" />
</div>

// Search input
<div className="search-container">
  <Search className="search-icon w-5 h-5" />
  <input type="text" className="search-input" placeholder="Search..." />
</div>

// Select input
<select className="select-input">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

### Navigation

```jsx
// Header
<header className="header">
  <div className="header-content">
    <div className="header-brand">
      <Logo className="w-8 h-8" />
      <span>Brand Name</span>
    </div>
    <div className="header-actions">
      <button className="header-button">Action</button>
    </div>
  </div>
</header>

// Nav links
<a href="#" className="nav-link">
  <Home className="w-5 h-5" />
  Dashboard
</a>
```

### Badges

```jsx
<span className="badge badge-success">Active</span>
<span className="badge badge-warning">Pending</span>
<span className="badge badge-info">Info</span>
<span className="badge badge-danger">Error</span>
```

### Avatars

```jsx
<div className="avatar">JD</div>
<div className="avatar avatar-sm">JD</div>
<div className="avatar avatar-lg">JD</div>
```

## 🎨 Color Palette

### Primary Colors
- **Blue**: `#667eea` to `#764ba2` (gradient)
- **Green**: `#4ade80` to `#22c55e` (gradient)
- **Purple**: `#a855f7` to `#9333ea` (gradient)
- **Orange**: `#f59e0b` to `#d97706` (gradient)
- **Red**: `#ff6b6b` to `#ee5a52` (gradient)

### Neutral Colors
- **Gray 50**: `#f9fafb`
- **Gray 100**: `#f3f4f6`
- **Gray 200**: `#e5e7eb`
- **Gray 300**: `#d1d5db`
- **Gray 400**: `#9ca3af`
- **Gray 500**: `#6b7280`
- **Gray 600**: `#4b5563`
- **Gray 700**: `#374151`
- **Gray 800**: `#1f2937`
- **Gray 900**: `#111827`

## 📱 Responsive Design

The CSS includes responsive utilities for different screen sizes:

- **sm**: 640px and up
- **md**: 768px and up
- **lg**: 1024px and up
- **xl**: 1280px and up

### Example Usage

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* Responsive grid */}
</div>

<div className="text-lg md:text-xl lg:text-2xl">
  {/* Responsive typography */}
</div>
```

## 🎭 Animations

### Built-in Animations

```jsx
// Fade in
<div className="animate-fade-in">Content</div>

// Slide up
<div className="animate-slide-up">Content</div>

// Bounce in
<div className="animate-bounce-in">Content</div>

// Spin
<div className="animate-spin">Loading...</div>
```

### Hover Effects

```jsx
// Scale on hover
<div className="hover:scale-105">Hover me</div>

// Shadow on hover
<div className="hover:shadow-lg">Hover me</div>

// Color change on hover
<button className="hover:bg-blue-50">Hover me</button>
```

## 🔧 Customization

### Adding New Components

1. Add your component styles to `styles/components.css`
2. Follow the existing naming conventions
3. Include responsive variants if needed
4. Add hover and focus states

### Example Component

```css
/* Custom component */
.custom-component {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
}

.custom-component:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Responsive variants */
@media (max-width: 768px) {
  .custom-component {
    padding: 1rem;
  }
}
```

## 🚀 Best Practices

1. **Use semantic class names**: Choose descriptive names that explain the purpose
2. **Follow the component pattern**: Group related styles together
3. **Use utility classes**: Leverage existing utilities for common patterns
4. **Keep it responsive**: Always consider mobile-first design
5. **Maintain consistency**: Use the established color palette and spacing scale
6. **Optimize for performance**: Minimize CSS bundle size
7. **Test across browsers**: Ensure cross-browser compatibility

## 📚 Additional Resources

- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [CSS Animation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)

## 🤝 Contributing

When contributing to the CSS:

1. Follow the existing naming conventions
2. Add comments for complex selectors
3. Test on multiple screen sizes
4. Ensure accessibility standards are met
5. Update this documentation if adding new components

## 📄 License

This project is licensed under the MIT License.
