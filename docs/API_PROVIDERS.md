# Providers API

Provider registration and management endpoints for senior housing facility owners.

**Base Path:** `/api/v1/providers`

## Endpoints

### List Providers

Get a paginated list of all providers.

**Endpoint:** `GET /api/v1/providers`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/providers?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "223e4567-e89b-12d3-a456-426614174000",
    "business_name": "Sunset Senior Living",
    "business_type": "Assisted Living Facility",
    "tax_id": "12-3456789",
    "address": "123 Main St",
    "city": "Los Angeles",
    "country": "USA",
    "verification_status": "VERIFIED",
    "verified_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Provider by ID

Get a specific provider by their ID.

**Endpoint:** `GET /api/v1/providers/{provider_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `provider_id` (UUID, required) - Provider ID

**Example Request:**
```
GET /api/v1/providers/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living",
  "business_type": "Assisted Living Facility",
  "tax_id": "12-3456789",
  "address": "123 Main St",
  "city": "Los Angeles",
  "country": "USA",
  "verification_status": "VERIFIED",
  "verified_at": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Provider not found

---

### Create Provider

Register a new provider (housing facility owner).

**Endpoint:** `POST /api/v1/providers`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living",
  "business_type": "Assisted Living Facility",
  "tax_id": "12-3456789",
  "address": "123 Main St",
  "city": "Los Angeles",
  "country": "USA"
}
```

**Request Fields:**
- `user_id` (UUID, required) - Associated user account ID
- `business_name` (string, required) - Business name
- `business_type` (string, required) - Type of business
- `tax_id` (string, optional) - Tax identification number
- `address` (string, optional) - Business address
- `city` (string, optional) - City
- `country` (string, optional) - Country

**Response:** `201 Created`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living",
  "business_type": "Assisted Living Facility",
  "tax_id": "12-3456789",
  "address": "123 Main St",
  "city": "Los Angeles",
  "country": "USA",
  "verification_status": "PENDING",
  "verified_at": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request data

---

### Update Provider

Update provider information.

**Endpoint:** `PUT /api/v1/providers/{provider_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `provider_id` (UUID, required) - Provider ID

**Request Body:**
```json
{
  "business_name": "Sunset Senior Living Updated",
  "business_type": "Memory Care Facility",
  "tax_id": "12-3456789",
  "address": "456 Oak Ave",
  "city": "San Francisco",
  "country": "USA"
}
```

**Request Fields:** (All optional)
- `business_name` (string, optional)
- `business_type` (string, optional)
- `tax_id` (string, optional)
- `address` (string, optional)
- `city` (string, optional)
- `country` (string, optional)
- `verification_status` (string, optional) - Admin only

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living Updated",
  "business_type": "Memory Care Facility",
  "tax_id": "12-3456789",
  "address": "456 Oak Ave",
  "city": "San Francisco",
  "country": "USA",
  "verification_status": "PENDING",
  "verified_at": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Provider not found
- `400 Bad Request` - Invalid request data

---

### Verify Provider

Admin endpoint to verify a provider (approve verification).

**Endpoint:** `POST /api/v1/providers/{provider_id}/verify`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `provider_id` (UUID, required) - Provider ID

**Example Request:**
```
POST /api/v1/providers/123e4567-e89b-12d3-a456-426614174000/verify
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living",
  "business_type": "Assisted Living Facility",
  "tax_id": "12-3456789",
  "address": "123 Main St",
  "city": "Los Angeles",
  "country": "USA",
  "verification_status": "VERIFIED",
  "verified_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Provider not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

### Reject Provider

Admin endpoint to reject a provider verification.

**Endpoint:** `POST /api/v1/providers/{provider_id}/reject`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `provider_id` (UUID, required) - Provider ID

**Example Request:**
```
POST /api/v1/providers/123e4567-e89b-12d3-a456-426614174000/reject
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "business_name": "Sunset Senior Living",
  "business_type": "Assisted Living Facility",
  "tax_id": "12-3456789",
  "address": "123 Main St",
  "city": "Los Angeles",
  "country": "USA",
  "verification_status": "REJECTED",
  "verified_at": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Provider not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

### Delete Provider

Delete a provider account.

**Endpoint:** `DELETE /api/v1/providers/{provider_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `provider_id` (UUID, required) - Provider ID

**Example Request:**
```
DELETE /api/v1/providers/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Provider not found

---

## Verification Status

Providers have the following verification statuses:

- `PENDING` - Awaiting admin verification
- `VERIFIED` - Verified and approved by admin
- `REJECTED` - Verification rejected by admin

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Register as provider
async function registerProvider(userId: string, providerData: {
  business_name: string;
  business_type: string;
  tax_id?: string;
  address?: string;
  city?: string;
  country?: string;
}) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/providers`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      ...providerData
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to register provider');
  }
  
  return response.json();
}

// Get provider details
async function getProvider(providerId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/providers/${providerId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch provider');
  }
  
  return response.json();
}
```


