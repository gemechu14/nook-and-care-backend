# Catalog APIs

Reference data endpoints for master lookup tables. These endpoints serve all the catalog data (amenities, activities, languages, certifications, etc.) that listings can reference.

**Base Path:** `/api/v1`

## Overview

All catalog endpoints follow a similar pattern:
- `GET /{resource}` - List all items (paginated)
- `GET /{resource}/{id}` - Get item by ID (where applicable)
- `POST /{resource}` - Create item (Admin only)
- `PUT /{resource}/{id}` - Update item (Admin only)
- `DELETE /{resource}/{id}` - Delete item (Admin only)

---

## Amenities

**Base Path:** `/api/v1/amenities`

### List Amenities

**Endpoint:** `GET /api/v1/amenities`

**Query Parameters:**
- `skip` (integer, optional, default: 0)
- `limit` (integer, optional, default: 20, max: 100)

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Swimming Pool",
    "category": "PREMIUM",
    "icon": "pool",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Amenity ID
- `name` (string) - Amenity name
- `category` (string) - Category: `BASIC`, `PREMIUM`, `SAFETY`, `ACCESSIBILITY`
- `icon` (string, nullable) - Icon identifier
- `created_at` (datetime) - Creation timestamp

### Get Amenity by ID

**Endpoint:** `GET /api/v1/amenities/{amenity_id}`

### Create Amenity

**Endpoint:** `POST /api/v1/amenities`

**Request Body:**
```json
{
  "name": "WiFi",
  "category": "BASIC",
  "icon": "wifi"
}
```

### Update Amenity

**Endpoint:** `PUT /api/v1/amenities/{amenity_id}`

### Delete Amenity

**Endpoint:** `DELETE /api/v1/amenities/{amenity_id}`

---

## Activities

**Base Path:** `/api/v1/activities`

### List Activities

**Endpoint:** `GET /api/v1/activities`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Gardening",
    "category": "RECREATIONAL",
    "description": "Outdoor gardening activities",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Activity ID
- `name` (string) - Activity name
- `category` (string) - Category: `RECREATIONAL`, `SOCIAL`, `FITNESS`, `EDUCATIONAL`
- `description` (string, nullable) - Activity description
- `created_at` (datetime) - Creation timestamp

### Get Activity by ID

**Endpoint:** `GET /api/v1/activities/{activity_id}`

### Create Activity

**Endpoint:** `POST /api/v1/activities`

**Request Body:**
```json
{
  "name": "Game Nights",
  "category": "SOCIAL",
  "description": "Weekly game nights with residents"
}
```

### Update Activity

**Endpoint:** `PUT /api/v1/activities/{activity_id}`

### Delete Activity

**Endpoint:** `DELETE /api/v1/activities/{activity_id}`

---

## Languages

**Base Path:** `/api/v1/languages`

### List Languages

**Endpoint:** `GET /api/v1/languages`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "code": "en",
    "name": "English",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Language ID
- `code` (string) - ISO language code (e.g., "en", "es", "fr")
- `name` (string) - Language name
- `created_at` (datetime) - Creation timestamp

### Create Language

**Endpoint:** `POST /api/v1/languages`

**Request Body:**
```json
{
  "code": "es",
  "name": "Spanish"
}
```

### Update Language

**Endpoint:** `PUT /api/v1/languages/{language_id}`

### Delete Language

**Endpoint:** `DELETE /api/v1/languages/{language_id}`

---

## Certifications

**Base Path:** `/api/v1/certifications`

### List Certifications

**Endpoint:** `GET /api/v1/certifications`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "State Licensed",
    "description": "Licensed by state health department",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Certification ID
- `name` (string) - Certification name
- `description` (string, nullable) - Certification description
- `created_at` (datetime) - Creation timestamp

### Create Certification

**Endpoint:** `POST /api/v1/certifications`

**Request Body:**
```json
{
  "name": "Medicare Certified",
  "description": "Certified by Medicare"
}
```

