# Listings API

Senior housing facility listing management endpoints.

**Base Path:** `/api/v1/listings`

## Endpoints

### List Listings

Get a paginated and filtered list of listings.

**Endpoint:** `GET /api/v1/listings`

**Authentication:** Not required (public endpoint)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return
- `city` (string, optional) - Filter by city
- `care_type` (string, optional) - Filter by care type
- `min_price` (float, optional) - Minimum price filter
- `max_price` (float, optional) - Maximum price filter

**Example Request:**
```
GET /api/v1/listings?city=Los Angeles&care_type=ASSISTED_LIVING&min_price=3000&max_price=5000&skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "provider_id": "223e4567-e89b-12d3-a456-426614174000",
    "title": "Sunset Senior Living",
    "description": "A beautiful assisted living facility...",
    "care_type": "ASSISTED_LIVING",
    "room_type": "PRIVATE",
    "address": "123 Main St",
    "city": "Los Angeles",
    "state": "CA",
    "country": "USA",
    "postal_code": "90001",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "price": 4500.00,
    "currency": "USD",
    "capacity": 50,
    "available_beds": 12,
    "staff_ratio": "1:3",
    "established_year": 2010,
    "phone": "+1234567890",
    "email": "info@sunsetliving.com",
    "license_number": "CA-12345",
    "is_featured": true,
    "has_24_hour_care": true,
    "status": "ACTIVE",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Featured Listings

Get a paginated list of featured listings (for homepage).

**Endpoint:** `GET /api/v1/listings/featured`

**Authentication:** Not required (public endpoint)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/listings/featured?skip=0&limit=10
```

**Response:** `200 OK`

Same format as List Listings response.

---

### Get Listing by ID

Get a specific listing by its ID.

**Endpoint:** `GET /api/v1/listings/{listing_id}`

**Authentication:** Not required (public endpoint)

**Path Parameters:**
- `listing_id` (UUID, required) - Listing ID

