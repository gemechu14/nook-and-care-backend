# Favorites API

Save and manage favorite listings.

**Base Path:** `/api/v1/favorites`

## Endpoints

### List Favorites

Get a paginated list of all favorites.

**Endpoint:** `GET /api/v1/favorites`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/favorites?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "223e4567-e89b-12d3-a456-426614174000",
    "listing_id": "323e4567-e89b-12d3-a456-426614174000",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Favorite by ID

Get a specific favorite by its ID.

**Endpoint:** `GET /api/v1/favorites/{favorite_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `favorite_id` (UUID, required) - Favorite ID

**Example Request:**
```
GET /api/v1/favorites/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "listing_id": "323e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Favorite not found

---

### Add Favorite

Add a listing to favorites.

**Endpoint:** `POST /api/v1/favorites`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "user_id": "223e4567-e89b-12d3-a456-426614174000",
  "listing_id": "323e4567-e89b-12d3-a456-426614174000"
}
```

**Request Fields:**
- `user_id` (UUID, required) - User ID
- `listing_id` (UUID, required) - Listing ID

**Response:** `201 Created`

Same format as Get Favorite by ID response.

**Error Responses:**
- `400 Bad Request` - Listing already in favorites or invalid data

---

### Remove Favorite

Remove a listing from favorites.

**Endpoint:** `DELETE /api/v1/favorites/{favorite_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `favorite_id` (UUID, required) - Favorite ID

**Example Request:**
```
DELETE /api/v1/favorites/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Favorite not found

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Add listing to favorites
async function addFavorite(userId: string, listingId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/favorites`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      listing_id: listingId
    })
  });
  
  if (!response.ok) {
    if (response.status === 400) {
      throw new Error('Listing already in favorites');
    }
    throw new Error('Failed to add favorite');
  }
  
  return response.json();
}

// Get user's favorites
async function getUserFavorites(userId: string, skip: number = 0, limit: number = 20) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/favorites?skip=${skip}&limit=${limit}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  const favorites = await response.json();
  
  // Filter by user_id client-side if backend doesn't support filtering
  return favorites.filter((fav: any) => fav.user_id === userId);
}

// Check if listing is favorited
async function isListingFavorited(userId: string, listingId: string): Promise<boolean> {
  const favorites = await getUserFavorites(userId);
  return favorites.some((fav: any) => fav.listing_id === listingId);
}

// Remove favorite
async function removeFavorite(favoriteId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/favorites/${favoriteId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to remove favorite');
  }
}

// Toggle favorite
async function toggleFavorite(userId: string, listingId: string) {
  try {
    // Try to add favorite
    return await addFavorite(userId, listingId);
  } catch (error: any) {
    if (error.message.includes('already in favorites')) {
      // If already favorited, find and remove it
      const favorites = await getUserFavorites(userId);
      const favorite = favorites.find((fav: any) => fav.listing_id === listingId);
      if (favorite) {
        await removeFavorite(favorite.id);
        return null; // Removed
      }
    }
    throw error;
  }
}
```





