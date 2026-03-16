# Nook and Care User Guide

This guide explains what each user role can do in the Nook and Care platform and how to use the system effectively.

## User Roles

The platform supports three main user roles:

- **FAMILY / SENIOR** - Families and seniors searching for senior housing facilities
- **PROVIDER** - Housing facility owners who list and manage their facilities
- **ADMIN** - Platform administrators who verify providers and moderate content

---

## FAMILY / SENIOR User Guide

### Overview

As a **Family member or Senior**, you can search for verified senior housing facilities, book tours, save favorites, and leave reviews.

### Getting Started

1. **Sign Up / Register**
   - Create an account with email and password
   - Choose role: `FAMILY` or `SENIOR`
   - Complete your profile with name and phone number

2. **Login**
   - Use your email and password to login
   - Receive access token and refresh token
   - Access token expires in 60 minutes (use refresh token to renew)

### What You Can Do

#### 1. Search and Discover Listings

**Public Access (No Login Required):**
- Browse all active listings
- View featured listings on homepage
- Search listings by:
  - City/Location
  - Care type (Assisted Living, Memory Care, Independent Living, etc.)
  - Price range (min/max)
  - Room type (Private, Semi-Private, Shared)

**API Endpoints:**
- `GET /api/v1/listings` - Search and filter listings
- `GET /api/v1/listings/featured` - Get featured listings
- `GET /api/v1/listings/{listing_id}` - View listing details

**Example Workflow:**
```
1. Search for listings in "Los Angeles"
2. Filter by care type: "ASSISTED_LIVING"
3. Set price range: $3000 - $5000
4. Browse results
5. Click on a listing to view full details
```

#### 2. View Listing Details

**What You Can See:**
- Facility title and description
- Care type and room types available
- Location (address, city, coordinates)
- Pricing information
- Capacity and available beds
- Staff ratio
- Contact information (phone, email)
- License number
- Facility images
- Amenities (pool, WiFi, parking, etc.)
- Treatment services offered
- Equipment available
- Languages supported
- Certifications (State licensed, Medicare certified, etc.)
- Activities and programs
- Dining options
- Safety features
- Insurance options accepted
- House rules
- Reviews and ratings

**API Endpoints:**
- `GET /api/v1/listings/{listing_id}` - Get full listing details
- `GET /api/v1/listing-images/listing/{listing_id}` - Get listing images
- `GET /api/v1/reviews` - Get reviews (filter by listing_id client-side)

#### 3. Save Favorite Listings

**Requires Login:**
- Save listings you want to revisit later
- Compare multiple favorites side-by-side
- Access your favorites anytime

**API Endpoints:**
- `POST /api/v1/favorites` - Add listing to favorites
- `GET /api/v1/favorites` - View your favorites
- `DELETE /api/v1/favorites/{favorite_id}` - Remove from favorites

**Example Workflow:**
```
1. Browse listings
2. Find a listing you like
3. Click "Add to Favorites"
4. Listing is saved to your account
5. View all favorites from your profile
6. Compare favorites side-by-side
```

#### 4. Book Tours

**Requires Login:**
- Book in-person or virtual tours
- Select preferred date and time
- Track tour status (Pending, Approved, Scheduled, Completed, Cancelled)

**API Endpoints:**
- `POST /api/v1/tours` - Book a tour
- `GET /api/v1/tours/{tour_id}` - View tour details
- `GET /api/v1/tours` - View all your tours
- `POST /api/v1/tours/{tour_id}/cancel` - Cancel a tour

**Example Workflow:**
```
1. View listing details
2. Click "Book a Tour"
3. Choose tour type: IN_PERSON or VIRTUAL
4. Select date and time
5. Submit tour request
6. Tour status: PENDING (waiting for provider approval)
7. Provider approves → Status: APPROVED
8. Tour confirmed → Status: SCHEDULED
9. Attend tour → Status: COMPLETED
```

#### 5. Leave Reviews and Ratings

**Requires Login:**
- Rate facilities from 1 to 5 stars
- Write detailed comments about your experience
- Reviews can be linked to completed tours
- View provider responses to your reviews

**API Endpoints:**
- `POST /api/v1/reviews` - Create a review
- `GET /api/v1/reviews/{review_id}` - View review details
- `PUT /api/v1/reviews/{review_id}` - Update your review
- `DELETE /api/v1/reviews/{review_id}` - Delete your review

**Example Workflow:**
```
1. Complete a tour
2. Visit listing page
3. Click "Write a Review"
4. Rate facility (1-5 stars)
5. Write comment about your experience
6. Optionally link to completed tour
7. Submit review
8. Review appears on listing page
9. Provider can respond to your review
```

#### 6. Report Issues

**Requires Login:**
- Report fake listings
- Report scam providers
- Report misleading images
- Report general fraud

