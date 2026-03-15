# Listing Features Batch Operations API

Complete API documentation for batch create and delete operations on listing features (amenities, activities, languages, certifications, dining options, safety features, insurance options, house rules, equipment, and services).

**Base Path:** `/api/v1`

---

## Overview

These endpoints allow providers to manage multiple listing feature associations in a single request, significantly improving performance and user experience when managing listings with many features.

### Key Features

- **Batch Operations**: Create or delete multiple associations in one request
- **Transaction Safety**: All-or-nothing behavior - if any item fails, the entire batch is rolled back
- **Validation**: Comprehensive validation before any database operations
- **Authorization**: Only listing owners (providers) or admins can manage features
- **Duplicate Prevention**: Automatically prevents duplicate associations

---

## Authentication

All endpoints require Bearer token authentication:

```
Authorization: Bearer <your_access_token>
```

**Required Role:** `PROVIDER` (must own the listing) or `ADMIN`

---

## Common Request Format

All batch endpoints follow the same pattern:

```json
{
  "items": [
    {
      "listing_id": "uuid",
      "{feature}_id": "uuid",
      // ... additional fields for specific feature types
    }
  ]
}
```

### Validation Rules

1. **Same Listing**: All items in a batch must reference the same `listing_id`
2. **Valid IDs**: All feature IDs must exist in the catalog
3. **No Duplicates**: Cannot create associations that already exist
4. **Ownership**: User must own the listing (or be admin)

---

## Common Response Format

All endpoints return an array of created/deleted associations:

```json
[
  {
    "id": "uuid",
    "listing_id": "uuid",
    "{feature}_id": "uuid",
    "created_at": "2024-01-01T00:00:00Z"
    // ... additional fields for specific feature types
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "All items must reference the same listing"
}
```

```json
{
  "detail": "Some amenities already associated: {amenity_ids}"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to manage this listing"
}
```

### 404 Not Found
```json
{
  "detail": "Listing not found"
}
```

```json
{
  "detail": "Amenity {amenity_id} not found"
}
```

---

## 1. Listing Amenities

### Batch Create Amenities

**Endpoint:** `POST /api/v1/listing-amenities/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "amenity_id": "223e4567-e89b-12d3-a456-426614174001"
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "amenity_id": "323e4567-e89b-12d3-a456-426614174002"
    }
  ]
}
```

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "amenity_id": "223e4567-e89b-12d3-a456-426614174001",
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": "523e4567-e89b-12d3-a456-426614174004",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "amenity_id": "323e4567-e89b-12d3-a456-426614174002",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete Amenities

**Endpoint:** `DELETE /api/v1/listing-amenities/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "amenity_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

**Response:** `200 OK`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "amenity_id": "223e4567-e89b-12d3-a456-426614174001",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

## 2. Listing Activities

### Batch Create Activities

**Endpoint:** `POST /api/v1/listing-activities/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "activity_id": "223e4567-e89b-12d3-a456-426614174001"
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "activity_id": "323e4567-e89b-12d3-a456-426614174002"
    }
  ]
}
```

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "activity_id": "223e4567-e89b-12d3-a456-426614174001",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete Activities

**Endpoint:** `DELETE /api/v1/listing-activities/batch`

**Request Body:** Same as create

**Response:** `200 OK` - Array of deleted associations

---

## 3. Listing Languages

### Batch Create Languages

**Endpoint:** `POST /api/v1/listing-languages/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "language_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

### Batch Delete Languages

**Endpoint:** `DELETE /api/v1/listing-languages/batch`

---

## 4. Listing Certifications

### Batch Create Certifications

**Endpoint:** `POST /api/v1/listing-certifications/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "certification_id": "223e4567-e89b-12d3-a456-426614174001",
      "license_number": "LIC-12345"
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "certification_id": "323e4567-e89b-12d3-a456-426614174002",
      "license_number": null
    }
  ]
}
```

**Note:** `license_number` is optional and can be `null`.

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "certification_id": "223e4567-e89b-12d3-a456-426614174001",
    "license_number": "LIC-12345",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete Certifications

**Endpoint:** `DELETE /api/v1/listing-certifications/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "certification_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

---

## 5. Listing Dining Options

### Batch Create Dining Options

**Endpoint:** `POST /api/v1/listing-dining-options/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "dining_option_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

### Batch Delete Dining Options

**Endpoint:** `DELETE /api/v1/listing-dining-options/batch`

---

## 6. Listing Safety Features

### Batch Create Safety Features