### Update Certification

**Endpoint:** `PUT /api/v1/certifications/{cert_id}`

### Delete Certification

**Endpoint:** `DELETE /api/v1/certifications/{cert_id}`

---

## Dining Options

**Base Path:** `/api/v1/dining-options`

### List Dining Options

**Endpoint:** `GET /api/v1/dining-options`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Three home-cooked meals daily",
    "description": "Three nutritious meals prepared daily",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Dining option ID
- `name` (string) - Dining option name
- `description` (string, nullable) - Description
- `created_at` (datetime) - Creation timestamp

### Create Dining Option

**Endpoint:** `POST /api/v1/dining-options`

**Request Body:**
```json
{
  "name": "Special dietary accommodations",
  "description": "Accommodations for special dietary needs"
}
```

### Update Dining Option

**Endpoint:** `PUT /api/v1/dining-options/{dining_id}`

### Delete Dining Option

**Endpoint:** `DELETE /api/v1/dining-options/{dining_id}`

---

## Safety Features

**Base Path:** `/api/v1/safety-features`

### List Safety Features

**Endpoint:** `GET /api/v1/safety-features`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Emergency call system",
    "category": "EMERGENCY",
    "description": "24/7 emergency call system in all rooms",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Safety feature ID
- `name` (string) - Safety feature name
- `category` (string) - Category: `EMERGENCY`, `FIRE`, `ACCESSIBILITY`, `MEDICAL`
- `description` (string, nullable) - Description
- `created_at` (datetime) - Creation timestamp

### Create Safety Feature

**Endpoint:** `POST /api/v1/safety-features`

**Request Body:**
```json
{
  "name": "Fire safety",
  "category": "FIRE",
  "description": "Fire safety systems and protocols"
}
```

### Update Safety Feature

**Endpoint:** `PUT /api/v1/safety-features/{sf_id}`

### Delete Safety Feature

**Endpoint:** `DELETE /api/v1/safety-features/{sf_id}`

---

## Insurance Options

**Base Path:** `/api/v1/insurance-options`

### List Insurance Options

**Endpoint:** `GET /api/v1/insurance-options`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Medicare",
    "description": "Accepts Medicare insurance",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Insurance option ID
- `name` (string) - Insurance option name
- `description` (string, nullable) - Description
- `created_at` (datetime) - Creation timestamp

### Create Insurance Option

**Endpoint:** `POST /api/v1/insurance-options`

**Request Body:**
```json
{
  "name": "Private insurance",
  "description": "Accepts private insurance plans"
}
```

### Update Insurance Option

**Endpoint:** `PUT /api/v1/insurance-options/{ins_id}`

### Delete Insurance Option

**Endpoint:** `DELETE /api/v1/insurance-options/{ins_id}`

---

## House Rules

**Base Path:** `/api/v1/house-rules`

### List House Rules

**Endpoint:** `GET /api/v1/house-rules`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "No smoking",
    "description": "Smoking is not allowed on premises",
    "category": "SMOKING",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - House rule ID
- `name` (string) - House rule name
- `description` (string, nullable) - Description
- `category` (string) - Category: `GENERAL`, `VISITOR`, `PET`, `SMOKING`, `QUIET_HOURS`
- `created_at` (datetime) - Creation timestamp

### Create House Rule

**Endpoint:** `POST /api/v1/house-rules`

**Request Body:**
```json
{
  "name": "Quiet hours",
  "description": "Quiet hours from 10 PM to 7 AM",
  "category": "QUIET_HOURS"
}
```

### Update House Rule

**Endpoint:** `PUT /api/v1/house-rules/{hr_id}`

### Delete House Rule

**Endpoint:** `DELETE /api/v1/house-rules/{hr_id}`

---

## Equipment

**Base Path:** `/api/v1/equipment`

### List Equipment

**Endpoint:** `GET /api/v1/equipment`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Wheelchair",
    "category": "MOBILITY",
    "description": "Wheelchair available for use",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Equipment ID
