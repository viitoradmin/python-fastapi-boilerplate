# Security Headers Guide

This document explains the different types of security headers used in the FastAPI application, their purposes, and when/how to use them.

## Overview

Security headers are HTTP response headers that help protect web applications from various attacks and vulnerabilities. They provide instructions to browsers on how to handle content and enforce security policies.

## Headers Implemented

### 1. Content-Security-Policy (CSP)

**Purpose**: Prevents Cross-Site Scripting (XSS) attacks by controlling which resources can be loaded and executed.

**Current Value**: Configured per environment (disabled in local/dev, enabled in prod)

**Common Directives**:
- `default-src`: Fallback for other fetch directives
- `script-src`: Controls which scripts can be executed
- `style-src`: Controls which stylesheets can be applied
- `img-src`: Controls which images can be loaded
- `connect-src`: Controls which URLs can be loaded via fetch, XMLHttpRequest, etc.
- `font-src`: Controls which fonts can be loaded
- `object-src`: Controls plugins like Flash
- `base-uri`: Restricts the URLs that can be used in `<base>` elements
- `form-action`: Restricts which URLs can be used as form submission targets
- `frame-ancestors`: Replaces X-Frame-Options, controls embedding

**When to Use**:
- **Always** in production environments
- When you need to prevent XSS attacks
- When you want to control resource loading
- For compliance with security standards (OWASP, PCI-DSS)

**Example**:
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';
```

**Note**: `unsafe-inline` should be avoided when possible. Use nonces or hashes instead.

---

### 2. Cross-Origin-Embedder-Policy (COEP)

**Purpose**: Prevents a document from loading cross-origin resources that don't explicitly grant permission.

**Current Value**: `require-corp`

**Possible Values**:
- `unsafe-none`: Default, allows all cross-origin resources
- `require-corp`: Requires resources to explicitly opt-in via Cross-Origin-Resource-Policy
- `credentialless`: Similar to require-corp but allows credentials to be omitted

**When to Use**:
- When using SharedArrayBuffer or other features requiring a secure context
- For enhanced isolation between origins
- When implementing advanced web features (WebAssembly, Web Workers)
- For defense-in-depth security

**Considerations**:
- Can break third-party resources that don't set proper CORS headers
- May require updating external resources to include `Cross-Origin-Resource-Policy: cross-origin`
- Often used together with COOP for Cross-Origin Isolation

**Example**:
```
Cross-Origin-Embedder-Policy: require-corp
```

---

### 3. Cross-Origin-Opener-Policy (COOP)

**Purpose**: Isolates the browsing context from other origins, preventing cross-origin attacks.

**Current Value**: `same-origin`

**Possible Values**:
- `unsafe-none`: Default, allows cross-origin window access
- `same-origin`: Only same-origin windows can access this window
- `same-origin-allow-popups`: Allows popups from same origin
- `restrict-properties`: Restricts access to window properties

**When to Use**:
- To prevent cross-origin window access attacks
- When using COEP for Cross-Origin Isolation
- To protect against Spectre-like attacks
- For enhanced privacy and security

**Example**:
```
Cross-Origin-Opener-Policy: same-origin
```

**Note**: Using `same-origin` can break OAuth flows and popup windows. Consider `same-origin-allow-popups` if needed.

---

### 4. Referrer-Policy

**Purpose**: Controls how much referrer information is sent with requests.

**Current Value**: `strict-origin-when-cross-origin`

**Possible Values**:
- `no-referrer`: Never send referrer
- `no-referrer-when-downgrade`: Default, send full referrer except when downgrading (HTTPS→HTTP)
- `origin`: Send only origin (scheme + host + port)
- `origin-when-cross-origin`: Send full referrer for same-origin, origin for cross-origin
- `same-origin`: Send referrer only for same-origin requests
- `strict-origin`: Send origin, but not when downgrading
- `strict-origin-when-cross-origin`: Send full referrer for same-origin, origin for cross-origin, nothing when downgrading
- `unsafe-url`: Always send full referrer (not recommended)

**When to Use**:
- To protect user privacy
- To prevent referrer leakage
- For GDPR/privacy compliance
- When you want to control what information is shared

**Example**:
```
Referrer-Policy: strict-origin-when-cross-origin
```

---

### 5. Strict-Transport-Security (HSTS)

**Purpose**: Forces browsers to use HTTPS for all future requests to the domain.

**Current Value**: `max-age=31556926; includeSubDomains`

**Directives**:
- `max-age`: Time in seconds to enforce HTTPS (31556926 = 1 year)
- `includeSubDomains`: Applies to all subdomains
- `preload`: Indicates eligibility for HSTS preload list

**When to Use**:
- **Always** in production with HTTPS
- To prevent protocol downgrade attacks
- To protect against man-in-the-middle attacks
- For compliance requirements

**Important**: 
- Only use with HTTPS (never with HTTP)
- Once set, browsers will remember it for the max-age duration
- Be careful with includeSubDomains - ensure all subdomains support HTTPS

**Example**:
```
Strict-Transport-Security: max-age=31556926; includeSubDomains
```

---

### 6. X-Content-Type-Options

**Purpose**: Prevents browsers from MIME-sniffing the content type.

**Current Value**: `nosniff`

**Possible Values**:
- `nosniff`: Prevents MIME type sniffing

**When to Use**:
- **Always** - it's a simple, safe header
- To prevent browsers from misinterpreting file types
- To prevent XSS attacks via MIME confusion
- For defense-in-depth

**Example**:
```
X-Content-Type-Options: nosniff
```

---

### 7. X-Frame-Options

**Purpose**: Prevents the page from being displayed in a frame/iframe (clickjacking protection).

**Current Value**: `DENY`

**Possible Values**:
- `DENY`: Never allow framing
- `SAMEORIGIN`: Allow framing only from same origin
- `ALLOW-FROM uri`: Allow framing from specific URI (deprecated, use CSP frame-ancestors instead)

**When to Use**:
- To prevent clickjacking attacks
- When you don't want your site embedded in iframes
- For sensitive operations (login, payment)

**Note**: Modern approach is to use CSP `frame-ancestors` directive instead, but X-Frame-Options is still widely supported.

**Example**:
```
X-Frame-Options: DENY
```

---

### 8. X-XSS-Protection

**Purpose**: Enables browser's built-in XSS filter (legacy header).

**Current Value**: `1; mode=block`

**Possible Values**:
- `0`: Disable filter
- `1`: Enable filter
- `1; mode=block`: Enable filter and block page if XSS detected

**When to Use**:
- For legacy browser support (Chrome, Edge removed support)
- As a fallback for older browsers
- Note: Modern browsers rely on CSP instead

**Important**: This header is deprecated in modern browsers. CSP is the recommended approach.

**Example**:
```
X-XSS-Protection: 1; mode=block
```

---

## Additional Security Headers (Not Currently Implemented)

### Permissions-Policy (formerly Feature-Policy)

**Purpose**: Controls which browser features and APIs can be used.

**Example**:
```
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**When to Use**:
- To restrict access to sensitive browser features
- To prevent unauthorized use of device capabilities
- For privacy protection