**API Endpoints:**
- `POST /api/v1/reports` - File a report
- `GET /api/v1/reports/{report_id}` - View report status

**Example Workflow:**
```
1. Notice suspicious listing or provider
2. Click "Report" button
3. Select report type:
   - FAKE_LISTING
   - SCAM_PROVIDER
   - MISLEADING_IMAGES
   - FRAUD
   - OTHER
4. Provide detailed description
5. Submit report
6. Admin reviews and takes action
```

#### 7. Manage Profile

**Requires Login:**
- Update your name and phone number
- View your account information
- Check email verification status

**API Endpoints:**
- `GET /api/v1/auth/me` - Get your profile
- `PUT /api/v1/users/{user_id}` - Update profile

---

## PROVIDER User Guide

### Overview

As a **Provider**, you can list your senior housing facilities, manage listings, handle tour requests, respond to reviews, and manage subscriptions.

### Getting Started

1. **Sign Up / Register**
   - Create an account with email and password
   - Choose role: `PROVIDER`
   - Complete your profile

2. **Register as Provider**
   - Provide business information:
     - Business name
     - Business type
     - Tax ID (optional)
     - Business address
     - City and country
   - Submit for verification

3. **Verification Process**
   - Admin reviews your provider application
   - Status: `PENDING` → `VERIFIED` or `REJECTED`
   - Once verified, you can create listings

4. **Subscribe to a Plan**
   - Choose subscription plan:
     - **FREE** - Limited listings
     - **PRO** - Unlimited listings
     - **PREMIUM** - Featured listings, homepage visibility, search ranking boost
   - Complete payment
   - Start creating listings

### What You Can Do

#### 1. Create and Manage Listings

**Requires Login + Provider Role + Verified Status + Active Subscription**

**Create a Listing:**
- Provide facility details:
  - Title and description
  - Care type (Assisted Living, Memory Care, etc.)
  - Room types (Private, Semi-Private, Shared)
  - Location (address, city, state, coordinates)
  - Pricing information
  - Capacity and available beds
  - Staff ratio
  - Contact information
  - License number
  - 24-hour care availability

**API Endpoints:**
- `POST /api/v1/listings` - Create listing
- `GET /api/v1/listings/{listing_id}` - View listing
- `PUT /api/v1/listings/{listing_id}` - Update listing
- `DELETE /api/v1/listings/{listing_id}` - Delete listing

**Example Workflow:**
```
1. Login as Provider
2. Navigate to "Create Listing"
3. Fill in all facility details
4. Submit listing
5. Status: PENDING (waiting for admin approval)
6. Admin approves → Status: ACTIVE
7. Listing is now visible to families
```

#### 2. Upload Listing Images

**Requires Login + Provider Role**

- Upload multiple images per listing
- Set primary image
- Organize images by display order
- Support for file upload or base64 encoding

**API Endpoints:**
- `POST /api/v1/listing-images/upload` - Upload image file
- `POST /api/v1/listing-images` - Create image (base64 or URL)
- `GET /api/v1/listing-images/listing/{listing_id}` - View listing images
- `PUT /api/v1/listing-images/{image_id}` - Update image metadata
- `DELETE /api/v1/listing-images/{image_id}` - Delete image

**Example Workflow:**
```
1. Create listing
2. Go to listing images section
3. Upload facility photos
4. Set primary image (main photo)
5. Arrange images in display order
6. Images appear on listing page
```

#### 3. Configure Listing Features

**Requires Login + Provider Role**

You can associate your listing with various features from the catalog:

- **Amenities** - Pool, WiFi, parking, etc.
- **Treatment Services** - Medication management, diabetes care, etc.
- **Equipment** - Wheelchairs, hospital beds, etc.
- **Languages** - Languages your staff can communicate in
- **Certifications** - State licensed, Medicare certified, etc.
- **Activities** - Gardening, game nights, social activities, etc.
- **Dining Options** - Meal plans, dietary accommodations, etc.
- **Safety Features** - Emergency call systems, fire safety, etc.
- **Insurance Options** - Medicare, private insurance, VA benefits, etc.
- **House Rules** - No smoking, quiet hours, visitor policies, etc.

**Note:** These associations are managed through the listing creation/update process. The catalog data is available via:
- `GET /api/v1/amenities`
- `GET /api/v1/treatment-services`
- `GET /api/v1/equipment`
- `GET /api/v1/languages`
- `GET /api/v1/certifications`
- `GET /api/v1/activities`
- `GET /api/v1/dining-options`
- `GET /api/v1/safety-features`
- `GET /api/v1/insurance-options`
- `GET /api/v1/house-rules`

#### 4. Manage Tour Requests

**Requires Login + Provider Role**

- Receive tour booking requests from families
- Approve or reject tour requests
- View all tour requests for your listings
- Track tour status

