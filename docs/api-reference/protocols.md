# Protocol Endpoints

Complete reference for all protocol management API endpoints including upload, retrieval, update, and deletion operations.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/protocols/` | List all protocols |
| POST | `/api/protocols/` | Upload new protocol |
| GET | `/api/protocols/{id}` | Get specific protocol |
| PUT | `/api/protocols/{id}` | Update protocol |
| DELETE | `/api/protocols/{id}` | Delete protocol |
| GET | `/api/protocols/{id}/summary` | Get protocol summary |
| GET | `/api/protocols/{id}/metadata` | Get protocol metadata |
| POST | `/api/protocols/{id}/versions` | Create new version |
| GET | `/api/protocols/{id}/versions` | List protocol versions |

## List Protocols

Retrieve a paginated list of all protocols.

### Request
```http
GET /api/protocols/
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | integer | 0 | Number of records to skip |
| `limit` | integer | 20 | Maximum records to return (max: 100) |
| `status` | string | - | Filter by status (`processing`, `ready`, `error`) |
| `search` | string | - | Search in title and description |
| `created_after` | string | - | Filter by creation date (ISO format) |
| `created_before` | string | - | Filter by creation date (ISO format) |
| `sort` | string | `created_at` | Sort field (`created_at`, `title`, `updated_at`) |
| `order` | string | `desc` | Sort order (`asc`, `desc`) |

### Example Request
```bash
curl -X GET "http://localhost:8000/api/protocols/?limit=10&status=ready&sort=title&order=asc" \
  -H "Accept: application/json"
```

### Response
```json
{
  "protocols": [
    {
      "id": "proto_abc123",
      "title": "Phase II Oncology Trial",
      "description": "Randomized controlled trial for new cancer therapy",
      "status": "ready",
      "file_size": 2048576,
      "metadata": {
        "pages": 45,
        "words": 12500,
        "sections": 12,
        "file_type": "pdf"
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:45:00Z"
    }
  ],
  "pagination": {
    "skip": 0,
    "limit": 10,
    "total": 25,
    "has_next": true,
    "has_previous": false
  }
}
```

## Upload Protocol

Upload a new clinical trial protocol document for analysis.

### Request
```http
POST /api/protocols/
Content-Type: multipart/form-data
```

### Request Body (Form Data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Protocol document (PDF, DOCX, TXT, MD) |
| `title` | string | Yes | Protocol title (max: 255 chars) |
| `description` | string | No | Protocol description (max: 1000 chars) |

### File Requirements
- **Maximum size**: 50MB
- **Supported formats**: PDF, DOCX, TXT, Markdown
- **Content**: Must be searchable text (not scanned images)

### Example Request
```bash
curl -X POST "http://localhost:8000/api/protocols/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@protocol.pdf" \
  -F "title=Phase II Oncology Trial" \
  -F "description=Randomized controlled trial for new cancer therapy"
```

### Response
```json
{
  "id": "proto_abc123",
  "title": "Phase II Oncology Trial",
  "description": "Randomized controlled trial for new cancer therapy",
  "status": "processing",
  "file_size": 2048576,
  "metadata": {
    "original_filename": "protocol.pdf",
    "file_type": "pdf",
    "upload_timestamp": "2024-01-15T10:30:00Z"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Responses

#### File Too Large
```json
{
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "File size exceeds maximum limit of 50MB",
    "details": {
      "file_size": 52428800,
      "max_size": 52428800
    }
  }
}
```

#### Unsupported Format
```json
{
  "error": {
    "code": "UNSUPPORTED_FORMAT",
    "message": "File format not supported",
    "details": {
      "provided_type": "image/jpeg",
      "supported_types": ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "text/markdown"]
    }
  }
}
```

## Get Protocol

Retrieve a specific protocol by ID.

### Request
```http
GET /api/protocols/{protocol_id}
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `protocol_id` | string | Unique protocol identifier |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_content` | boolean | false | Include full protocol text content |
| `include_metadata` | boolean | true | Include protocol metadata |

### Example Request
```bash
curl -X GET "http://localhost:8000/api/protocols/proto_abc123?include_content=true" \
  -H "Accept: application/json"
