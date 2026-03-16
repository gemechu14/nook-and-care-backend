# Nook and Care API Documentation

Welcome to the **Nook and Care** Senior Housing Marketplace API documentation. This documentation provides comprehensive details about all available endpoints for frontend integration.

## Base URL

```
http://localhost:8000/api/v1
```

**Production URL:** (To be configured)

## Authentication

The API uses **JWT (JSON Web Token)** authentication with refresh tokens. Most endpoints require authentication via Bearer token in the Authorization header.

### Authentication Flow

1. **Register/Login** → Receive `access_token` + `refresh_token`
2. **Use access_token** → Include in `Authorization: Bearer <access_token>` header
3. **When access_token expires** → Use `refresh_token` to get a new `access_token`
4. **Logout** → Revoke the `refresh_token`

See [Authentication API](./API_AUTHENTICATION.md) for detailed authentication endpoints.

## API Endpoints Overview

### Core APIs

- **[Authentication](./API_AUTHENTICATION.md)** - User registration, login, token management
- **[Users](./API_USERS.md)** - User profile management
- **[Providers](./API_PROVIDERS.md)** - Provider registration and management
- **[Listings](./API_LISTINGS.md)** - Senior housing facility listings
- **[Listing Images](./API_LISTING_IMAGES.md)** - Image upload and management for listings
- **[Tours](./API_TOURS.md)** - Tour booking and management
- **[Reviews](./API_REVIEWS.md)** - Reviews and ratings
- **[Favorites](./API_FAVORITES.md)** - Save favorite listings
- **[Subscriptions](./API_SUBSCRIPTIONS.md)** - Provider subscription plans
- **[Payments](./API_PAYMENTS.md)** - Payment processing
- **[Reports](./API_REPORTS.md)** - Fraud and issue reporting

### Catalog APIs (Reference Data)

- **[Amenities](./API_CATALOG.md#amenities)** - Facility amenities catalog
- **[Activities](./API_CATALOG.md#activities)** - Activities and programs catalog
- **[Languages](./API_CATALOG.md#languages)** - Supported languages catalog
- **[Certifications](./API_CATALOG.md#certifications)** - Certifications and licenses catalog
- **[Dining Options](./API_CATALOG.md#dining-options)** - Dining options catalog
- **[Safety Features](./API_CATALOG.md#safety-features)** - Safety features catalog
- **[Insurance Options](./API_CATALOG.md#insurance-options)** - Insurance and payment options catalog
- **[House Rules](./API_CATALOG.md#house-rules)** - House rules catalog
- **[Equipment](./API_CATALOG.md#equipment)** - Equipment catalog
- **[Treatment Services](./API_CATALOG.md#treatment-services)** - Treatment services catalog

## Common Request/Response Patterns

### Pagination

Most list endpoints support pagination via query parameters:

- `skip` (default: 0) - Number of records to skip
- `limit` (default: 20, max: 100) - Number of records to return

**Example:**
```
GET /api/v1/listings?skip=0&limit=20
```

### Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

### UUID Format

All IDs are UUIDs (Universally Unique Identifiers) in the format:
```
123e4567-e89b-12d3-a456-426614174000
```

## Rate Limiting

(To be implemented - currently no rate limiting)

## CORS

CORS is enabled for configured origins. Check with backend team for allowed origins.

## Swagger Documentation

Interactive API documentation is available at:
- **Swagger UI:** `http://localhost:8000/swagger`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

## Support

For questions or issues, contact the backend development team.

---

**Last Updated:** 2024
**API Version:** v1






