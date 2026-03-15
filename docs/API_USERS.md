# Users API

User profile management endpoints.

**Base Path:** `/api/v1/users`

## Endpoints

### List Users

Get a paginated list of all users.

**Endpoint:** `GET /api/v1/users`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/users?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "role": "FAMILY",
    "is_active": true,
    "email_verified_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get User by ID

Get a specific user by their ID.

**Endpoint:** `GET /api/v1/users/{user_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `user_id` (UUID, required) - User ID

**Example Request:**
```
GET /api/v1/users/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "role": "FAMILY",
  "is_active": true,
  "email_verified_at": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

### Update User

Update user profile information.

**Endpoint:** `PUT /api/v1/users/{user_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `user_id` (UUID, required) - User ID

**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "phone": "+9876543210",
  "is_active": true
}
```

**Request Fields:**
- `full_name` (string, optional) - User's full name
- `phone` (string, optional) - Phone number
- `is_active` (boolean, optional) - Whether account is active

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "phone": "+9876543210",
  "role": "FAMILY",
  "is_active": true,
  "email_verified_at": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - User not found
- `400 Bad Request` - Invalid request data

---

### Delete User

Delete a user account.

**Endpoint:** `DELETE /api/v1/users/{user_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `user_id` (UUID, required) - User ID

**Example Request:**
```
DELETE /api/v1/users/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - User not found

---

## User Roles

The following roles are available:

- `FAMILY` - Family member searching for senior housing
- `SENIOR` - Senior searching for housing
- `PROVIDER` - Housing facility provider
- `ADMIN` - Platform administrator

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Get user profile
async function getUserProfile(userId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/users/${userId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  
  return response.json();
}

// Update user profile
async function updateUserProfile(userId: string, updates: {
  full_name?: string;
  phone?: string;
  is_active?: boolean;
}) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  
  if (!response.ok) {
    throw new Error('Failed to update user');
  }
  
  return response.json();
}
```