```

### Response
```json
{
  "id": "proto_abc123",
  "title": "Phase II Oncology Trial",
  "description": "Randomized controlled trial for new cancer therapy",
  "content": "PROTOCOL TITLE: Phase II Randomized Controlled Trial...",
  "status": "ready",
  "file_size": 2048576,
  "metadata": {
    "pages": 45,
    "words": 12500,
    "sections": 12,
    "file_type": "pdf",
    "original_filename": "protocol.pdf",
    "processing_time": 45.2,
    "extracted_sections": [
      "Title Page",
      "Protocol Summary",
      "Background and Rationale",
      "Objectives",
      "Study Design",
      "Study Population",
      "Interventions",
      "Outcomes",
      "Statistical Analysis",
      "Ethical Considerations",
      "Data Management",
      "References"
    ]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:45:00Z"
}
```

### Error Response
```json
{
  "error": {
    "code": "PROTOCOL_NOT_FOUND",
    "message": "Protocol with ID 'proto_abc123' not found",
    "details": {
      "protocol_id": "proto_abc123"
    }
  }
}
```

## Update Protocol

Update an existing protocol's metadata or content.

### Request
```http
PUT /api/protocols/{protocol_id}
Content-Type: application/json
```

### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Protocol title (optional) |
| `description` | string | Protocol description (optional) |
| `content` | string | Protocol content (optional) |

### Example Request
```bash
curl -X PUT "http://localhost:8000/api/protocols/proto_abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Phase II Oncology Trial",
    "description": "Updated description with additional details"
  }'