**Endpoint:** `POST /api/v1/listing-safety-features/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "safety_feature_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

### Batch Delete Safety Features

**Endpoint:** `DELETE /api/v1/listing-safety-features/batch`

---

## 7. Listing Insurance Options

### Batch Create Insurance Options

**Endpoint:** `POST /api/v1/listing-insurance-options/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "insurance_option_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

### Batch Delete Insurance Options

**Endpoint:** `DELETE /api/v1/listing-insurance-options/batch`

---

## 8. Listing House Rules

### Batch Create House Rules

**Endpoint:** `POST /api/v1/listing-house-rules/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "house_rule_id": "223e4567-e89b-12d3-a456-426614174001",
      "display_order": 1
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "house_rule_id": "323e4567-e89b-12d3-a456-426614174002",
      "display_order": 2
    }
  ]
}
```

**Note:** `display_order` is optional. If not provided, it will be auto-incremented based on the item's position in the array (0, 1, 2, ...).

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "house_rule_id": "223e4567-e89b-12d3-a456-426614174001",
    "display_order": 1,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete House Rules

**Endpoint:** `DELETE /api/v1/listing-house-rules/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "house_rule_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

---

## 9. Listing Equipment

### Batch Create Equipment

**Endpoint:** `POST /api/v1/listing-equipment/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "equipment_id": "223e4567-e89b-12d3-a456-426614174001",
      "quantity": 5
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "equipment_id": "323e4567-e89b-12d3-a456-426614174002",
      "quantity": 10
    }
  ]
}
```

**Note:** `quantity` defaults to `1` if not provided.

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "equipment_id": "223e4567-e89b-12d3-a456-426614174001",
    "quantity": 5,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete Equipment

**Endpoint:** `DELETE /api/v1/listing-equipment/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "equipment_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

---

## 10. Listing Services (Treatment Services)

### Batch Create Services

**Endpoint:** `POST /api/v1/listing-services/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "treatment_service_id": "223e4567-e89b-12d3-a456-426614174001",
      "price": 50.00,
      "is_included": false
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "treatment_service_id": "323e4567-e89b-12d3-a456-426614174002",
      "price": null,
      "is_included": true
    }
  ]
}
```

**Note:** 
- `price` is optional and can be `null`
- `is_included` defaults to `false` if not provided

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "treatment_service_id": "223e4567-e89b-12d3-a456-426614174001",
    "price": 50.00,
    "is_included": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Delete Services

**Endpoint:** `DELETE /api/v1/listing-services/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "treatment_service_id": "223e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
```

---

## Frontend Integration Guide

### 1. API Base URL

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

### 2. Authentication

Include the Bearer token in all requests:

```javascript
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${accessToken}`
};
```

### 3. Batch Create Example (React/TypeScript)

```typescript
interface BatchCreateRequest {
  items: Array<{
    listing_id: string;
    amenity_id: string;
  }>;
}

async function batchCreateAmenities(
  listingId: string,
  amenityIds: string[],
  accessToken: string
): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/listing-amenities/batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      items: amenityIds.map(amenityId => ({
        listing_id: listingId,
        amenity_id: amenityId
      }))
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create amenities');
  }

  return await response.json();
}
```

### 4. Batch Delete Example

```typescript
async function batchDeleteAmenities(
  listingId: string,
  amenityIds: string[],
  accessToken: string
): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/listing-amenities/batch`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      items: amenityIds.map(amenityId => ({
        listing_id: listingId,
        amenity_id: amenityId
      }))
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete amenities');
  }

  return await response.json();
}
```

### 5. Complete React Hook Example

