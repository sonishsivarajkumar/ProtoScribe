# API Reference Overview

Complete reference documentation for ProtoScribe's REST API endpoints, data models, and integration patterns.

## Base URL

```
Development: http://localhost:8000
Production: https://api.protoscribe.app
```

## Authentication

ProtoScribe currently operates in development mode without authentication. Production deployment will include:

- **API Key Authentication**: For programmatic access
- **OAuth 2.0**: For user authentication
- **JWT Tokens**: For session management

## API Versioning

ProtoScribe API uses URL path versioning:

```
/api/v1/     # Current stable version
/api/v2/     # Future version (when available)
```

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "PROTOCOL_NOT_FOUND",
    "message": "Protocol with ID 'proto_123' not found",
    "details": {
      "protocol_id": "proto_123",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  }
}
```

## Status Codes

ProtoScribe uses standard HTTP status codes:

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted for processing |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict |
| 413 | Payload Too Large | File too large |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

## Rate Limiting

API endpoints are rate limited to ensure fair usage:

| Endpoint Type | Rate Limit | Window |
|---------------|------------|--------|
| Protocol Upload | 5 requests | 1 minute |
| Analysis Requests | 10 requests | 1 minute |
| General API | 100 requests | 1 minute |
| Download/Export | 20 requests | 1 hour |

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1642248600
```

## Pagination

List endpoints support pagination with consistent parameters:

### Request Parameters
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 20, max: 100)

### Response Format
```json
{
  "data": [...],
  "pagination": {
    "skip": 0,
    "limit": 20,
    "total": 150,
    "has_next": true,
    "has_previous": false
  }
}
```

## Filtering and Sorting

Many endpoints support filtering and sorting:

### Filtering
```http
GET /api/protocols/?status=ready&created_after=2024-01-01
```

### Sorting
```http
GET /api/protocols/?sort=created_at&order=desc
```

Common filter parameters:
- `status`: Filter by resource status
- `created_after`: Filter by creation date
- `created_before`: Filter by creation date
- `search`: Text search in relevant fields

Common sort fields:
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `title`: Alphabetical by title
- `score`: By analysis score (where applicable)

## Error Handling

ProtoScribe provides detailed error information to help with debugging:

### Validation Errors
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field_errors": {
        "title": ["This field is required"],
        "file": ["File size exceeds maximum limit of 50MB"]
      }
    }
  }
}
```

### Service Errors
```json
{
  "success": false,
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "AI analysis service is temporarily unavailable",
    "details": {
      "provider": "openai",
      "retry_after": 300,
      "fallback_available": true
    }
  }
}
```

## Interactive Documentation

ProtoScribe provides interactive API documentation:

- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Spec**: Available at `/openapi.json`

These interfaces allow you to:
- Explore all available endpoints
- View request/response schemas
- Test API calls directly in the browser
- Download API specifications

## SDK and Client Libraries

### Python SDK
```python
# Install the ProtoScribe Python SDK
pip install protoscribe-sdk

# Usage example
from protoscribe import ProtoScribeClient

client = ProtoScribeClient(api_url="http://localhost:8000")

# Upload and analyze a protocol
protocol = client.upload_protocol("protocol.pdf", title="My Trial")
analysis = client.analyze_protocol(protocol.id, analysis_type="comprehensive")
```

### JavaScript/TypeScript SDK
```typescript
// Install the ProtoScribe JavaScript SDK
npm install @protoscribe/sdk

// Usage example
import { ProtoScribeClient } from '@protoscribe/sdk';

const client = new ProtoScribeClient({
  apiUrl: 'http://localhost:8000'
});

// Upload and analyze a protocol
const protocol = await client.uploadProtocol(file, { title: 'My Trial' });
const analysis = await client.analyzeProtocol(protocol.id, {
  analysisType: 'comprehensive'
});
```

## Webhooks (Future Feature)

ProtoScribe will support webhooks for real-time notifications:

### Event Types
- `protocol.uploaded`: New protocol uploaded
- `analysis.completed`: Analysis finished
- `analysis.failed`: Analysis failed
- `export.ready`: Export file ready for download

### Webhook Payload
```json
{
  "event_type": "analysis.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "protocol_id": "proto_123",
    "analysis_id": "analysis_456",
    "status": "completed",
    "overall_score": 85
  }
}
```

## API Changelog

### Version 1.0.0 (Current)
- Initial API release
- Protocol management endpoints
- AI analysis capabilities
- Export functionality
- Interactive documentation

### Planned Features
- User authentication and authorization
- Webhook support
- Advanced filtering and search
- Bulk operations
- Real-time collaboration APIs
- Integration with external systems

## Best Practices

### Request Optimization
1. **Use appropriate HTTP methods** (GET, POST, PUT, DELETE)
2. **Include proper headers** (Content-Type, Accept)
3. **Handle errors gracefully** with proper error checking
4. **Implement retry logic** for transient failures
5. **Cache responses** when appropriate

### Security
1. **Validate all inputs** before sending to API
2. **Use HTTPS** in production environments
3. **Implement proper authentication** when available
4. **Don't expose sensitive data** in URLs or logs
5. **Follow rate limiting guidelines**

### Performance
1. **Use pagination** for large datasets
2. **Implement request caching** where appropriate
3. **Batch requests** when possible
4. **Monitor API usage** and optimize accordingly
5. **Use appropriate timeout values**

## Support and Feedback

For API support and feedback:

- **Documentation Issues**: Open an issue on GitHub
- **Bug Reports**: Use the GitHub issue tracker
- **Feature Requests**: Submit via GitHub discussions
- **General Questions**: Check our FAQ or community forums

## Related Resources

- [Getting Started Guide](../getting-started/quick-start.md)
- [Backend API Development](../developer-guide/backend-api.md)
- [Frontend Integration](../developer-guide/frontend.md)
- [Contributing Guidelines](../contributing/development-setup.md)