```

### Response
```json
{
  "id": "proto_abc123",
  "title": "Updated Phase II Oncology Trial",
  "description": "Updated description with additional details",
  "status": "ready",
  "file_size": 2048576,
  "metadata": {
    "pages": 45,
    "words": 12500,
    "sections": 12,
    "file_type": "pdf",
    "last_modified_by": "user_123",
    "modification_history": [
      {
        "timestamp": "2024-01-15T11:00:00Z",
        "changes": ["title", "description"],
        "modified_by": "user_123"
      }
    ]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

## Delete Protocol

Delete a protocol and all associated data.

### Request
```http
DELETE /api/protocols/{protocol_id}
```

### Example Request
```bash
curl -X DELETE "http://localhost:8000/api/protocols/proto_abc123"
```

### Response
```json
{
  "message": "Protocol deleted successfully",
  "protocol_id": "proto_abc123",
  "deleted_at": "2024-01-15T11:30:00Z"
}
```

### Warning
!!! warning "Destructive Operation"
    Deleting a protocol will permanently remove:
    - The protocol document and content
    - All analysis results and suggestions
    - Version history
    - Export files
    This operation cannot be undone.

## Get Protocol Summary

Get a concise summary of the protocol including key metadata and analysis overview.

### Request
```http
GET /api/protocols/{protocol_id}/summary
```

### Example Request
```bash
curl -X GET "http://localhost:8000/api/protocols/proto_abc123/summary" \
  -H "Accept: application/json"
```

### Response
```json
{
  "protocol_id": "proto_abc123",
  "title": "Phase II Oncology Trial",
  "summary": {
    "study_type": "Randomized Controlled Trial",
    "phase": "II",
    "therapeutic_area": "Oncology",
    "population": "Advanced cancer patients",
    "intervention": "Novel targeted therapy vs. standard care",
    "primary_endpoint": "Progression-free survival",
    "secondary_endpoints": [
      "Overall survival",
      "Response rate",
      "Safety and tolerability"
    ],
    "sample_size": 200,
    "study_duration": "24 months",
    "enrollment_period": "18 months"
  },
  "compliance_overview": {
    "overall_score": 85,
    "consort_score": 88,
    "spirit_score": 82,
    "last_analysis": "2024-01-15T10:45:00Z",
    "analysis_count": 3,
    "status": "compliant",
    "critical_issues": 0,
    "improvement_opportunities": 5
  },
  "key_strengths": [
    "Well-defined primary endpoint",
    "Appropriate statistical methodology",
    "Clear inclusion/exclusion criteria",
    "Comprehensive safety monitoring plan"
  ],
  "areas_for_improvement": [
    "Sample size justification needs more detail",
    "Interim analysis procedures could be clearer",
    "Data monitoring committee responsibilities undefined"
  ]
}
```

## Get Protocol Metadata

Retrieve detailed metadata about the protocol without the full content.

### Request
```http
GET /api/protocols/{protocol_id}/metadata
```

### Response
```json
{
  "protocol_id": "proto_abc123",
  "file_metadata": {
    "original_filename": "protocol.pdf",
    "file_type": "pdf",
    "file_size": 2048576,
    "pages": 45,
    "words": 12500,
    "characters": 89750,
    "upload_timestamp": "2024-01-15T10:30:00Z",
    "processing_time": 45.2
  },
  "content_analysis": {
    "sections": 12,
    "tables": 8,
    "figures": 15,
    "references": 67,
    "appendices": 3,
    "readability_score": 45.2,
    "language": "en",
    "technical_terms": 234
  },
  "structure_analysis": {
    "has_title_page": true,
    "has_abstract": true,
    "has_objectives": true,
    "has_methodology": true,
    "has_statistical_plan": true,
    "has_ethics_section": true,
    "has_references": true,
    "missing_sections": []
  },
  "version_info": {
    "current_version": 1,
    "total_versions": 1,
    "last_modified": "2024-01-15T10:45:00Z",
    "creation_date": "2024-01-15T10:30:00Z"
  }
}
```

## Create Protocol Version

Create a new version of an existing protocol.

### Request
```http
POST /api/protocols/{protocol_id}/versions
Content-Type: application/json
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | Yes | Updated protocol content |
| `change_summary` | string | Yes | Summary of changes made |
| `version_notes` | string | No | Additional notes about this version |

### Example Request
```bash
curl -X POST "http://localhost:8000/api/protocols/proto_abc123/versions" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated protocol content with revised methodology...",
    "change_summary": "Updated sample size calculation and statistical analysis plan",
    "version_notes": "Incorporated feedback from statistical review"
  }'
```

### Response
```json
{
  "version_id": "version_def456",
  "protocol_id": "proto_abc123",
  "version_number": 2,
  "change_summary": "Updated sample size calculation and statistical analysis plan",
  "version_notes": "Incorporated feedback from statistical review",
  "created_at": "2024-01-15T12:00:00Z",
  "created_by": "user_123",
  "content_hash": "sha256:abc123...",
  "diff_summary": {
    "lines_added": 15,
    "lines_removed": 8,
    "lines_modified": 23,
    "sections_changed": ["Statistical Analysis", "Sample Size Calculation"]
  }
}
```

## List Protocol Versions

Get all versions of a protocol with change history.

### Request
```http
GET /api/protocols/{protocol_id}/versions
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_content` | boolean | false | Include full content for each version |
| `include_diff` | boolean | true | Include diff information between versions |

### Response
```json
{
  "protocol_id": "proto_abc123",
  "current_version": 2,
  "versions": [
    {
      "version_id": "version_def456",
      "version_number": 2,
      "change_summary": "Updated sample size calculation and statistical analysis plan",
      "created_at": "2024-01-15T12:00:00Z",
      "created_by": "user_123",
      "is_current": true,
      "diff_from_previous": {
        "lines_added": 15,
        "lines_removed": 8,
        "sections_changed": ["Statistical Analysis", "Sample Size Calculation"]
      }
    },
    {
      "version_id": "version_abc123",
      "version_number": 1,
      "change_summary": "Initial protocol version",
      "created_at": "2024-01-15T10:30:00Z",
      "created_by": "user_123",
      "is_current": false
    }
  ]
}
```

## Common Response Codes

| Status Code | Meaning | Common Scenarios |
|-------------|---------|------------------|
| 200 | OK | Successful GET, PUT operations |
| 201 | Created | Successful POST operations |
| 400 | Bad Request | Invalid request data, validation errors |
| 404 | Not Found | Protocol ID doesn't exist |
| 413 | Payload Too Large | File exceeds size limits |
| 415 | Unsupported Media Type | Invalid file format |
| 422 | Unprocessable Entity | Valid format but processing failed |

## Best Practices

### File Upload
1. **Check file size** before upload to avoid 413 errors
2. **Validate file format** on client side
3. **Provide progress feedback** for large uploads
4. **Handle upload failures** with retry logic

### Content Management
1. **Use descriptive titles** and descriptions
2. **Version your protocols** when making significant changes
3. **Include change summaries** for better tracking
4. **Backup important protocols** before major updates

### Performance
1. **Use `include_content=false`** when you don't need full text
2. **Implement pagination** for protocol lists
3. **Cache frequently accessed protocols**
4. **Use appropriate filters** to reduce response sizes

!!! tip "Protocol Organization"
    Use consistent naming conventions and detailed descriptions to make protocols easier to find and manage. Consider including study phase, therapeutic area, and version information in titles.

!!! warning "Data Loss Prevention"
    Always create protocol versions before making significant changes. The delete operation is permanent and cannot be undone.

!!! info "File Processing"
    Protocol files are processed asynchronously. Check the `status` field to determine when a protocol is ready for analysis. Processing typically takes 30-60 seconds depending on file size and complexity.