---

### Expect-CT

**Purpose**: Allows sites to opt in to Certificate Transparency reporting.

**Example**:
```
Expect-CT: max-age=86400, enforce, report-uri="https://example.com/report"
```

**Note**: Deprecated, replaced by Certificate Transparency in modern browsers.

---

### Public-Key-Pins (HPKP)

**Purpose**: Associates a cryptographic public key with a web server.

**Note**: **Deprecated and dangerous** - can cause site lockout. Do not use.

---

## Best Practices

1. **Start Strict, Relax as Needed**: Begin with strict policies and relax only when necessary
2. **Test Thoroughly**: Security headers can break functionality - test in staging first
3. **Monitor Reports**: Use CSP reporting to identify issues
4. **Keep Updated**: Security headers evolve - stay informed about best practices
5. **Environment-Specific**: Use different policies for dev/staging/production
6. **Documentation**: Document why each header is set and any exceptions

## Implementation Notes

- Headers are applied via middleware (`SecurityHeadersMiddleware`)
- CSP is conditionally enabled (prod only) to allow Swagger UI in development
- All headers are applied to all responses
- Headers can be customized per environment via configuration

## Testing Security Headers

Use these tools to test your security headers:
- [SecurityHeaders.com](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- Browser DevTools Network tab
- `curl -I` command

## References

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [Content Security Policy Reference](https://content-security-policy.com/)
- [CSP Evaluator](https://csp-evaluator.withgoogle.com/)

