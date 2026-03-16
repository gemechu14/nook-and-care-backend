# Tours API

Tour booking and management endpoints.

**Base Path:** `/api/v1/tours`

## Endpoints

### List Tours

Get a paginated list of all tours.

**Endpoint:** `GET /api/v1/tours`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/tours?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "listing_id": "223e4567-e89b-12d3-a456-426614174000",
    "tour_type": "IN_PERSON",
    "scheduled_at": "2024-02-15T14:00:00Z",
    "status": "PENDING",
    "booked_by_user_id": "323e4567-e89b-12d3-a456-426614174000",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Tour by ID

Get a specific tour by its ID.

**Endpoint:** `GET /api/v1/tours/{tour_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Example Request:**
```
GET /api/v1/tours/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "listing_id": "223e4567-e89b-12d3-a456-426614174000",
  "tour_type": "IN_PERSON",
  "scheduled_at": "2024-02-15T14:00:00Z",
  "status": "APPROVED",
  "booked_by_user_id": "323e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Tour not found

---

### Book Tour

Book a tour for a listing.

**Endpoint:** `POST /api/v1/tours`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "listing_id": "223e4567-e89b-12d3-a456-426614174000",
  "tour_type": "IN_PERSON",
  "scheduled_at": "2024-02-15T14:00:00Z",
  "booked_by_user_id": "323e4567-e89b-12d3-a456-426614174000"
}
```

**Request Fields:**
- `listing_id` (UUID, required) - Listing ID
- `tour_type` (string, required) - Tour type: `VIRTUAL` or `IN_PERSON`
- `scheduled_at` (datetime, required) - Scheduled date and time (ISO 8601 format)
- `booked_by_user_id` (UUID, optional) - User ID booking the tour (defaults to current user)

**Response:** `201 Created`

Same format as Get Tour by ID response, with `status: "PENDING"`.

**Error Responses:**
- `400 Bad Request` - Invalid request data

---

### Update Tour

Update tour information.

**Endpoint:** `PUT /api/v1/tours/{tour_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Request Body:**
```json
{
  "tour_type": "VIRTUAL",
  "scheduled_at": "2024-02-16T15:00:00Z",
  "status": "SCHEDULED"
}
```

**Request Fields:** (All optional)
- `tour_type` (string, optional) - Tour type: `VIRTUAL` or `IN_PERSON`
- `scheduled_at` (datetime, optional) - Scheduled date and time
- `status` (string, optional) - Tour status

**Response:** `200 OK`

Same format as Get Tour by ID response.

**Error Responses:**
- `404 Not Found` - Tour not found
- `400 Bad Request` - Invalid request data

---

### Approve Tour

Approve a pending tour request (Provider only).

**Endpoint:** `POST /api/v1/tours/{tour_id}/approve`

**Authentication:** Required (Bearer token, Provider role)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Example Request:**
```
POST /api/v1/tours/123e4567-e89b-12d3-a456-426614174000/approve
```

**Response:** `200 OK`

Same format as Get Tour by ID response, with `status: "APPROVED"`.

**Error Responses:**
- `404 Not Found` - Tour not found
- `403 Forbidden` - Insufficient permissions

---

### Cancel Tour

Cancel a tour.

**Endpoint:** `POST /api/v1/tours/{tour_id}/cancel`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Example Request:**
```
POST /api/v1/tours/123e4567-e89b-12d3-a456-426614174000/cancel
```

**Response:** `200 OK`

Same format as Get Tour by ID response, with `status: "CANCELLED"`.

**Error Responses:**
- `404 Not Found` - Tour not found

---

### Complete Tour

Mark a tour as completed.

**Endpoint:** `POST /api/v1/tours/{tour_id}/complete`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Example Request:**
```
POST /api/v1/tours/123e4567-e89b-12d3-a456-426614174000/complete
```

**Response:** `200 OK`

Same format as Get Tour by ID response, with `status: "COMPLETED"`.

**Error Responses:**
- `404 Not Found` - Tour not found

---

### Delete Tour

Delete a tour.

**Endpoint:** `DELETE /api/v1/tours/{tour_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `tour_id` (UUID, required) - Tour ID

**Example Request:**
```
DELETE /api/v1/tours/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Tour not found

---

## Tour Types

- `VIRTUAL` - Virtual tour (video call, online)
- `IN_PERSON` - In-person tour at the facility

## Tour Status

- `PENDING` - Tour request pending provider approval
- `APPROVED` - Tour approved by provider
- `SCHEDULED` - Tour scheduled and confirmed
- `COMPLETED` - Tour completed
- `CANCELLED` - Tour cancelled

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Book a tour
async function bookTour(listingId: string, scheduledAt: string, tourType: 'VIRTUAL' | 'IN_PERSON') {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/tours`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      listing_id: listingId,
      tour_type: tourType,
      scheduled_at: scheduledAt
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to book tour');
  }
  
  return response.json();
}

// Get tour details
async function getTour(tourId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/tours/${tourId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch tour');
  }
  
  return response.json();
}

// Approve tour (Provider only)
async function approveTour(tourId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/tours/${tourId}/approve`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to approve tour');
  }
  
  return response.json();
}

// Cancel tour
async function cancelTour(tourId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/tours/${tourId}/cancel`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to cancel tour');
  }
  
  return response.json();
}
```





