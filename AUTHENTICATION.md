# Authentication Guide

The API uses JWT-based authentication with refresh tokens for secure, long-lived sessions.

## Authentication Flow

1. **Register/Login** → Receive `access_token` + `refresh_token`
2. **Use access_token** → Include in `Authorization: Bearer <access_token>` header
3. **When access_token expires** → Use `refresh_token` to get a new `access_token`
4. **Logout** → Revoke the `refresh_token`

## API Endpoints

### Register

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "role": "FAMILY"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

### Login

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

### Refresh Access Token

```bash
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "xYz123abc..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xYz123abc...",
  "token_type": "bearer"
}
```

### Logout

```bash
POST /api/v1/auth/logout
Content-Type: application/json

{
  "refresh_token": "xYz123abc..."
}
```

**Response:** `204 No Content`

### Get Current User

```bash
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "FAMILY",
  "is_active": true,
  ...
}
```

## Token Details

### Access Token
- **Type:** JWT (JSON Web Token)
- **Expiry:** 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Usage:** Include in `Authorization` header for authenticated requests
- **Payload:** Contains user ID (`sub` claim)

### Refresh Token
- **Type:** Cryptographically secure random string (43 characters)
- **Expiry:** 30 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- **Storage:** Stored in database (`refresh_tokens` table)
- **Usage:** Exchange for new access token when current one expires
- **Revocable:** Can be revoked on logout or password change

## Usage Examples

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "user@example.com",
        "password": "SecurePassword123!"
    }
)
tokens = response.json()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]

# Use access token
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
user = response.json()

# Refresh access token when expired
response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": refresh_token}
)
new_tokens = response.json()
access_token = new_tokens["access_token"]

# Logout
requests.post(
    f"{BASE_URL}/auth/logout",
    json={"refresh_token": refresh_token}
)
```

### JavaScript (fetch)

```javascript
const BASE_URL = 'http://localhost:8000/api/v1';

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePassword123!'
  })
});
const { access_token, refresh_token } = await loginResponse.json();

// Store tokens (e.g., in localStorage)
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);

// Use access token
const meResponse = await fetch(`${BASE_URL}/auth/me`, {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});
const user = await meResponse.json();

// Refresh access token
async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  const response = await fetch(`${BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  const { access_token } = await response.json();
  localStorage.setItem('access_token', access_token);
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

### Axios Interceptor (Auto-refresh)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// Add access token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Refresh token on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post(
            'http://localhost:8000/api/v1/auth/refresh',
            { refresh_token: refreshToken }
          );
          localStorage.setItem('access_token', data.access_token);
          // Retry original request
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return axios.request(error.config);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

## Security Best Practices

1. **Store tokens securely:**
   - **Browser:** Use `httpOnly` cookies (recommended) or `localStorage` (less secure)
   - **Mobile:** Use secure storage (Keychain/Keystore)
   - **Never** store tokens in plain text or commit to version control

2. **HTTPS only:** Always use HTTPS in production

3. **Token rotation:** Consider rotating refresh tokens on each refresh (not implemented by default)

4. **Revoke on password change:** When a user changes their password, revoke all refresh tokens

5. **Short access token expiry:** Keep access tokens short-lived (default: 60 minutes)

6. **Monitor token usage:** Log and monitor refresh token usage for security

## Environment Variables

```env
ACCESS_TOKEN_EXPIRE_MINUTES=60      # Access token lifetime
REFRESH_TOKEN_EXPIRE_DAYS=30        # Refresh token lifetime
SECRET_KEY=<random-32-byte-hex>     # JWT signing key
```

## Database Schema

Refresh tokens are stored in the `refresh_tokens` table:

- `id` (UUID, PK)
- `user_id` (UUID, FK → users.id)
- `token` (TEXT, UNIQUE) - The refresh token string
- `expires_at` (TIMESTAMP) - Expiration datetime
- `is_revoked` (BOOLEAN) - Whether token has been revoked
- `created_at` (TIMESTAMP)

## Migration

After adding refresh tokens, run:

```bash
alembic revision --autogenerate -m "add refresh tokens"
alembic upgrade head
```







