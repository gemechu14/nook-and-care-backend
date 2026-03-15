# Payments API

Payment processing endpoints for providers.

**Base Path:** `/api/v1/payments`

## Endpoints

### List Payments

Get a paginated list of all payments.

**Endpoint:** `GET /api/v1/payments`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 20, max: 100) - Number of records to return

**Example Request:**
```
GET /api/v1/payments?skip=0&limit=20
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "provider_id": "223e4567-e89b-12d3-a456-426614174000",
    "amount": 99.00,
    "currency": "USD",
    "payment_method": "CREDIT_CARD",
    "transaction_id": "txn_1234567890",
    "status": "COMPLETED",
    "processed_at": "2024-01-01T12:00:00Z",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Payment by ID

Get a specific payment by its ID.

**Endpoint:** `GET /api/v1/payments/{payment_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `payment_id` (UUID, required) - Payment ID

**Example Request:**
```
GET /api/v1/payments/123e4567-e89b-12d3-a456-426614174000
```

**Response:** `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "amount": 99.00,
  "currency": "USD",
  "payment_method": "CREDIT_CARD",
  "transaction_id": "txn_1234567890",
  "status": "COMPLETED",
  "processed_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Payment not found

---

### Create Payment

Create a new payment record.

**Endpoint:** `POST /api/v1/payments`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "provider_id": "223e4567-e89b-12d3-a456-426614174000",
  "amount": 99.00,
  "currency": "USD",
  "payment_method": "CREDIT_CARD",
  "transaction_id": "txn_1234567890"
}
```

**Request Fields:**
- `provider_id` (UUID, required) - Provider ID
- `amount` (float, required) - Payment amount
- `currency` (string, optional, default: "USD") - Currency code
- `payment_method` (string, required) - Payment method: `CREDIT_CARD`, `PAYPAL`, or `BANK_TRANSFER`
- `transaction_id` (string, optional) - External transaction ID

**Response:** `201 Created`

Same format as Get Payment by ID response, with `status: "PENDING"`.

**Error Responses:**
- `400 Bad Request` - Invalid request data

---

### Update Payment

Update payment information (typically to update status after processing).

**Endpoint:** `PUT /api/v1/payments/{payment_id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `payment_id` (UUID, required) - Payment ID

**Request Body:**
```json
{
  "status": "COMPLETED",
  "transaction_id": "txn_1234567890",
  "processed_at": "2024-01-01T12:00:00Z"
}
```

**Request Fields:** (All optional)
- `status` (string, optional) - Payment status
- `transaction_id` (string, optional) - External transaction ID
- `processed_at` (datetime, optional) - Processing timestamp (ISO 8601)

**Response:** `200 OK`

Same format as Get Payment by ID response.

**Error Responses:**
- `404 Not Found` - Payment not found
- `400 Bad Request` - Invalid request data

---

## Payment Methods

- `CREDIT_CARD` - Credit card payment
- `PAYPAL` - PayPal payment
- `BANK_TRANSFER` - Bank transfer

## Payment Status

- `PENDING` - Payment pending processing
- `COMPLETED` - Payment completed successfully
- `FAILED` - Payment failed
- `REFUNDED` - Payment refunded

---

## Frontend Integration Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';

// Create payment record
async function createPayment(
  providerId: string,
  amount: number,
  paymentMethod: 'CREDIT_CARD' | 'PAYPAL' | 'BANK_TRANSFER',
  transactionId?: string
) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/payments`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      provider_id: providerId,
      amount,
      payment_method: paymentMethod,
      currency: 'USD',
      transaction_id: transactionId
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to create payment');
  }
  
  return response.json();
}

// Get provider's payments
async function getProviderPayments(providerId: string, skip: number = 0, limit: number = 20) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/payments?skip=${skip}&limit=${limit}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  
  const payments = await response.json();
  
  // Filter by provider_id client-side if backend doesn't support filtering
  return payments.filter((payment: any) => payment.provider_id === providerId);
}

// Update payment status
async function updatePaymentStatus(
  paymentId: string,
  status: 'PENDING' | 'COMPLETED' | 'FAILED' | 'REFUNDED',
  transactionId?: string
) {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/payments/${paymentId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      status,
      transaction_id: transactionId,
      processed_at: new Date().toISOString()
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to update payment');
  }
  
  return response.json();
}
```




