# Reviews API

Reviews and ratings endpoints for listings.

**Base Path:** `/api/v1/reviews`

## Endpoints

### List Reviews

Get a paginated list of all reviews.

**Endpoint:** `GET /api/v1/reviews`

**Authentication:** Not required (public endpoint)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/reviews?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "tour_id": "323e4567-e89b-12d3-a456-426614174000",
    "listing_id": "223e4567-e89b-12d3-a456-426614174000",
    "user_id": "423e4567-e89b-12d3-a456-426614174000",
    "rating": 5,
    "comment": "Excellent facility with caring staff!",
    "response_from_provider": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Review by ID

Get a specific review by its ID.

**Endpoint:** `GET /api/v1/reviews/{review_id}`

**Authentication:** Not required (public endpoint)

**Path Parameters:**
- `review_id` (UUID, required) - Review ID

**Example Request:**
```
GET /api/v1/reviews/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "tour_id": "323e4567-e89b-12d3-a456-426614174000",
  "listing_id": "223e4567-e89b-12d3-a456-426614174000",
  "user_id": "423e4567-e89b-12d3-a456-426614174000",
  "rating": 5,
  "comment": "Excellent facility with caring staff!",
  "response_from_provider": "Thank you for your kind words!",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Review not found

---

### Create Review

Create a new review for a listing.

**Endpoint:** `POST /api/v1/reviews`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "tour_id": "323e4567-e89b-12d3-a456-426614174000",
  "listing_id": "223e4567-e89b-12d3-a456-426614174000",
  "user_id": "423e4567-e89b-12d3-a456-426614174000",
  "rating": 5,
  "comment": "Excellent facility with caring staff!"
}
```

**Request Fields:**
- `listing_id` (UUID, required) - Listing ID
- `rating` (integer, required) - Rating from 1 to 5
- `comment` (string, optional) - Review comment
- `tour_id` (UUID, optional) - Associated tour ID (if review is after a tour)
- `user_id` (UUID, required) - User ID writing the review

**Response:** `201 Created`

Same format as Get Review by ID response.

**Error Responses:**
- `400 Bad Request` - Invalid request data (e.g., rating out of range)

---

### Update Review

Update a review (user can update their own review, provider can add response).

**Endpoint:** `PUT /api/v1/reviews/{review_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `review_id` (UUID, required) - Review ID

**Request Body:**
```json
{
  "rating": 4,
  "comment": "Updated comment",
  "response_from_provider": "Thank you for your feedback!"
}
```

**Request Fields:** (All optional)
- `rating` (integer, optional) - Rating from 1 to 5
- `comment` (string, optional) - Review comment
- `response_from_provider` (string, optional) - Provider response (Provider only)

**Response:** `200 OK`

Same format as Get Review by ID response.

**Error Responses:**
- `404 Not Found` - Review not found
- `400 Bad Request` - Invalid request data
- `403 Forbidden` - Insufficient permissions

---

### Delete Review

Delete a review.

**Endpoint:** `DELETE /api/v1/reviews/{review_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `review_id` (UUID, required) - Review ID

**Example Request:**
```
DELETE /api/v1/reviews/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Review not found
- `403 Forbidden` - Insufficient permissions (can only delete own reviews)

---

## Rating Scale

Ratings must be integers from 1 to 5:
- `1` - Poor
- `2` - Fair
- `3` - Good
- `4` - Very Good
- `5` - Excellent

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Create a review
async function createReview(
  listingId: string,
  userId: string,
  rating: number,
  comment?: string,
  tourId?: string
) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/reviews`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      listing_id: listingId,
      user_id: userId,
      rating,
      comment,
      tour_id: tourId
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to create review');
  }
  
  return response.json();
}

// Get reviews for a listing (you may need to filter client-side)
async function getReviewsForListing(listingId: string, skip: number = 0, limit: number = 20) {
  const response = await fetch(`${BASE_URL}/reviews?skip=${skip}&limit=${limit}`);
  const reviews = await response.json();
  
  // Filter by listing_id client-side if backend doesn't support filtering
  return reviews.filter((review: any) => review.listing_id === listingId);
}

// Add provider response to review
async function addProviderResponse(reviewId: string, response: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const fetchResponse = await fetch(`${BASE_URL}/reviews/${reviewId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      response_from_provider: response
    })
  });
  
  if (!fetchResponse.ok) {
    throw new Error('Failed to add provider response');
  }
  
  return fetchResponse.json();
}
```






