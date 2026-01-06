// Theme management for Swagger UI
const THEME_KEY = 'swagger-ui-theme';
const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';

// Get saved theme or default to dark
function getTheme() {
    return localStorage.getItem(THEME_KEY) || DARK_THEME;
}

// Save theme preference
function setTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
    applyTheme(theme);
}

// Force apply dark theme to schema elements
function forceSchemaDarkTheme() {
    if (getTheme() !== DARK_THEME) return;
    
    const modelBoxes = document.querySelectorAll('.swagger-ui .model-box');
    modelBoxes.forEach(box => {
        const allElements = box.querySelectorAll('*');
        allElements.forEach(el => {
            const computedStyle = window.getComputedStyle(el);
            const bgColor = computedStyle.backgroundColor;
            const textColor = computedStyle.color;
            
            if (bgColor && (bgColor.includes('255') || bgColor.includes('white') || bgColor.includes('#fff'))) {
                el.style.setProperty('background-color', '#1e1e1e', 'important');
                el.style.setProperty('background', '#1e1e1e', 'important');
            }
            
            if (textColor && (textColor.includes('128') || textColor.includes('gray') || textColor.includes('grey') || textColor.includes('#808'))) {
                el.style.setProperty('color', '#ffffff', 'important');
            }
        });
        
        const codeElements = box.querySelectorAll('pre, code');
        codeElements.forEach(el => {
            el.style.setProperty('background-color', '#1e1e1e', 'important');
            el.style.setProperty('color', '#ffffff', 'important');
        });
    });
}

// Apply theme
function applyTheme(theme) {
    const darkModeCSS = document.getElementById('swagger-dark-mode-css');
    const toggleBtn = document.getElementById('theme-toggle-btn');
    
    if (theme === DARK_THEME) {
        if (!darkModeCSS) {
            const style = document.createElement('style');
            style.id = 'swagger-dark-mode-css';
            style.textContent = getDarkModeCSS();
            document.head.appendChild(style);
        }
        if (toggleBtn) {
            toggleBtn.innerHTML = '<span style="font-size: 16px;">☀️</span><span>Light</span>';
            toggleBtn.title = 'Switch to Light Mode';
        }
        
        setTimeout(forceSchemaDarkTheme, 100);
        setTimeout(forceSchemaDarkTheme, 500);
        setTimeout(forceSchemaDarkTheme, 1000);
    } else {
        if (darkModeCSS) {
            darkModeCSS.remove();
        }
        if (toggleBtn) {
            toggleBtn.innerHTML = '<span style="font-size: 16px;">🌙</span><span>Dark</span>';
            toggleBtn.title = 'Switch to Dark Mode';
        }
    }
}

// Toggle theme
function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    setTheme(newTheme);
}