**API Endpoints:**
- `GET /api/v1/tours` - View all tours (filter by your listings)
- `GET /api/v1/tours/{tour_id}` - View tour details
- `POST /api/v1/tours/{tour_id}/approve` - Approve tour request
- `POST /api/v1/tours/{tour_id}/cancel` - Cancel tour
- `POST /api/v1/tours/{tour_id}/complete` - Mark tour as completed

**Example Workflow:**
```
1. Family books a tour for your listing
2. Receive notification of tour request
3. View tour details:
   - Tour type (IN_PERSON or VIRTUAL)
   - Scheduled date and time
   - Family contact information
4. Review request
5. Click "Approve" → Status: APPROVED
6. Family receives confirmation
7. Tour happens → Mark as COMPLETED
```

#### 5. Respond to Reviews

**Requires Login + Provider Role**

- View all reviews for your listings
- Respond to reviews from families
- Thank families for positive feedback
- Address concerns in negative reviews

**API Endpoints:**
- `GET /api/v1/reviews` - View all reviews (filter by your listings)
- `PUT /api/v1/reviews/{review_id}` - Add provider response

**Example Workflow:**
```
1. Family leaves review for your listing
2. Receive notification
3. View review:
   - Rating (1-5 stars)
   - Comment
   - Reviewer name
4. Write response
5. Submit response
6. Response appears below review
```

#### 6. Feature Listings

**Requires Login + Provider Role + Premium Subscription**

- Upgrade listings to featured status
- Featured listings appear on homepage
- Better search ranking
- Increased visibility

**API Endpoints:**
- `POST /api/v1/listings/{listing_id}/feature?is_featured=true` - Feature listing
- `POST /api/v1/listings/{listing_id}/feature?is_featured=false` - Unfeature listing

**Example Workflow:**
```
1. Subscribe to PREMIUM plan
2. Go to listing management
3. Click "Feature Listing"
4. Listing becomes featured
5. Appears on homepage
6. Higher in search results
```

#### 7. Manage Subscriptions

**Requires Login + Provider Role**

- View current subscription
- Upgrade or downgrade plans
- Cancel subscription
- View subscription history

**API Endpoints:**
- `GET /api/v1/subscriptions` - View subscriptions
- `GET /api/v1/subscriptions/{subscription_id}` - View subscription details
- `POST /api/v1/subscriptions` - Create new subscription
- `PUT /api/v1/subscriptions/{subscription_id}` - Update subscription
- `POST /api/v1/subscriptions/{subscription_id}/cancel` - Cancel subscription

**Example Workflow:**
```
1. View current subscription status
2. Choose to upgrade:
   - FREE → PRO (unlimited listings)
   - PRO → PREMIUM (featured listings)
3. Complete payment
4. Subscription activated
5. New features available
```

#### 8. View Payments

**Requires Login + Provider Role**

- View payment history
- Track payment status
- View transaction details

**API Endpoints:**
- `GET /api/v1/payments` - View payments
- `GET /api/v1/payments/{payment_id}` - View payment details

---

## ADMIN User Guide

### Overview

As an **Administrator**, you verify providers, approve listings, moderate reports, and manage the platform.

### Getting Started

1. **Login**
   - Login with admin credentials
   - Role: `ADMIN`
   - Full platform access

### What You Can Do

#### 1. Verify Providers

**Requires Login + Admin Role**

- Review provider applications
- Verify business credentials
- Approve or reject providers
- Check business licenses and tax IDs

**API Endpoints:**
- `GET /api/v1/providers` - View all providers
- `GET /api/v1/providers/{provider_id}` - View provider details
- `POST /api/v1/providers/{provider_id}/verify` - Verify provider
- `POST /api/v1/providers/{provider_id}/reject` - Reject provider

**Example Workflow:**
```
1. Provider submits application
2. Review provider information:
   - Business name and type
   - Tax ID
   - Business address
   - Verification documents
3. Verify business credentials
4. Check government licenses
5. Approve → Status: VERIFIED
   OR
   Reject → Status: REJECTED
6. Provider notified of decision
```

#### 2. Approve Listings

**Requires Login + Admin Role**

- Review new listings before publication
- Verify listing information
- Check for fraudulent content
- Approve or reject listings

**API Endpoints:**
- `GET /api/v1/listings` - View all listings
- `GET /api/v1/listings/{listing_id}` - View listing details
- `POST /api/v1/listings/{listing_id}/activate` - Activate listing

**Example Workflow:**
```
1. Provider creates listing
2. Status: PENDING
3. Review listing:
   - Facility details
   - Images (AI validation for fraud)
   - Location verification
   - License numbers
4. Verify provider is verified
5. Approve → Status: ACTIVE
   OR
   Reject → Status: SUSPENDED
6. Listing visible to families (if approved)
```

