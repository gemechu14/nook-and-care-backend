# File and Image Storage in Database

The backend now supports storing images and files directly in the PostgreSQL database (as binary data) instead of using external URLs or file systems.

## Features

- **Binary Storage**: Images are stored as `BYTEA` (PostgreSQL) or `BLOB` (SQLite) in the database
- **Metadata Support**: Filename, content type, and file size are stored alongside the binary data
- **URL Fallback**: Still supports external URLs for images hosted on CDNs
- **Base64 API**: API accepts base64-encoded image data for easy integration
- **File Upload**: Direct file upload endpoint using multipart/form-data

## Database Schema

The `listing_images` table now includes:

- `image_data` (BYTEA/BLOB): Binary image data
- `image_url` (TEXT, optional): External URL (for CDN-hosted images)
- `filename` (TEXT, optional): Original filename
- `content_type` (TEXT, optional): MIME type (e.g., "image/jpeg")
- `file_size` (INTEGER, optional): Size in bytes

## API Endpoints

### Upload Image File

```bash
POST /api/v1/listing-images/upload
Content-Type: multipart/form-data

Form fields:
- listing_id: UUID
- file: File (image file)
- display_order: int (optional, default: 0)
- is_primary: bool (optional, default: false)
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/v1/listing-images/upload" \
  -F "listing_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "file=@/path/to/image.jpg" \
  -F "display_order=0" \
  -F "is_primary=true"
```

### Create Image with Base64

```bash
POST /api/v1/listing-images/
Content-Type: application/json

{
  "listing_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_data_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "filename": "image.jpg",
  "content_type": "image/jpeg",
  "display_order": 0,
  "is_primary": true
}
```

### Download Image

```bash
GET /api/v1/listing-images/{image_id}/download
```

Returns the binary image data with appropriate Content-Type header.

### Get Image Metadata

```bash
GET /api/v1/listing-images/{image_id}
```

Returns image metadata (without binary data by default to keep responses small).

## Usage Examples

### Python (requests)

```python
import requests
import base64

# Upload file
with open("image.jpg", "rb") as f:
    files = {"file": f}
    data = {
        "listing_id": "123e4567-e89b-12d3-a456-426614174000",
        "display_order": 0,
        "is_primary": True
    }
    response = requests.post(
        "http://localhost:8000/api/v1/listing-images/upload",
        files=files,
        data=data
    )
    print(response.json())

# Upload base64
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "listing_id": "123e4567-e89b-12d3-a456-426614174000",
        "image_data_base64": image_data,
        "filename": "image.jpg",
        "content_type": "image/jpeg",
        "display_order": 0,
        "is_primary": True
    }
    response = requests.post(
        "http://localhost:8000/api/v1/listing-images/",
        json=payload
    )
    print(response.json())
```

### JavaScript (fetch)

```javascript
// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('listing_id', '123e4567-e89b-12d3-a456-426614174000');
formData.append('display_order', '0');
formData.append('is_primary', 'true');

fetch('http://localhost:8000/api/v1/listing-images/upload', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));

// Upload base64
const file = fileInput.files[0];
const reader = new FileReader();
reader.onload = () => {
  const base64 = reader.result.split(',')[1]; // Remove data URL prefix
  
  fetch('http://localhost:8000/api/v1/listing-images/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      listing_id: '123e4567-e89b-12d3-a456-426614174000',
      image_data_base64: base64,
      filename: file.name,
      content_type: file.type,
      display_order: 0,
      is_primary: true
    })
  })
  .then(res => res.json())
  .then(data => console.log(data));
};
reader.readAsDataURL(file);
```

## Migration Notes

If you have existing `listing_images` records with `image_url` only:

1. The `image_url` field is still supported
2. You can migrate URLs to binary data by downloading and re-uploading
3. Both `image_url` and `image_data` can coexist (URL takes precedence for display)

## Performance Considerations

- **Database Size**: Storing binary data in the database increases database size
- **Query Performance**: Large images may slow down queries that return image data
- **Recommendations**:
  - Use the metadata endpoint (`GET /api/v1/listing-images/{id}`) for lists
  - Only fetch binary data when needed (`GET /api/v1/listing-images/{id}/download`)
  - Consider using `image_url` for very large images or CDN-hosted assets
  - Set appropriate `MAX_UPLOAD_SIZE_MB` in `.env` to limit file sizes

## Limits

- Maximum file size is controlled by `MAX_UPLOAD_SIZE_MB` in `.env` (default: 10MB)
- PostgreSQL `BYTEA` can store up to 1GB per field
- Consider using external storage (S3, Cloudinary) for production with many/large images