// Dark mode CSS - Cleaned and optimized
function getDarkModeCSS() {
    return `
        html, body { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        .swagger-ui { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        
        /* Top bar and info */
        .swagger-ui .topbar { background-color: #2d2d2d !important; }
        .swagger-ui .topbar * { color: #d4d4d4 !important; }
        .swagger-ui .info { background-color: #252526 !important; color: #d4d4d4 !important; }
        .swagger-ui .info * { color: #d4d4d4 !important; }
        .swagger-ui .info .base-url { color: #9cdcfe !important; }
        
        /* Scheme container */
        .swagger-ui .scheme-container { background-color: #252526 !important; }
        .swagger-ui .scheme-container * { color: rgb(31, 121, 204) !important; }
        
        /* Operation blocks */
        .swagger-ui .opblock { background-color: #252526 !important; border-color: #3e3e42 !important; }
        .swagger-ui .opblock * { color: #d4d4d4 !important; }
        .swagger-ui .opblock.opblock-get { border-color: #4ec9b0 !important; background-color: #1e3a3a !important; }
        .swagger-ui .opblock.opblock-post { border-color: #569cd6 !important; background-color: #1e2a3a !important; }
        .swagger-ui .opblock.opblock-put { border-color: #dcdcaa !important; background-color: #3a3a1e !important; }
        .swagger-ui .opblock.opblock-delete { border-color: #f48771 !important; background-color: #3a1e1e !important; }
        .swagger-ui .opblock-tag { color:rgb(255, 255, 255) !important; font-weight: bold !important; }
        .swagger-ui .opblock-tag:hover { color: #6ed4c0 !important; }
        .swagger-ui .opblock-summary-method { color: #ffffff !important; font-weight: bold !important; }
        .swagger-ui .opblock-body { background-color: #252526 !important; }
        .swagger-ui .opblock-section { background-color: #252526 !important; }
        .swagger-ui .opblock-section-header { background-color: #2d2d2d !important; color: #d4d4d4 !important; }
        
        /* Parameters */
        .swagger-ui .parameters-container { background-color: #252526 !important; }
        .swagger-ui .parameter { background-color: #2d2d2d !important; border-color: #3e3e42 !important; }
        .swagger-ui .parameter__name { color: #9cdcfe !important; font-weight: bold !important; }
        .swagger-ui .parameter__type { color: #ce9178 !important; }
        .swagger-ui .parameter__in { color: #ce9178 !important; background-color: #3c3c3c !important; }
        .swagger-ui .parameter__required { color: #f48771 !important; }
        
        /* Tables */
        .swagger-ui .table-container { background-color: #252526 !important; }
        .swagger-ui .table-container table { background-color: #252526 !important; }
        .swagger-ui .table-container table thead { background-color: #2d2d2d !important; }
        .swagger-ui .table-container table thead th { color: #d4d4d4 !important; background-color: #2d2d2d !important; }
        .swagger-ui .table-container table tbody td { color: #d4d4d4 !important; background-color: #252526 !important; }
        .swagger-ui .table-container table tbody tr:nth-child(even) { background-color: #2d2d2d !important; }
        .swagger-ui .table-container table tbody tr:nth-child(even) td { background-color: #2d2d2d !important; }
        
        /* Responses */
        .swagger-ui .responses-wrapper { background-color: #252526 !important; }
        .swagger-ui .response-col_status { color: #4ec9b0 !important; font-weight: bold !important; }
        .swagger-ui .response-content-type { color: #9cdcfe !important; }
        .swagger-ui .response-content-type select { background-color: #3c3c3c !important; color: #d4d4d4 !important; }
        .swagger-ui .response-body { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        .swagger-ui .response-body pre, .swagger-ui .response-body code { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        .swagger-ui .response-header { background-color: #2d2d2d !important; color: #d4d4d4 !important; }
        
        /* Request body */
        .swagger-ui .request-body { background-color: #252526 !important; }
        .swagger-ui .request-body-content-type { color: #9cdcfe !important; }
        .swagger-ui .request-body-content-type select { background-color: #3c3c3c !important; color: #d4d4d4 !important; }
        .swagger-ui .body-param-content textarea { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        .swagger-ui .curl-command { background-color: #1e1e1e !important; color: #d4d4d4 !important; }
        .swagger-ui .request-url { background-color: #1e1e1e !important; color: #9cdcfe !important; }
        
        /* Inputs and buttons */
        .swagger-ui input[type=text], .swagger-ui input[type=password], .swagger-ui input[type=number], .swagger-ui textarea { 
            background-color: #3c3c3c !important; color: #d4d4d4 !important; border-color: #3e3e42 !important; 
        }
        .swagger-ui input::placeholder { color: rgb(76, 125, 153) !important; }
        .swagger-ui select { background-color: #3c3c3c !important; color: #d4d4d4 !important; border-color: #3e3e42 !important; }
        .swagger-ui select option { background-color: #3c3c3c !important; color: #d4d4d4 !important; }
        .swagger-ui .btn { background-color: #0e639c !important; color: #ffffff !important; border: none !important; }
        .swagger-ui .btn:hover { background-color: #1177bb !important; }
        .swagger-ui .btn.cancel, .swagger-ui .btn.clear { background-color: #3c3c3c !important; color: #d4d4d4 !important; }
        
        /* Servers */
        .swagger-ui .servers { background-color: #252526 !important; }
        .swagger-ui .servers * { color: #d4d4d4 !important; }
        .swagger-ui .servers select { background-color: #3c3c3c !important; color: #d4d4d4 !important; }
        
        /* Markdown */
        .swagger-ui .markdown p { color: #d4d4d4 !important; }
        .swagger-ui .markdown code { background-color: #3c3c3c !important; color: #ce9178 !important; }
        .swagger-ui .markdown pre { background-color: #252526 !important; color: #d4d4d4 !important; }
        
        /* Schemas section */
        .swagger-ui .schemas, .swagger-ui .schemas-container, .swagger-ui .models, .swagger-ui .section-models { 
            background-color: #1e1e1e !important; color: #ffffff !important; 
        }
        .swagger-ui .section-models .section-title { color: #4ec9b0 !important; font-weight: bold !important; font-size: 18px !important; }
        
        /* Schema list items - improved UX */
        .swagger-ui .model-box-control { 
            background: linear-gradient(135deg, #2d2d2d 0%, #252526 100%) !important;
            background-color: #2d2d2d !important;
            color: #ffffff !important; 
            border: 1px solid #3e3e42 !important;
            border-left: 3px solid #4ec9b0 !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            margin-bottom: 8px !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 8px !important;
        }
        .swagger-ui .model-box-control:hover { 
            background: linear-gradient(135deg, #3c3c3c 0%, #2d2d2d 100%) !important;
            background-color: #3c3c3c !important;
            border-color: #4ec9b0 !important;
            border-left-color: #6ed4c0 !important;
            box-shadow: 0 2px 8px rgba(78, 201, 176, 0.2) !important;
            transform: translateY(-1px) !important;
        }
        .swagger-ui .model-box-control .model-title,
        .swagger-ui .model-box-control .model-title__text,
        .swagger-ui .model-box-control span:first-child {
            color: #4ec9b0 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
        }
        .swagger-ui .model-box-control:hover .model-title,
        .swagger-ui .model-box-control:hover .model-title__text {
            color: #6ed4c0 !important;
        }
        .swagger-ui .model-box-control a,
        .swagger-ui .model-box-control .expand-methods {
            color: #9cdcfe !important;
            font-size: 13px !important;
            text-decoration: none !important;
        }
        .swagger-ui .model-box-control a:hover {
            color: #6ed4c0 !important;
            background-color: rgba(78, 201, 176, 0.1) !important;
        }
        .swagger-ui .model-box-control svg {
            fill: #9cdcfe !important;
            transition: all 0.2s ease !important;
        }
        .swagger-ui .model-box-control:hover svg {
            fill: #4ec9b0 !important;
            transform: translateX(2px) !important;
        }
        
        /* Expanded schema content */
        .swagger-ui .model-box { 
            background-color: #1e1e1e !important; 
            color: #ffffff !important; 
            border: 1px solid #3e3e42 !important;
        }
        .swagger-ui .model-box * { color: #ffffff !important; }
        .swagger-ui .model-title { color: #4ec9b0 !important; font-weight: bold !important; }
        .swagger-ui .model-title__text { color: #4ec9b0 !important; }
        .swagger-ui .model-toggle { 
            background-color: #3c3c3c !important; 
            color: #ffffff !important; 
            border: 1px solid #4ec9b0 !important;
        }
        .swagger-ui .model-toggle:hover { 
            background-color: #4ec9b0 !important; 
            color: #1e1e1e !important;
        }
        .swagger-ui .model-toggle svg { fill: #ffffff !important; }
        .swagger-ui .model-toggle:hover svg { fill: #1e1e1e !important; }
        .swagger-ui .model-toggle.expanded svg { fill: #4ec9b0 !important; }
        .swagger-ui .model-jump-to-path { color: #9cdcfe !important; font-weight: bold !important; }
        .swagger-ui .model-jump-to-path:hover { color: #6ed4c0 !important; text-decoration: underline !important; }
        
        /* Schema properties */
        .swagger-ui .prop { background-color: #252526 !important; color: #ffffff !important; border-color: #3e3e42 !important; }
        .swagger-ui .prop:hover { background-color: #2d2d2d !important; border-color: #4ec9b0 !important; }
        .swagger-ui .prop-row { background-color: #252526 !important; color: #ffffff !important; }
        .swagger-ui .prop-row:hover { background-color: #2d2d2d !important; }
        .swagger-ui .prop-name { color: #9cdcfe !important; font-weight: bold !important; }
        .swagger-ui .prop-type { color: #ce9178 !important; font-weight: bold !important; }
        .swagger-ui .prop-format { color: #ce9178 !important; }
        .swagger-ui .prop-description { color: #d4d4d4 !important; }
        .swagger-ui .prop-required { color: #f48771 !important; font-weight: bold !important; }
        .swagger-ui .prop-deprecated { color: #f48771 !important; }
        
        /* Model content */
        .swagger-ui .model { background-color: #252526 !important; color: #ffffff !important; }
        .swagger-ui .model * { color: #ffffff !important; }
        .swagger-ui .model-box .model { 
            background-color: #252526 !important; 
            border-left: 2px solid #4ec9b0 !important;
            padding-left: 10px !important;
        }
        .swagger-ui .model-example { 
            background-color: #1e1e1e !important; 
            color: #ffffff !important; 
            border: 1px solid #3e3e42 !important;
        }
        .swagger-ui .model-example * { color: #ffffff !important; }
        .swagger-ui .model-box pre,
        .swagger-ui .model-box code {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            border: 1px solid #3e3e42 !important;
        }
        .swagger-ui .model-box pre *,
        .swagger-ui .model-box code * {
            color: #ffffff !important;
        }
        .swagger-ui .model-box textarea {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            border: 1px solid #3e3e42 !important;
        }
        .swagger-ui .renderedMarkdown { background-color: #252526 !important; color: #ffffff !important; }
        .swagger-ui .renderedMarkdown * { color: #ffffff !important; }
        .swagger-ui .renderedMarkdown code { background-color: #2d2d2d !important; color: #ce9178 !important; padding: 2px 4px !important; border-radius: 3px !important; }
        
        /* Override white backgrounds and grey text in schemas */
        .swagger-ui .model-box [style*="background-color: white"],
        .swagger-ui .model-box [style*="background-color: #fff"],
        .swagger-ui .model-box [style*="background-color: #ffffff"],
        .swagger-ui .model-box [style*="background: white"],
        .swagger-ui .model-box [style*="background: #fff"],
        .swagger-ui .model-box [style*="background: #ffffff"] {
            background-color: #1e1e1e !important;
            background: #1e1e1e !important;
        }
        .swagger-ui .model-box [style*="color: gray"],
        .swagger-ui .model-box [style*="color: grey"],
        .swagger-ui .model-box [style*="color: #808080"] {
            color: #ffffff !important;
        }
        .swagger-ui .model-box table {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }
        .swagger-ui .model-box table td,
        .swagger-ui .model-box table th {
            background-color: #252526 !important;
            color: #ffffff !important;
            border-color: #3e3e42 !important;
        }
        .swagger-ui .model-box table tr:nth-child(even) td {
            background-color: #2d2d2d !important;
        }
        
        /* Theme toggle button */
        #theme-toggle-btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; 
            color: white !important; 
            border: none !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        #theme-toggle-btn:hover { 
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important; 
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
        }
    `;
}