**Example Request:**
```
GET /api/v1/listings/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "title": "Sunset Senior Living",
  "description": "A beautiful assisted living facility...",
  "care_type": "ASSISTED_LIVING",
  "room_type": "PRIVATE",
  "address": "123 Main St",
  "city": "Los Angeles",
  "state": "CA",
  "country": "USA",
  "postal_code": "90001",
  "latitude": 34.0522,
  "longitude": -118.2437,
  "price": 4500.00,
  "currency": "USD",
  "capacity": 50,
  "available_beds": 12,
  "staff_ratio": "1:3",
  "established_year": 2010,
  "phone": "+1234567890",
  "email": "info@sunsetliving.com",
  "license_number": "CA-12345",
  "is_featured": true,
  "has_24_hour_care": true,
  "status": "ACTIVE",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Listing not found

---

### Create Listing

Create a new listing (Provider only).

**Endpoint:** `POST /api/v1/listings`

**Authentication:** Required (Bearer token, Provider role)

**Request Body:**
```json
{
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "title": "Sunset Senior Living",
  "description": "A beautiful assisted living facility...",
  "care_type": "ASSISTED_LIVING",
  "room_type": "PRIVATE",
  "address": "123 Main St",
  "city": "Los Angeles",
  "state": "CA",
  "country": "USA",
  "postal_code": "90001",
  "latitude": 34.0522,
  "longitude": -118.2437,
  "price": 4500.00,
  "currency": "USD",
  "capacity": 50,
  "available_beds": 12,
  "staff_ratio": "1:3",
  "established_year": 2010,
  "phone": "+1234567890",
  "email": "info@sunsetliving.com",
  "license_number": "CA-12345",
  "is_featured": false,
  "has_24_hour_care": true
}
```

**Request Fields:**
- `provider_id` (UUID, required) - Provider ID
- `title` (string, required) - Listing title
- `description` (string, optional) - Listing description
- `care_type` (string, required) - Care type: `ASSISTED_LIVING`, `MEMORY_CARE`, `INDEPENDENT_LIVING`, `ADULT_FAMILY_HOME`, `SKILLED_NURSING`
- `room_type` (string, required) - Room type: `PRIVATE`, `SEMI_PRIVATE`, `SHARED`
- `address` (string, optional) - Street address
- `city` (string, optional) - City
- `state` (string, optional) - State/Province
- `country` (string, optional) - Country
- `postal_code` (string, optional) - Postal/ZIP code
- `latitude` (float, optional) - Latitude coordinate
- `longitude` (float, optional) - Longitude coordinate
- `price` (float, optional) - Monthly price
- `currency` (string, optional, default: "USD") - Currency code
- `capacity` (integer, optional) - Total capacity
- `available_beds` (integer, optional) - Available beds
- `staff_ratio` (string, optional) - Staff to resident ratio (e.g., "1:3")
- `established_year` (integer, optional) - Year established
- `phone` (string, optional) - Contact phone
- `email` (string, optional) - Contact email
- `license_number` (string, optional) - License number
- `is_featured` (boolean, optional, default: false) - Featured status
- `has_24_hour_care` (boolean, optional, default: false) - 24-hour care availability

**Response:** `201 Created`

Same format as Get Listing by ID response.

**Error Responses:**
- `400 Bad Request` - Invalid request data
- `403 Forbidden` - Insufficient permissions (Provider only)

---

### Update Listing

Update listing information.

**Endpoint:** `PUT /api/v1/listings/{listing_id}`

**Authentication:** Required (Bearer token, Provider role)

**Path Parameters:**
- `listing_id` (UUID, required) - Listing ID

**Request Body:**
```json
{
  "title": "Sunset Senior Living Updated",
  "description": "Updated description...",
  "price": 4800.00,
  "available_beds": 10
}
```

**Request Fields:** (All optional)
- All fields from Create Listing are optional for updates
- `status` (string, optional) - Status: `ACTIVE`, `INACTIVE`, `PENDING`, `SUSPENDED`

**Response:** `200 OK`

Same format as Get Listing by ID response.

**Error Responses:**
- `404 Not Found` - Listing not found
- `400 Bad Request` - Invalid request data
- `403 Forbidden` - Insufficient permissions

---

### Activate Listing

Admin endpoint to activate a listing.

**Endpoint:** `POST /api/v1/listings/{listing_id}/activate`

**Authentication:** Required (Bearer token, Admin role)

**Path Parameters:**
- `listing_id` (UUID, required) - Listing ID

**Example Request:**
```
POST /api/v1/listings/123e4567-e89b-12d3-a456-426614174000/activate
```

**Response:** `200 OK`

Same format as Get Listing by ID response, with `status: "ACTIVE"`.

**Error Responses:**
- `404 Not Found` - Listing not found
- `403 Forbidden` - Insufficient permissions (Admin only)

---

### Feature Listing

Toggle featured status of a listing.

**Endpoint:** `POST /api/v1/listings/{listing_id}/feature`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `listing_id` (UUID, required) - Listing ID

**Query Parameters:**
- `is_featured` (boolean, optional, default: true) - Featured status

**Example Request:**
```
POST /api/v1/listings/123e4567-e89b-12d3-a456-426614174000/feature?is_featured=true
```

**Response:** `200 OK`

Same format as Get Listing by ID response.

**Error Responses:**
- `404 Not Found` - Listing not found

---

### Delete Listing

Delete a listing.

**Endpoint:** `DELETE /api/v1/listings/{listing_id}`

**Authentication:** Required (Bearer token, Provider role)

**Path Parameters:**
- `listing_id` (UUID, required) - Listing ID

**Example Request:**
```
DELETE /api/v1/listings/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Listing not found
- `403 Forbidden` - Insufficient permissions

---

## Care Types

- `ASSISTED_LIVING` - Assisted living facility
- `MEMORY_CARE` - Memory care facility
- `INDEPENDENT_LIVING` - Independent living facility
- `ADULT_FAMILY_HOME` - Adult family home
- `SKILLED_NURSING` - Skilled nursing facility

## Room Types

- `PRIVATE` - Private room
- `SEMI_PRIVATE` - Semi-private room
- `SHARED` - Shared room

## Listing Status

- `ACTIVE` - Active and visible
- `INACTIVE` - Inactive/hidden
- `PENDING` - Pending admin approval
- `SUSPENDED` - Suspended by admin

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Search listings
async function searchListings(filters: {
  city?: string;
  care_type?: string;
  min_price?: number;
  max_price?: number;
  skip?: number;
  limit?: number;
}) {
  const params = new URLSearchParams();
  if (filters.city) params.append('city', filters.city);
  if (filters.care_type) params.append('care_type', filters.care_type);
  if (filters.min_price) params.append('min_price', filters.min_price.toString());
  if (filters.max_price) params.append('max_price', filters.max_price.toString());
  if (filters.skip) params.append('skip', filters.skip.toString());
  if (filters.limit) params.append('limit', filters.limit.toString());
  
  const response = await fetch(`${BASE_URL}/listings?${params}`);
  return response.json();
}

// Get featured listings
async function getFeaturedListings(limit: number = 10) {
  const response = await fetch(`${BASE_URL}/listings/featured?limit=${limit}`);
  return response.json();
}

// Get listing details
async function getListing(listingId: string) {
  const response = await fetch(`${BASE_URL}/listings/${listingId}`);
  return response.json();
}

// Create listing (Provider only)
async function createListing(listingData: any) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/listings`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(listingData)
  });
  
  if (!response.ok) {
    throw new Error('Failed to create listing');
  }
  
  return response.json();
}
```