#### 3. Moderate Reports

**Requires Login + Admin Role**

- Review user reports
- Investigate reported issues
- Take appropriate action
- Resolve or dismiss reports

**API Endpoints:**
- `GET /api/v1/reports` - View all reports
- `GET /api/v1/reports/{report_id}` - View report details
- `POST /api/v1/reports/{report_id}/review` - Mark as reviewed
- `POST /api/v1/reports/{report_id}/resolve` - Resolve report
- `POST /api/v1/reports/{report_id}/dismiss` - Dismiss report

**Example Workflow:**
```
1. User files report:
   - FAKE_LISTING
   - SCAM_PROVIDER
   - MISLEADING_IMAGES
   - FRAUD
   - OTHER
2. Review report details
3. Investigate issue
4. Take action:
   - Remove fraudulent listing
   - Suspend provider
   - Contact provider
5. Mark report as:
   - REVIEWED
   - RESOLVED
   - DISMISSED
```

#### 4. Manage Catalog Data

**Requires Login + Admin Role**

- Create and manage catalog items:
  - Amenities
  - Activities
  - Languages
  - Certifications
  - Dining Options
  - Safety Features
  - Insurance Options
  - House Rules
  - Equipment
  - Treatment Services

**API Endpoints:**
- `POST /api/v1/amenities` - Create amenity
- `PUT /api/v1/amenities/{amenity_id}` - Update amenity
- `DELETE /api/v1/amenities/{amenity_id}` - Delete amenity
- (Similar endpoints for all catalog resources)

**Example Workflow:**
```
1. Need to add new amenity
2. Create amenity:
   - Name: "Swimming Pool"
   - Category: "PREMIUM"
   - Icon: "pool"
3. Amenity available for providers to select
4. Providers can now add this to their listings
```

#### 5. Monitor Platform

**Requires Login + Admin Role**

- View all users
- View all providers
- View all listings
- View all tours
- View all reviews
- View all subscriptions
- View all payments
- Monitor platform analytics

**API Endpoints:**
- `GET /api/v1/users` - View all users
- `GET /api/v1/providers` - View all providers
- `GET /api/v1/listings` - View all listings
- `GET /api/v1/tours` - View all tours
- `GET /api/v1/reviews` - View all reviews
- `GET /api/v1/subscriptions` - View all subscriptions
- `GET /api/v1/payments` - View all payments

---

## Common Workflows

### Complete User Journey: Family Finding Housing

```
1. FAMILY signs up
2. FAMILY searches listings (no login required)
3. FAMILY filters by location, care type, price
4. FAMILY views listing details
5. FAMILY logs in to favorite listings
6. FAMILY compares favorites
7. FAMILY books tour (requires login)
8. PROVIDER receives tour request
9. PROVIDER approves tour
10. FAMILY receives confirmation
11. FAMILY attends tour
12. PROVIDER marks tour as completed
13. FAMILY leaves review
14. PROVIDER responds to review
15. FAMILY decides on placement (outside system)
```

### Complete Provider Journey: Listing a Facility

```
1. PROVIDER signs up
2. PROVIDER registers business information
3. ADMIN reviews and verifies provider
4. PROVIDER subscribes to plan (FREE/PRO/PREMIUM)
5. PROVIDER creates listing
6. PROVIDER uploads images
7. PROVIDER configures amenities, services, etc.
8. ADMIN reviews and approves listing
9. Listing goes live (ACTIVE status)
10. FAMILIES can now see and book tours
11. PROVIDER receives tour requests
12. PROVIDER approves tours
13. FAMILIES attend tours
14. FAMILIES leave reviews
15. PROVIDER responds to reviews
```

---

## Authentication Requirements Summary

| Action | Requires Login | Requires Role |
|--------|---------------|----------------|
| Browse listings | No | - |
| View listing details | No | - |
| Search listings | No | - |
| Add to favorites | Yes | FAMILY/SENIOR |
| Book tour | Yes | FAMILY/SENIOR |
| Leave review | Yes | FAMILY/SENIOR |
| File report | Yes | FAMILY/SENIOR |
| Create listing | Yes | PROVIDER (verified) |
| Upload images | Yes | PROVIDER |
| Approve tours | Yes | PROVIDER |
| Respond to reviews | Yes | PROVIDER |
| Manage subscriptions | Yes | PROVIDER |
| Verify providers | Yes | ADMIN |
| Approve listings | Yes | ADMIN |
| Moderate reports | Yes | ADMIN |
| Manage catalog | Yes | ADMIN |

---

## Support

For questions or issues:
- Check the API documentation in `/docs` folder
- Contact the backend development team
- Review the SRS document for system architecture details

---

**Last Updated:** 2024
**Version:** 1.0