```typescript
import { useState } from 'react';

interface UseBatchAmenitiesProps {
  listingId: string;
  accessToken: string;
}

export function useBatchAmenities({ listingId, accessToken }: UseBatchAmenitiesProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const batchCreate = async (amenityIds: string[]) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/listing-amenities/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          items: amenityIds.map(amenityId => ({
            listing_id: listingId,
            amenity_id: amenityId
          }))
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create amenities');
      }

      const data = await response.json();
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const batchDelete = async (amenityIds: string[]) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/listing-amenities/batch`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          items: amenityIds.map(amenityId => ({
            listing_id: listingId,
            amenity_id: amenityId
          }))
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete amenities');
      }

      const data = await response.json();
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    batchCreate,
    batchDelete,
    loading,
    error
  };
}
```

### 6. Usage in Component

```typescript
function ListingAmenitiesManager({ listingId, accessToken }: Props) {
  const { batchCreate, batchDelete, loading, error } = useBatchAmenities({
    listingId,
    accessToken
  });

  const handleSave = async (selectedAmenityIds: string[]) => {
    try {
      // Get current amenities
      const currentResponse = await fetch(
        `${API_BASE_URL}/listings/${listingId}`
      );
      const listing = await currentResponse.json();
      const currentAmenityIds = listing.amenities.map((a: any) => a.amenity.id);

      // Find added and removed
      const added = selectedAmenityIds.filter(id => !currentAmenityIds.includes(id));
      const removed = currentAmenityIds.filter(id => !selectedAmenityIds.includes(id));

      // Batch operations
      if (added.length > 0) {
        await batchCreate(added);
      }
      if (removed.length > 0) {
        await batchDelete(removed);
      }

      // Success notification
      alert('Amenities updated successfully!');
    } catch (err) {
      alert(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  return (
    <div>
      {/* Your UI here */}
      <button onClick={() => handleSave(selectedIds)} disabled={loading}>
        {loading ? 'Saving...' : 'Save Changes'}
      </button>
      {error && <div className="error">{error}</div>}
    </div>
  );
}
```

### 7. Error Handling

```typescript
try {
  await batchCreate(amenityIds);
} catch (error) {
  if (error instanceof Error) {
    // Handle specific error messages
    if (error.message.includes('already associated')) {
      // Show user-friendly message
      alert('Some amenities are already associated with this listing');
    } else if (error.message.includes('same listing')) {
      alert('All items must reference the same listing');
    } else if (error.message.includes('permission')) {
      alert('You do not have permission to manage this listing');
    } else {
      alert(`Error: ${error.message}`);
    }
  }
}
```

### 8. Axios Example

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Batch create function
export const batchCreateAmenities = async (
  listingId: string,
  amenityIds: string[]
) => {
  const response = await api.post('/listing-amenities/batch', {
    items: amenityIds.map(amenityId => ({
      listing_id: listingId,
      amenity_id: amenityId
    }))
  });
  return response.data;
};
```

---

## Endpoint Summary

| Feature Type | Create Endpoint | Delete Endpoint |
|-------------|----------------|-----------------|
| Amenities | `POST /listing-amenities/batch` | `DELETE /listing-amenities/batch` |
| Activities | `POST /listing-activities/batch` | `DELETE /listing-activities/batch` |
| Languages | `POST /listing-languages/batch` | `DELETE /listing-languages/batch` |
| Certifications | `POST /listing-certifications/batch` | `DELETE /listing-certifications/batch` |
| Dining Options | `POST /listing-dining-options/batch` | `DELETE /listing-dining-options/batch` |
| Safety Features | `POST /listing-safety-features/batch` | `DELETE /listing-safety-features/batch` |
| Insurance Options | `POST /listing-insurance-options/batch` | `DELETE /listing-insurance-options/batch` |
| House Rules | `POST /listing-house-rules/batch` | `DELETE /listing-house-rules/batch` |
| Equipment | `POST /listing-equipment/batch` | `DELETE /listing-equipment/batch` |
| Services | `POST /listing-services/batch` | `DELETE /listing-services/batch` |
| Images | `POST /listing-images/batch` or `/listing-images/batch/upload` | `DELETE /listing-images/batch` |

---

## Testing with cURL

### Create Amenities
```bash
curl -X POST "http://localhost:8000/api/v1/listing-amenities/batch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "items": [
      {
        "listing_id": "123e4567-e89b-12d3-a456-426614174000",
        "amenity_id": "223e4567-e89b-12d3-a456-426614174001"
      }
    ]
  }'
```

### Delete Amenities
```bash
curl -X DELETE "http://localhost:8000/api/v1/listing-amenities/batch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "items": [
      {
        "listing_id": "123e4567-e89b-12d3-a456-426614174000",
        "amenity_id": "223e4567-e89b-12d3-a456-426614174001"
      }
    ]
  }'
```

---

## Notes

1. **Transaction Safety**: All batch operations are transactional. If any item fails validation, the entire batch is rolled back.

2. **Performance**: Batch operations are significantly faster than individual requests, especially when managing many features.

3. **Validation Order**: 
   - First: Verify all items reference the same listing
   - Second: Verify user owns the listing
   - Third: Verify all feature IDs exist
   - Fourth: Check for existing associations
   - Finally: Create/delete all items

4. **Response Order**: The response array maintains the same order as the request items.

5. **Empty Batches**: Sending an empty `items` array will return a 400 error.

---

---

## 11. Listing Images (Bulk Upload & Delete)

### Batch Upload Images (Base64/URL)

**Endpoint:** `POST /api/v1/listing-images/batch`

**Request Body:**
```json
{
  "items": [
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "image_data_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "filename": "facility-photo-1.jpg",
      "content_type": "image/jpeg",
      "display_order": 0,
      "is_primary": true
    },
    {
      "listing_id": "123e4567-e89b-12d3-a456-426614174000",
      "image_url": "https://example.com/image.jpg",
      "filename": "facility-photo-2.jpg",
      "display_order": 1,
      "is_primary": false
    }
  ]
}
```

**Note:** 
- Either `image_data_base64` or `image_url` must be provided
- `image_data_base64` should be base64-encoded image data (data URL prefix optional)
- Maximum file size: 10MB per image
- `display_order` defaults to 0 if not provided
- `is_primary` defaults to false if not provided

**Response:** `201 Created`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_url": null,
    "filename": "facility-photo-1.jpg",
    "content_type": "image/jpeg",
    "file_size": 245678,
    "display_order": 0,
    "is_primary": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Batch Upload Images (Multipart/Form-Data)

**Endpoint:** `POST /api/v1/listing-images/batch/upload`

**Content-Type:** `multipart/form-data`

**Form Fields:**
- `listing_id` (UUID, required) - Listing ID to attach images to
- `files` (File[], required) - Array of image files to upload

**Supported Formats:** JPEG, PNG, GIF, WebP, BMP
**Maximum File Size:** 10MB per file

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/api/v1/listing-images/batch/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "listing_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "files=@image3.gif"
```

**Response:** `201 Created` - Same format as base64 upload

### Batch Delete Images

**Endpoint:** `DELETE /api/v1/listing-images/batch`

**Request Body:**
```json
{
  "items": [
    {
      "image_id": "423e4567-e89b-12d3-a456-426614174003"
    },
    {
      "image_id": "523e4567-e89b-12d3-a456-426614174004"
    }
  ]
}
```

**Response:** `200 OK`
```json
[
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "listing_id": "123e4567-e89b-12d3-a456-426614174000",
    "filename": "facility-photo-1.jpg",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Note:** Only images belonging to listings owned by the authenticated provider can be deleted.

---

## Frontend Integration for Images

### Batch Upload with Base64 (React)

```typescript
async function batchUploadImages(
  listingId: string,
  imageFiles: File[],
  accessToken: string
): Promise<any[]> {
  // Convert files to base64
  const items = await Promise.all(
    imageFiles.map(async (file, index) => {
      const base64 = await fileToBase64(file);
      return {
        listing_id: listingId,
        image_data_base64: base64,
        filename: file.name,
        content_type: file.type,
        display_order: index,
        is_primary: index === 0
      };
    })
  );

  const response = await fetch(`${API_BASE_URL}/listing-images/batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({ items })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to upload images');
  }

  return await response.json();
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = error => reject(error);
  });
}
```

### Batch Upload with FormData (React)

```typescript
async function batchUploadImageFiles(
  listingId: string,
  imageFiles: File[],
  accessToken: string
): Promise<any[]> {
  const formData = new FormData();
  formData.append('listing_id', listingId);
  
  imageFiles.forEach(file => {
    formData.append('files', file);
  });

  const response = await fetch(`${API_BASE_URL}/listing-images/batch/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
      // Don't set Content-Type - browser will set it with boundary
    },
    body: formData
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to upload images');
  }

  return await response.json();
}
```

### Batch Delete Images

```typescript
async function batchDeleteImages(
  imageIds: string[],
  accessToken: string
): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/listing-images/batch`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      items: imageIds.map(imageId => ({ image_id: imageId }))
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete images');
  }

  return await response.json();
}
```

### Complete Image Manager Hook

```typescript
import { useState } from 'react';

export function useBatchImages({ listingId, accessToken }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const batchUpload = async (files: File[]) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('listing_id', listingId);
      files.forEach(file => formData.append('files', file));

      const response = await fetch(`${API_BASE_URL}/listing-images/batch/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${accessToken}` },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload images');
      }

      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const batchDelete = async (imageIds: string[]) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/listing-images/batch`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          items: imageIds.map(id => ({ image_id: id }))
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete images');
      }

      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { batchUpload, batchDelete, loading, error };
}
```

---

**Last Updated:** 2024
**Version:** 1.0

