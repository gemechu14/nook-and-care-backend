# Reports API

Fraud and issue reporting endpoints.

**Base Path:** `/api/v1/reports`

## Endpoints

### List Reports

Get a paginated list of all reports.

**Endpoint:** `GET /api/v1/reports`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/reports?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "reported_by_user_id": "223e4567-e89b-12d3-a456-426614174000",
    "reported_user_id": "323e4567-e89b-12d3-a456-426614174000",
    "listing_id": "423e4567-e89b-12d3-a456-426614174000",
    "report_type": "FAKE_LISTING",
    "description": "This listing appears to be fraudulent...",
    "status": "PENDING",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Report by ID

Get a specific report by its ID.

**Endpoint:** `GET /api/v1/reports/{report_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `report_id` (UUID, required) - Report ID

**Example Request:**
```
GET /api/v1/reports/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "reported_by_user_id": "223e4567-e89b-12d3-a456-426614174000",
  "reported_user_id": "323e4567-e89b-12d3-a456-426614174000",
  "listing_id": "423e4567-e89b-12d3-a456-426614174000",
  "report_type": "FAKE_LISTING",
  "description": "This listing appears to be fraudulent...",
  "status": "PENDING",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Report not found

---

### File Report

Create a new report.

**Endpoint:** `POST /api/v1/reports`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "reported_by_user_id": "223e4567-e89b-12d3-a456-426614174000",
  "reported_user_id": "323e4567-e89b-12d3-a456-426614174000",
  "listing_id": "423e4567-e89b-12d3-a456-426614174000",
  "report_type": "FAKE_LISTING",
  "description": "This listing appears to be fraudulent..."
}
```

**Request Fields:**
- `reported_by_user_id` (UUID, required) - User ID filing the report
- `report_type` (string, required) - Report type
- `description` (string, required) - Report description
- `reported_user_id` (UUID, optional) - Provider/user being reported
- `listing_id` (UUID, optional) - Listing being reported

**Response:** `201 Created`

Same format as Get Report by ID response, with `status: "PENDING"`.

**Error Responses:**
- `400 Bad Request` - Invalid request data

---

### Update Report

Update report information.

**Endpoint:** `PUT /api/v1/reports/{report_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `report_id` (UUID, required) - Report ID

**Request Body:**
```json
{
  "status": "REVIEWED"
}
```

**Request Fields:** (All optional)
- `status` (string, optional) - Report status

**Response:** `200 OK`

Same format as Get Report by ID response.

**Error Responses:**
- `404 Not Found` - Report not found
- `400 Bad Request` - Invalid request data

---

### Review Report

Admin endpoint to mark a report as reviewed.

**Endpoint:** `POST /api/v1/reports/{report_id}/review`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `report_id` (UUID, required) - Report ID

**Example Request:**
```
POST /api/v1/reports/123e4567-e89b-12d3-a456-426614174000/review
```

**Response:** `200 OK`

Same format as Get Report by ID response, with `status: "REVIEWED"`.

**Error Responses:**
- `404 Not Found` - Report not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

### Resolve Report

Admin endpoint to mark a report as resolved.

**Endpoint:** `POST /api/v1/reports/{report_id}/resolve`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `report_id` (UUID, required) - Report ID

**Example Request:**
```
POST /api/v1/reports/123e4567-e89b-12d3-a456-426614174000/resolve
```

**Response:** `200 OK`

Same format as Get Report by ID response, with `status: "RESOLVED"`.

**Error Responses:**
- `404 Not Found` - Report not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

### Dismiss Report

Admin endpoint to dismiss a report.

**Endpoint:** `POST /api/v1/reports/{report_id}/dismiss`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `report_id` (UUID, required) - Report ID

**Example Request:**
```
POST /api/v1/reports/123e4567-e89b-12d3-a456-426614174000/dismiss
```

**Response:** `200 OK`

Same format as Get Report by ID response, with `status: "DISMISSED"`.

**Error Responses:**
- `404 Not Found` - Report not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

## Report Types

- `FAKE_LISTING` - Fake or fraudulent listing
- `SCAM_PROVIDER` - Scam provider
- `MISLEADING_IMAGES` - Misleading or fake images
- `FRAUD` - General fraud
- `OTHER` - Other issues

## Report Status

- `PENDING` - Report pending admin review
- `REVIEWED` - Report reviewed by admin
- `RESOLVED` - Report resolved
- `DISMISSED` - Report dismissed

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// File a report
async function fileReport(
  reportedByUserId: string,
  reportType: 'FAKE_LISTING' | 'SCAM_PROVIDER' | 'MISLEADING_IMAGES' | 'FRAUD' | 'OTHER',
  description: string,
  reportedUserId?: string,
  listingId?: string
) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/reports`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      reported_by_user_id: reportedByUserId,
      report_type: reportType,
      description,
      reported_user_id: reportedUserId,
      listing_id: listingId
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to file report');
  }
  
  return response.json();
}

// Get reports (Admin only)
async function getReports(skip: number = 0, limit: number = 20) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/reports?skip=${skip}&limit=${limit}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch reports');
  }
  
  return response.json();
}

// Review report (Admin only)
async function reviewReport(reportId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/reports/${reportId}/review`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to review report');
  }
  
  return response.json();
}
```


