# Protocol Upload

Learn how to upload and manage clinical trial protocols in ProtoScribe for AI-powered analysis and optimization.

## Supported Formats

ProtoScribe accepts protocols in multiple formats:

### Primary Formats
- **PDF**: Most common format for protocol documents
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text protocols
- **MD**: Markdown-formatted protocols

### File Requirements

!!! note "File Size Limits"
    - Maximum file size: 50MB
    - Recommended size: Under 10MB for optimal processing speed

!!! warning "Document Quality"
    - Ensure text is searchable (not scanned images)
    - Use clear formatting and structure
    - Include all protocol sections for comprehensive analysis

## Upload Methods

### 1. Web Interface Upload

The primary method for uploading protocols through the ProtoScribe web interface:

1. **Navigate to Editor**: Go to the Protocol Editor page
2. **Click Upload**: Use the "Upload Protocol" button
3. **Select File**: Choose your protocol document
4. **Review Upload**: Verify the document was processed correctly

```mermaid
graph LR
    A[Select File] --> B[Upload to Server]
    B --> C[Document Processing]
    C --> D[Text Extraction]
    D --> E[Protocol Ready]
```

### 2. API Upload

For programmatic access, use the REST API:

```bash
# Upload a protocol via API
curl -X POST "http://localhost:8000/api/protocols/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@protocol.pdf" \
  -F "title=My Clinical Trial Protocol" \
  -F "description=Phase II trial for new drug"
```

## Protocol Management

### Viewing Protocols

Once uploaded, protocols appear in your protocol library:

- **Title**: Protocol name or auto-generated title
- **Upload Date**: When the protocol was added
- **Status**: Processing status (Processing, Ready, Error)
- **Size**: File size information
- **Format**: Original document format

### Protocol Actions

For each protocol, you can:

- **📊 Analyze**: Run AI-powered compliance analysis
- **✏️ Edit**: Open in the interactive editor
- **📋 View**: Read the full protocol content
- **🗑️ Delete**: Remove from your library
- **📥 Download**: Get the original file

## Document Processing

### Text Extraction

ProtoScribe automatically extracts and processes text from uploaded documents:

1. **Format Detection**: Identifies document type and structure
2. **Content Extraction**: Extracts readable text content
3. **Structure Analysis**: Identifies sections, headers, and organization
4. **Metadata Extraction**: Captures document properties and information

### Processing Status

Monitor document processing through status indicators:

- **🔄 Processing**: Document is being analyzed
- **✅ Ready**: Ready for analysis and editing
- **❌ Error**: Processing failed (check file format)
- **⚠️ Warning**: Processed with issues (may affect analysis quality)

## Best Practices

### Document Preparation

To ensure optimal analysis results:

1. **Use Clear Structure**: Organize content with clear headings and sections
2. **Include All Sections**: Ensure complete protocol information
3. **Check Formatting**: Verify text is readable and properly formatted
4. **Review Content**: Ensure all critical information is present

### Common Issues and Solutions

#### Upload Failures

**Problem**: File upload fails or times out
**Solutions**:
- Check file size (must be under 50MB)
- Verify internet connection
- Try a different file format
- Refresh the page and retry

#### Poor Text Extraction

**Problem**: Extracted text is garbled or incomplete
**Solutions**:
- Ensure PDF is text-based (not scanned image)
- Try converting to DOCX format
- Check document permissions and encryption
- Use OCR software before upload if needed

#### Missing Content

**Problem**: Some protocol sections are missing after upload
**Solutions**:
- Verify complete document was uploaded
- Check for multi-file protocols (combine into single document)
- Ensure all pages are included in the PDF
- Review document structure and formatting

## Multiple Protocol Management

### Organizing Protocols

For research groups managing multiple protocols:

- **Naming Convention**: Use consistent, descriptive names
- **Version Control**: Include version numbers in titles
- **Study Phases**: Organize by trial phase or stage
- **Date Management**: Track upload and modification dates

### Batch Operations

ProtoScribe supports efficient management of multiple protocols:

- **Bulk Upload**: Upload multiple files simultaneously
- **Batch Analysis**: Run analysis on multiple protocols
- **Comparative Review**: Compare protocols side-by-side
- **Export Collections**: Generate reports for multiple protocols

## Security and Privacy

### Data Protection

ProtoScribe implements robust security measures:

- **Encrypted Storage**: All protocols are stored with encryption
- **Access Control**: User-specific protocol access
- **Audit Trails**: Track all protocol access and modifications
- **Secure Deletion**: Complete removal when protocols are deleted

### Compliance Considerations

When uploading protocols, consider:

- **IRB/Ethics Approval**: Ensure proper approvals for sharing
- **Intellectual Property**: Respect proprietary information
- **Patient Privacy**: Remove or redact sensitive information
- **Regulatory Requirements**: Follow applicable data protection laws

!!! tip "Workflow Tip"
    Create a standardized protocol template that includes all required CONSORT/SPIRIT elements to streamline the upload and analysis process.

!!! info "Need Help?"
    If you encounter issues with protocol upload, check the [troubleshooting guide](../getting-started/quick-start.md#troubleshooting) or contact support through our [GitHub repository](https://github.com/sonishsivarajkumar/ProtoScribe).