// Add toggle button
function addThemeToggle() {
    if (document.getElementById('theme-toggle-btn')) {
        return;
    }
    
    const toggleBtn = document.createElement('button');
    toggleBtn.id = 'theme-toggle-btn';
    toggleBtn.style.cssText = 'position: fixed; top: 15px; right: 15px; z-index: 10000; padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 13px; font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;';
    toggleBtn.onclick = toggleTheme;
    
    toggleBtn.onmouseenter = function() {
        this.style.background = 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)';
        this.style.transform = 'translateY(-2px)';
        this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)';
    };
    toggleBtn.onmouseleave = function() {
        this.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
    };
    
    toggleBtn.onmousedown = function() {
        this.style.transform = 'translateY(0) scale(0.98)';
    };
    toggleBtn.onmouseup = function() {
        this.style.transform = 'translateY(-2px)';
    };
    
    if (document.body) {
        document.body.appendChild(toggleBtn);
        const theme = getTheme();
        if (theme === DARK_THEME) {
            toggleBtn.innerHTML = '<span style="font-size: 16px;">☀️</span><span>Light</span>';
            toggleBtn.title = 'Switch to Light Mode';
        } else {
            toggleBtn.innerHTML = '<span style="font-size: 16px;">🌙</span><span>Dark</span>';
            toggleBtn.title = 'Switch to Dark Mode';
        }
    }
}