- `name` (string) - Equipment name
- `category` (string) - Equipment category
- `description` (string, nullable) - Description
- `created_at` (datetime) - Creation timestamp

### Create Equipment

**Endpoint:** `POST /api/v1/equipment`

**Request Body:**
```json
{
  "name": "Hospital bed",
  "category": "MEDICAL",
  "description": "Adjustable hospital bed"
}
```

### Update Equipment

**Endpoint:** `PUT /api/v1/equipment/{eq_id}`

### Delete Equipment

**Endpoint:** `DELETE /api/v1/equipment/{eq_id}`

---

## Treatment Services

**Base Path:** `/api/v1/treatment-services`

### List Treatment Services

**Endpoint:** `GET /api/v1/treatment-services`

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Medication management",
    "description": "Assistance with medication administration",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Fields:**
- `id` (UUID) - Treatment service ID
- `name` (string) - Service name
- `description` (string, nullable) - Description
- `created_at` (datetime) - Creation timestamp

### Create Treatment Service

**Endpoint:** `POST /api/v1/treatment-services`

**Request Body:**
```json
{
  "name": "Diabetes management",
  "description": "Specialized diabetes care and monitoring"
}
```

### Update Treatment Service

**Endpoint:** `PUT /api/v1/treatment-services/{ts_id}`

### Delete Treatment Service

**Endpoint:** `DELETE /api/v1/treatment-services/{ts_id}`

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Generic function to fetch catalog items
async function fetchCatalogItems(
  resource: string,
  skip: number = 0,
  limit: number = 100
) {
  const response = await fetch(`${BASE_URL}/${resource}?skip=${skip}&limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${resource}`);
  }
  return response.json();
}

// Fetch all amenities
async function getAmenities() {
  return fetchCatalogItems('amenities');
}

// Fetch all activities
async function getActivities() {
  return fetchCatalogItems('activities');
}

// Fetch all languages
async function getLanguages() {
  return fetchCatalogItems('languages');
}

// Fetch all certifications
async function getCertifications() {
  return fetchCatalogItems('certifications');
}

// Fetch all dining options
async function getDiningOptions() {
  return fetchCatalogItems('dining-options');
}

// Fetch all safety features
async function getSafetyFeatures() {
  return fetchCatalogItems('safety-features');
}

// Fetch all insurance options
async function getInsuranceOptions() {
  return fetchCatalogItems('insurance-options');
}

// Fetch all house rules
async function getHouseRules() {
  return fetchCatalogItems('house-rules');
}

// Fetch all equipment
async function getEquipment() {
  return fetchCatalogItems('equipment');
}

// Fetch all treatment services
async function getTreatmentServices() {
  return fetchCatalogItems('treatment-services');
}

// Usage: Load all catalog data for a listing form
async function loadAllCatalogData() {
  const [
    amenities,
    activities,
    languages,
    certifications,
    diningOptions,
    safetyFeatures,
    insuranceOptions,
    houseRules,
    equipment,
    treatmentServices
  ] = await Promise.all([
    getAmenities(),
    getActivities(),
    getLanguages(),
    getCertifications(),
    getDiningOptions(),
    getSafetyFeatures(),
    getInsuranceOptions(),
    getHouseRules(),
    getEquipment(),
    getTreatmentServices()
  ]);
  
  return {
    amenities,
    activities,
    languages,
    certifications,
    diningOptions,
    safetyFeatures,
    insuranceOptions,
    houseRules,
    equipment,
    treatmentServices
  };
}
```

---

## Notes

- All catalog endpoints are **read-only for regular users** (public endpoints)
- **Create, Update, Delete** operations require **Admin** authentication
- Catalog data is typically loaded once and cached on the frontend
- These catalogs are used to populate dropdowns and checkboxes when creating/editing listings
- Listing associations (e.g., which amenities a listing has) are managed through the Listings API, not through these catalog endpoints




