# Swagger UI Customization Guide

This document explains the customizations made to Swagger UI in the FastAPI application, including API versioning, theme toggle functionality, and custom OpenAPI schema modifications.

## Table of Contents

1. [Overview](#overview)
2. [API Versioning](#api-versioning)
3. [Custom OpenAPI Schema](#custom-openapi-schema)
4. [Theme Toggle (Light/Dark Mode)](#theme-toggle-lightdark-mode)
5. [Module-Based Tagging](#module-based-tagging)
6. [File Structure](#file-structure)
7. [Configuration](#configuration)
8. [Customization Guide](#customization-guide)

---

## Overview

The Swagger UI implementation includes several customizations:

- **API Versioning**: Support for multiple API versions (v1, v2, latest) with switchable documentation
- **Theme Toggle**: Light and dark mode support with persistent user preferences
- **Custom OpenAPI Schema**: Modified schema with server definitions for version switching
- **Module-Based Organization**: API endpoints organized by modules (health, auth) rather than versions
- **Static File Management**: External JavaScript for theme management

---

## API Versioning

### Implementation

API versioning is implemented using `fastapi-versioning` library with the following configuration:

```python
from fastapi_versioning import VersionedFastAPI

app = VersionedFastAPI(
    base_app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    enable_latest=True,
    enable_docs=True,
)
```

### Version Format

- **Version Format**: `{major}` - Uses major version number (1, 2, etc.)
- **Prefix Format**: `/api/v{major}` - Creates routes like `/api/v1`, `/api/v2`
- **Latest Endpoint**: Enabled - Provides `/latest` endpoint pointing to the latest version

### Route Versioning

Routes are versioned using the `@version` decorator:

```python
from fastapi_versioning import version

@router.get("/health")
@version(1)  # This route belongs to v1
async def health_check():
    return {"status": "ok", "message": "API v1 is running"}
```

### Version Endpoints

- `/api/v1/*` - Version 1 endpoints
- `/api/v2/*` - Version 2 endpoints
- `/latest/*` - Latest version endpoints (points to highest version)

---

## Custom OpenAPI Schema

### Custom Schema Function

The OpenAPI schema is customized to include:

1. **Multiple Servers**: Server dropdown in Swagger UI for version switching
2. **Custom Logo**: Application logo in the info section
3. **Proper Metadata**: Title, description, and version information

```python
def custom_openapi(app: FastAPI):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.1.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom logo
    openapi_schema["info"]["x-logo"] = {
        "url": "https://img.lovepik.com/element/45015/3146.png_300.png"
    }
    
    return openapi_schema
```

### Server Definitions

The schema includes server definitions for version switching:

- `/api/v1` - Version 1 server
- `/api/v2` - Version 2 server
- `/latest` - Latest version server

These appear in the Swagger UI server dropdown, allowing users to switch between API versions.

---

## Theme Toggle (Light/Dark Mode)

### Overview

The theme toggle feature allows users to switch between light and dark modes in Swagger UI, with preferences saved in browser localStorage.

### Implementation

The theme toggle is implemented using:

1. **External JavaScript File**: `app/static/js/theme-toggle.js`
2. **Middleware Injection**: `ThemeToggleDocsMiddleware` injects the script tag
3. **Dynamic CSS Injection**: Dark mode CSS is injected/removed based on theme selection

### Features

- **Persistent Preferences**: Theme choice saved in `localStorage`
- **Default Theme**: Dark mode (configurable)
- **Toggle Button**: Fixed position button in top-right corner
- **Smooth Transitions**: CSS transitions for theme switching
- **Comprehensive Styling**: All Swagger UI elements styled for dark mode

### Theme Toggle Button

**Location**: Top-right corner of Swagger UI

**Styling**:
- Gradient background (purple: `#667eea` to `#764ba2`)
- Rounded pill shape
- Icon + text display (☀️ Light / 🌙 Dark)
- Hover effects with elevation
- Press animation

**Functionality**:
- Click to toggle between light and dark themes
- Button text/icon updates based on current theme
- Theme preference persists across page refreshes

### Dark Mode Styling

The dark mode includes comprehensive styling for:

- **Background Colors**: Dark gray (`#1e1e1e`, `#252526`, `#2d2d2d`)
- **Text Colors**: Light gray (`#d4d4d4`) with high contrast
- **Tags**: Teal/cyan (`#4ec9b0`) for visibility
- **Parameters**: Light blue (`#9cdcfe`) for names, orange (`#ce9178`) for types
- **HTTP Methods**: Color-coded backgrounds (GET: teal, POST: blue, PUT: yellow, DELETE: red)
- **Input Fields**: Dark backgrounds with light text
- **Tables**: Alternating row colors for readability
- **Code Blocks**: Dark backgrounds with syntax highlighting

### JavaScript Functions

#### Core Functions

- `getTheme()`: Retrieves theme from localStorage (defaults to dark)
- `setTheme(theme)`: Saves theme preference and applies it
- `applyTheme(theme)`: Applies the selected theme (injects/removes CSS)
- `toggleTheme()`: Switches between light and dark themes
- `getDarkModeCSS()`: Returns the complete dark mode CSS string
- `addThemeToggle()`: Creates and positions the toggle button
- `initTheme()`: Initializes theme on page load

#### Initialization

The theme is initialized on:
- `DOMContentLoaded` event
- Immediate execution if DOM is already loaded
- `window.load` event as backup

---

## Module-Based Tagging

### Organization Strategy

API endpoints are organized by **modules** rather than versions:

- **health**: Health check endpoints
- **auth**: Authentication endpoints

### Implementation

```python
# In router files
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
```

### Benefits

- **Better Organization**: Endpoints grouped by functionality
- **Cleaner UI**: Easier to find related endpoints
- **Version Agnostic**: Same tags across all versions
- **Scalability**: Easy to add new modules

---

## File Structure

```
app/
├── api/
│   └── server.py              # Main FastAPI app, middleware, OpenAPI customization
├── static/
│   └── js/
│       └── theme-toggle.js    # Theme toggle JavaScript
└── core/
    └── middleware/
        └── headers.py         # Security headers (affects Swagger UI)
```

### Key Files

1. **`app/api/server.py`**:
   - FastAPI app creation
   - VersionedFastAPI wrapper
   - Custom OpenAPI schema
   - ThemeToggleDocsMiddleware

2. **`app/static/js/theme-toggle.js`**:
   - All theme toggle functionality
   - Dark mode CSS definitions
   - Button creation and management
   - LocalStorage management

---

## Configuration

### Swagger UI Parameters

Configured in `create_app()` function:

```python
swagger_ui_parameters={
    "syntaxHighlight.theme": "obsidian",  # Dark theme for code highlighting
    "filter": True,                       # Enable filtering
    "tagsSorter": "alpha",                # Sort tags alphabetically
    "operationsSorter": "alpha",          # Sort operations alphabetically
    "persistAuthorization": True,          # Save authorization state
    "displayRequestDuration": True,       # Show request duration
}
```

### Environment-Based Configuration

- **Docs URL**: Disabled in production (`docs_url=None`), enabled in dev/local
- **CSP**: Disabled in local/dev (to allow Swagger UI resources), enabled in prod

### Static Files Mounting

Static files are mounted after VersionedFastAPI wrapping:

```python
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
```

**Important**: Static files must be mounted on the wrapped app, not the base app, to avoid VersionedFastAPI processing errors.

---

## Customization Guide

### Changing Default Theme

Edit `app/static/js/theme-toggle.js`:

```javascript
// Change default from dark to light
function getTheme() {
    return localStorage.getItem(THEME_KEY) || LIGHT_THEME;  // Changed from DARK_THEME
}
```

### Modifying Dark Mode Colors

Edit the `getDarkModeCSS()` function in `theme-toggle.js`:

```javascript
function getDarkModeCSS() {
    return `
        html { background-color: #YOUR_COLOR !important; }
        // ... modify other colors
    `;
}
```

### Customizing Toggle Button

Modify the `addThemeToggle()` function:

```javascript
toggleBtn.style.cssText = 'position: fixed; top: 15px; right: 15px; ...';
// Change position, colors, size, etc.
```

### Adding New Server Versions

Update the `custom_openapi()` function to add more servers:

```python
openapi_schema["servers"] = [
    {"url": "/api/v1", "description": "Version 1"},
    {"url": "/api/v2", "description": "Version 2"},
    {"url": "/api/v3", "description": "Version 3"},  # New version
    {"url": "/latest", "description": "Latest Version"},
]
```

### Changing Module Tags

Update router files:

```python
# In app/api/v1/router.py or app/api/v2/router.py
api_router.include_router(
    new_module.router, 
    prefix="/new-module", 
    tags=["new-module"]
)
```

### Modifying OpenAPI Logo

Change the logo URL in `custom_openapi()`:

```python
openapi_schema["info"]["x-logo"] = {
    "url": "https://your-logo-url.com/logo.png"
}
```

---

## Troubleshooting

### Theme Toggle Not Appearing

1. **Check Static Files**: Ensure `/static/js/theme-toggle.js` is accessible
2. **Browser Console**: Check for JavaScript errors
3. **Middleware**: Verify `ThemeToggleDocsMiddleware` is added to the app
4. **Hard Refresh**: Clear cache and hard refresh (Ctrl+F5)

### Version Dropdown Not Showing

1. **OpenAPI Schema**: Verify `custom_openapi()` includes servers array
2. **VersionedFastAPI**: Ensure `enable_docs=True` is set
3. **Browser**: Check browser console for errors

### Dark Mode Not Applying

1. **CSS Injection**: Check if dark mode CSS is injected (inspect element)
2. **LocalStorage**: Verify theme is saved in localStorage
3. **JavaScript Errors**: Check browser console for errors
4. **File Path**: Ensure script tag path is correct (`/static/js/theme-toggle.js`)

### Static Files Not Loading

1. **Mounting**: Verify static files are mounted on the wrapped app
2. **Path**: Check the static directory path is correct
3. **Permissions**: Ensure file permissions allow reading
4. **VersionedFastAPI**: Static files must be mounted after wrapping

---

## Best Practices

1. **Keep JavaScript External**: Maintain theme toggle in separate file for easier updates
2. **Test Both Themes**: Ensure all UI elements are visible in both light and dark modes
3. **Version Management**: Use semantic versioning for API versions
4. **Documentation**: Keep API documentation updated with version changes
5. **Performance**: Minimize CSS and JavaScript for faster loading
6. **Accessibility**: Ensure sufficient color contrast in both themes
7. **Browser Compatibility**: Test in multiple browsers

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Swagger UI Configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
- [fastapi-versioning](https://github.com/DeanWay/fastapi-versioning)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

## Version History

- **v1.0.0**: Initial implementation
  - API versioning with VersionedFastAPI
  - Theme toggle (light/dark mode)
  - Custom OpenAPI schema
  - Module-based tagging
  - External JavaScript file structure