// Initialize theme and button
function initTheme() {
    const theme = getTheme();
    applyTheme(theme);
    
    let attempts = 0;
    const maxAttempts = 10;
    const tryAddButton = setInterval(function() {
        attempts++;
        if (document.body && document.getElementById('theme-toggle-btn') === null) {
            addThemeToggle();
        }
        if (document.getElementById('theme-toggle-btn') || attempts >= maxAttempts) {
            clearInterval(tryAddButton);
        }
    }, 100);
    
    if (theme === DARK_THEME) {
        const observer = new MutationObserver(function(mutations) {
            forceSchemaDarkTheme();
        });
        
        const observeSwagger = setInterval(function() {
            const swaggerUI = document.querySelector('.swagger-ui');
            if (swaggerUI) {
                observer.observe(swaggerUI, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['class', 'style']
                });
                clearInterval(observeSwagger);
            }
        }, 100);
        
        document.addEventListener('click', function(e) {
            if (e.target.closest('.model-box-control, .model-toggle')) {
                setTimeout(forceSchemaDarkTheme, 100);
                setTimeout(forceSchemaDarkTheme, 300);
            }
        });
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}

window.addEventListener('load', function() {
    if (!document.getElementById('theme-toggle-btn')) {
        addThemeToggle();
    }
});
