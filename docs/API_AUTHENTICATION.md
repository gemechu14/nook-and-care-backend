# Authentication API

Authentication endpoints for user registration, login, token management, and profile access.

**Base Path:** `/api/v1/auth`

## Endpoints

### Register User

Register a new user account.

**Endpoint:** `POST /api/v1/auth/register`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "role": "FAMILY"
}
```

**Request Fields:**
- `email` (string, required) - Valid email address
- `password` (string, required) - Password (min length enforced by backend)
- `full_name` (string, required) - User's full name
- `phone` (string, optional) - Phone number
- `role` (string, optional) - User role: `FAMILY`, `SENIOR`, `PROVIDER`, or `ADMIN` (default: `FAMILY`)

**Response:** `201 Created`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

**Response Fields:**
- `access_token` (string) - JWT access token (expires in 60 minutes)
- `refresh_token` (string) - Refresh token (expires in 30 days)
- `token_type` (string) - Always "bearer"

---

### Login

Login with email and password.

**Endpoint:** `POST /api/v1/auth/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Request Fields:**
- `email` (string, required) - User email
- `password` (string, required) - User password

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid email or password

---

### Refresh Access Token

Get a new access token using a valid refresh token.

**Endpoint:** `POST /api/v1/auth/refresh`

**Authentication:** Not required

**Request Body:**
```json
{
  "refresh_token": "xYz123abc..."
}
```

**Request Fields:**
- `refresh_token` (string, required) - Valid refresh token

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

---

### Logout

Logout by revoking the refresh token.

**Endpoint:** `POST /api/v1/auth/logout`

**Authentication:** Not required

**Request Body:**
```json
{
  "refresh_token": "xYz123abc..."
}
```

**Request Fields:**
- `refresh_token` (string, required) - Refresh token to revoke

**Response:** `204 No Content`

---

### Get Current User

Get the currently authenticated user's profile.

**Endpoint:** `GET /api/v1/auth/me`

**Authentication:** Required (Bearer token)

**Headers:**
```
Authorization: Bearer <access_token>
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

**Response Fields:**
- `id` (UUID) - User ID
- `email` (string) - User email
- `full_name` (string) - User's full name
- `phone` (string, nullable) - Phone number
- `role` (string) - User role: `FAMILY`, `SENIOR`, `PROVIDER`, or `ADMIN`
- `is_active` (boolean) - Whether account is active
- `email_verified_at` (datetime, nullable) - Email verification timestamp
- `created_at` (datetime) - Account creation timestamp
- `updated_at` (datetime) - Last update timestamp

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - User not found

---

## Token Details

### Access Token
- **Type:** JWT (JSON Web Token)
- **Expiry:** 60 minutes (configurable)
- **Usage:** Include in `Authorization: Bearer <token>` header
- **Payload:** Contains user ID (`sub` claim)

### Refresh Token
- **Type:** Cryptographically secure random string (43 characters)
- **Expiry:** 30 days (configurable)
- **Storage:** Stored in database
- **Usage:** Exchange for new access token when current one expires
- **Revocable:** Can be revoked on logout or password change

---

## Frontend Integration Example

### JavaScript/TypeScript

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Login
async function login(email: string, password: string) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const { access_token, refresh_token } = await response.json();
  
  // Store tokens
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', refresh_token);
  
  return { access_token, refresh_token };
}

// Get current user
async function getCurrentUser() {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (response.status === 401) {
    // Token expired, refresh it
    await refreshAccessToken();
    return getCurrentUser(); // Retry
  }
  
  return response.json();
}

// Refresh access token
async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch(`${BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  
  if (!response.ok) {
    // Refresh token expired, redirect to login
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
    return;
  }
  
  const { access_token, refresh_token } = await response.json();
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', refresh_token);
  
  return access_token;
}

// Logout
async function logout() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  await fetch(`${BASE_URL}/auth/logout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
```

---

## Error Handling

All endpoints may return the following errors:

- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Invalid credentials or expired token
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message description"
}
```


