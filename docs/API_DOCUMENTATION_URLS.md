# 📚 EveryCRED DCS API Documentation URLs

This document provides a comprehensive list of all available documentation URLs when running your FastAPI server.

## 🚀 Quick Start

Start your server with:
```bash
poetry run python asgi.py --env local --debug
```

Default server URL: `http://localhost:8008`

## 🌐 Main Gateway

### Landing Page & Navigation
- **🏠 API Hub**: [http://localhost:8008/](http://localhost:8008/)
  - Beautiful landing page with links to all documentation
  - Visual navigation to all API versions
  - Status indicators and quick access

### Gateway Endpoints
- **❤️ Health Check**: [http://localhost:8008/health](http://localhost:8008/health)
- **📊 API Status**: [http://localhost:8008/api/status](http://localhost:8008/api/status)
- **📚 Gateway Docs**: [http://localhost:8008/docs](http://localhost:8008/docs)
- **📖 Gateway ReDoc**: [http://localhost:8008/redoc](http://localhost:8008/redoc)

## 🔐 API Version 1 (Production Ready)

### Documentation
- **📚 Swagger UI**: [http://localhost:8008/api/v1/docs](http://localhost:8008/api/v1/docs)
- **📖 ReDoc**: [http://localhost:8008/api/v1/redoc](http://localhost:8008/api/v1/redoc)
- **⚙️ OpenAPI Schema**: [http://localhost:8008/api/v1/openapi.json](http://localhost:8008/api/v1/openapi.json)

### Available Endpoints
- **🔐 User Registration**: `POST /api/v1/auth/register`
- **🔑 User Login**: `POST /api/v1/auth/login`
- **❤️ Health Check**: `GET /api/v1/health`

### Features
- ✅ Argon2id password hashing
- ✅ User authentication system
- ✅ Input validation & sanitization
- ✅ Security headers middleware
- ✅ Rate limiting protection

## 🚀 API Version 2 (In Development)

### Documentation
- **📚 Swagger UI**: [http://localhost:8008/api/v2/docs](http://localhost:8008/api/v2/docs)
- **📖 ReDoc**: [http://localhost:8008/api/v2/redoc](http://localhost:8008/api/v2/redoc)
- **⚙️ OpenAPI Schema**: [http://localhost:8008/api/v2/openapi.json](http://localhost:8008/api/v2/openapi.json)

### Available Endpoints
- **❤️ Health Check**: `GET /api/v2/health`

### Planned Features
- 🔮 Enhanced authentication mechanisms
- 🔮 Advanced user management
- 🔮 Real-time notifications
- 🔮 Advanced analytics

## 🛠️ Development URLs

### Environment-Specific Behavior
- **Local/Dev**: All documentation URLs are accessible
- **Production**: Documentation URLs are disabled for security

### Custom Configuration
Set these environment variables to customize URLs:
```bash
SERVER_HOST=localhost    # Default: localhost
SERVER_PORT=8008        # Default: 8008
BASE_URL=http://localhost:8008  # Used in API status responses
ENV=local               # Options: local, dev, prod
```

## 📱 Interactive Testing

### Using Swagger UI
1. Navigate to any `/docs` URL
2. Click "Try it out" on any endpoint
3. Fill in parameters and click "Execute"
4. View the response directly in the browser

### Using ReDoc
1. Navigate to any `/redoc` URL
2. Browse the comprehensive API documentation
3. View request/response schemas
4. Copy curl commands for testing

## 🔧 API Client Integration

### OpenAPI Schema URLs
Use these URLs to generate client SDKs:
- **v1 Schema**: `http://localhost:8008/api/v1/openapi.json`
- **v2 Schema**: `http://localhost:8008/api/v2/openapi.json`

### Example Client Generation
```bash
# Generate Python client for API v1
openapi-generator generate -i http://localhost:8008/api/v1/openapi.json -g python -o ./client-v1

# Generate TypeScript client for API v2
openapi-generator generate -i http://localhost:8008/api/v2/openapi.json -g typescript-axios -o ./client-v2
```

## 🎨 UI Customization

### Swagger UI Features
- 🌙 Dark theme (Obsidian)
- 🔍 Filtering and search
- 📋 Alphabetical sorting
- 🔐 OAuth2 integration ready
- ⏱️ Request duration display

### Custom Styling
The documentation includes:
- Custom logo integration
- Branded color schemes
- Responsive design
- Modern UI components

## 🔒 Security Notes

### Production Deployment
- Documentation URLs are automatically disabled in production
- Only API endpoints remain accessible
- Health and status endpoints remain available

### Development Safety
- CORS is configured for development
- Security headers are applied
- Rate limiting is active
- Input validation is enforced

## 📞 Support & Troubleshooting

### Common Issues
1. **Port already in use**: Change `SERVER_PORT` in your `.env` file
2. **Module not found**: Run `poetry install` to install dependencies
3. **Permission denied**: Check firewall settings for the specified port

### Health Check
Always verify your server is running by visiting:
- [http://localhost:8008/health](http://localhost:8008/health)

This should return a JSON response with service status and available API links.

---

**📝 Note**: This documentation is automatically updated when you modify your API structure. The URLs will adapt to your server configuration and environment settings.