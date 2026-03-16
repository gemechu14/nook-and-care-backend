# Subscriptions API

Provider subscription plan management endpoints.

**Base Path:** `/api/v1/subscriptions`

## Endpoints

### List Subscriptions

Get a paginated list of all subscriptions.

**Endpoint:** `GET /api/v1/subscriptions`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/subscriptions?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "provider_id": "223e4567-e89b-12d3-a456-426614174000",
    "plan_type": "PRO",
    "price": 99.00,
    "billing_cycle": "MONTHLY",
    "start_date": "2024-01-01",
    "end_date": "2024-02-01",
    "status": "ACTIVE",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Subscription by ID

Get a specific subscription by its ID.

**Endpoint:** `GET /api/v1/subscriptions/{subscription_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `subscription_id` (UUID, required) - Subscription ID

**Example Request:**
```
GET /api/v1/subscriptions/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "plan_type": "PRO",
  "price": 99.00,
  "billing_cycle": "MONTHLY",
  "start_date": "2024-01-01",
  "end_date": "2024-02-01",
  "status": "ACTIVE",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Subscription not found

---

### Create Subscription

Subscribe a provider to a plan.

**Endpoint:** `POST /api/v1/subscriptions`

**Authentication:** Required (Bearer token, Provider role)

**Request Body:**
```json
{
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "plan_type": "PRO",
  "price": 99.00,
  "billing_cycle": "MONTHLY",
  "start_date": "2024-01-01",
  "end_date": "2024-02-01"
}
```

**Request Fields:**
- `provider_id` (UUID, required) - Provider ID
- `plan_type` (string, required) - Plan type: `FREE`, `PRO`, or `PREMIUM`
- `price` (float, optional) - Subscription price
- `billing_cycle` (string, optional, default: "MONTHLY") - Billing cycle: `MONTHLY` or `YEARLY`
- `start_date` (date, required) - Subscription start date (YYYY-MM-DD)
- `end_date` (date, optional) - Subscription end date (YYYY-MM-DD)

**Response:** `201 Created`

Same format as Get Subscription by ID response, with `status: "ACTIVE"`.

**Error Responses:**
- `400 Bad Request` - Invalid request data

---

### Update Subscription

Update subscription information.

**Endpoint:** `PUT /api/v1/subscriptions/{subscription_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `subscription_id` (UUID, required) - Subscription ID

**Request Body:**
```json
{
  "plan_type": "PREMIUM",
  "price": 199.00,
  "billing_cycle": "YEARLY",
  "end_date": "2025-01-01",
  "status": "ACTIVE"
}
```

**Request Fields:** (All optional)
- `plan_type` (string, optional) - Plan type
- `price` (float, optional) - Subscription price
- `billing_cycle` (string, optional) - Billing cycle
- `end_date` (date, optional) - Subscription end date
- `status` (string, optional) - Subscription status

**Response:** `200 OK`

Same format as Get Subscription by ID response.

**Error Responses:**
- `404 Not Found` - Subscription not found
- `400 Bad Request` - Invalid request data

---

### Cancel Subscription

Cancel a subscription.

**Endpoint:** `POST /api/v1/subscriptions/{subscription_id}/cancel`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `subscription_id` (UUID, required) - Subscription ID

**Example Request:**
```
POST /api/v1/subscriptions/123e4567-e89b-12d3-a456-426614174000/cancel
```

**Response:** `200 OK`

Same format as Get Subscription by ID response, with `status: "CANCELLED"`.

**Error Responses:**
- `404 Not Found` - Subscription not found

---

## Plan Types

- `FREE` - Free plan (limited listings)
- `PRO` - Pro plan (unlimited listings)
- `PREMIUM` - Premium plan (featured listings, homepage visibility, search ranking boost)

## Billing Cycles

- `MONTHLY` - Monthly billing
- `YEARLY` - Yearly billing

## Subscription Status

- `ACTIVE` - Active subscription
- `EXPIRED` - Subscription expired
- `CANCELLED` - Subscription cancelled

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Subscribe to a plan
async function subscribe(
  providerId: string,
  planType: 'FREE' | 'PRO' | 'PREMIUM',
  billingCycle: 'MONTHLY' | 'YEARLY' = 'MONTHLY',
  startDate: string,
  price?: number
) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/subscriptions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      provider_id: providerId,
      plan_type: planType,
      billing_cycle: billingCycle,
      start_date: startDate,
      price
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to subscribe');
  }
  
  return response.json();
}

// Get provider's active subscription
async function getProviderSubscription(providerId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/subscriptions?skip=0&limit=100`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  const subscriptions = await response.json();
  
  // Filter by provider_id and find active subscription
  return subscriptions.find(
    (sub: any) => sub.provider_id === providerId && sub.status === 'ACTIVE'
  );
}

// Cancel subscription
async function cancelSubscription(subscriptionId: string) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/subscriptions/${subscriptionId}/cancel`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to cancel subscription');
  }
  
  return response.json();
}
```






