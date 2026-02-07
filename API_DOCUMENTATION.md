# API Documentation - Google Ads Campaign Manager

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently, no authentication is required for API endpoints. In production, implement JWT or OAuth2.

## Response Format

### Success Response
```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": ["Validation error 1", "Validation error 2"]
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Endpoints

### Health Check

Check API health status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "google_ads_config": "valid",
  "missing_config": []
}
```

**Example**:
```bash
curl http://localhost:5000/api/health
```

---

### Get All Campaigns

Retrieve all campaigns from the database.

**Endpoint**: `GET /campaigns`

**Query Parameters**: None

**Response**:
```json
{
  "campaigns": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Summer Sale Campaign",
      "objective": "SALES",
      "campaign_type": "DEMAND_GEN",
      "daily_budget": 50000,
      "start_date": "2024-03-01",
      "end_date": "2024-03-31",
      "status": "DRAFT",
      "google_campaign_id": null,
      "ad_group_name": "Main Ad Group",
      "ad_headline": "Amazing Summer Deals!",
      "ad_description": "Save up to 50% on all products",
      "asset_url": "https://example.com/summer-sale",
      "created_at": "2024-02-04T10:00:00Z",
      "updated_at": "2024-02-04T10:00:00Z"
    }
  ]
}
```

**Example**:
```bash
curl http://localhost:5000/api/campaigns
```

**Notes**:
- Campaigns are ordered by creation date (newest first)
- Returns empty array if no campaigns exist

---

### Get Campaign by ID

Retrieve a specific campaign.

**Endpoint**: `GET /campaigns/{id}`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Campaign ID |

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Summer Sale Campaign",
  "objective": "SALES",
  "campaign_type": "DEMAND_GEN",
  "daily_budget": 50000,
  "start_date": "2024-03-01",
  "end_date": "2024-03-31",
  "status": "DRAFT",
  "google_campaign_id": null,
  "ad_group_name": "Main Ad Group",
  "ad_headline": "Amazing Summer Deals!",
  "ad_description": "Save up to 50% on all products",
  "asset_url": "https://example.com/summer-sale",
  "created_at": "2024-02-04T10:00:00Z",
  "updated_at": "2024-02-04T10:00:00Z"
}
```

**Example**:
```bash
curl http://localhost:5000/api/campaigns/550e8400-e29b-41d4-a716-446655440000
```

**Error Responses**:
- `404 Not Found`: Campaign does not exist

---

### Create Campaign

Create a new campaign in the local database.

**Endpoint**: `POST /campaigns`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Summer Sale Campaign",
  "objective": "SALES",
  "campaign_type": "DEMAND_GEN",
  "daily_budget": 50000,
  "start_date": "2024-03-01",
  "end_date": "2024-03-31",
  "ad_group_name": "Main Ad Group",
  "ad_headline": "Amazing Summer Deals!",
  "ad_description": "Save up to 50% on all products",
  "asset_url": "https://example.com/summer-sale"
}
```

**Field Descriptions**:
| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| name | string | Yes | Campaign name | Max 255 chars |
| objective | string | No | Campaign objective | SALES, LEADS, WEBSITE_TRAFFIC, etc. |
| campaign_type | string | No | Campaign type | Default: DEMAND_GEN |
| daily_budget | integer | No | Daily budget in micros | Positive integer ($1 = 1,000,000 micros) |
| start_date | date | No | Campaign start date | ISO 8601 format (YYYY-MM-DD) |
| end_date | date | No | Campaign end date | Must be after start_date |
| ad_group_name | string | No | Ad group name | Max 255 chars |
| ad_headline | string | No | Ad headline text | Max 30 chars |
| ad_description | string | No | Ad description text | Max 90 chars |
| asset_url | string | No | Final URL for ad | Valid URL format |

**Response**: `201 Created`
```json
{
  "message": "Campaign created successfully",
  "campaign": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Summer Sale Campaign",
    "status": "DRAFT",
    "created_at": "2024-02-04T10:00:00Z",
    ...
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "objective": "SALES",
    "daily_budget": 50000,
    "ad_headline": "Test Headline"
  }'
```

**Error Responses**:
- `400 Bad Request`: Validation errors
  ```json
  {
    "error": "Validation failed",
    "details": [
      "Campaign name is required",
      "End date must be after start date"
    ]
  }
  ```

---

### Update Campaign

Update an existing campaign.

**Endpoint**: `PUT /campaigns/{id}`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Campaign ID |

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Updated Campaign Name",
  "daily_budget": 100000
}
```

**Notes**:
- Only include fields you want to update
- Cannot update PUBLISHED campaigns
- Status field cannot be updated directly

**Response**: `200 OK`
```json
{
  "message": "Campaign updated successfully",
  "campaign": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Campaign Name",
    "daily_budget": 100000,
    "updated_at": "2024-02-04T11:00:00Z",
    ...
  }
}
```

**Example**:
```bash
curl -X PUT http://localhost:5000/api/campaigns/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Name",
    "daily_budget": 75000
  }'
```

**Error Responses**:
- `404 Not Found`: Campaign does not exist
- `400 Bad Request`: Cannot update published campaign

---

### Delete Campaign

Delete a campaign from the database.

**Endpoint**: `DELETE /campaigns/{id}`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Campaign ID |

**Response**: `200 OK`
```json
{
  "message": "Campaign deleted successfully"
}
```

**Example**:
```bash
curl -X DELETE http://localhost:5000/api/campaigns/550e8400-e29b-41d4-a716-446655440000
```

**Notes**:
- Deleting a PUBLISHED campaign only removes it from local DB
- It will still exist in Google Ads
- Consider pausing before deleting

**Error Responses**:
- `404 Not Found`: Campaign does not exist

---

### Publish Campaign to Google Ads

Publish a campaign to Google Ads.

**Endpoint**: `POST /campaigns/{id}/publish`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Campaign ID |

**Prerequisites**:
- Campaign must be in DRAFT status
- Google Ads credentials must be configured
- Campaign must have required fields filled

**Response**: `200 OK`
```json
{
  "message": "Campaign published successfully",
  "google_campaign_id": "1234567890",
  "ad_group_id": "9876543210",
  "ad_id": "1122334455",
  "status": "PUBLISHED"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/campaigns/550e8400-e29b-41d4-a716-446655440000/publish
```

**What Happens**:
1. Creates campaign in Google Ads
2. Creates campaign budget
3. Creates ad group under campaign
4. Creates responsive display ad
5. Updates local database with Google IDs
6. Changes status to PUBLISHED

**Notes**:
- This operation may take 10-30 seconds
- Campaign is created as PAUSED or with future start date
- Actual spend only begins when campaign is activated in Google Ads

**Error Responses**:
- `404 Not Found`: Campaign does not exist
- `400 Bad Request`: Campaign already published
- `500 Internal Server Error`: Google Ads API error
  ```json
  {
    "error": "Failed to publish campaign: PERMISSION_DENIED: User does not have access"
  }
  ```

---

### Disable Campaign

Pause a campaign in Google Ads.

**Endpoint**: `POST /campaigns/{id}/disable`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | UUID | Yes | Campaign ID |

**Prerequisites**:
- Campaign must be PUBLISHED
- Google Ads credentials must be configured

**Response**: `200 OK`
```json
{
  "message": "Campaign disabled successfully",
  "status": "PAUSED"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/campaigns/550e8400-e29b-41d4-a716-446655440000/disable
```

**What Happens**:
1. Updates campaign status to PAUSED in Google Ads
2. Updates status to PAUSED in local database
3. Campaign stops serving immediately

**Notes**:
- This prevents charges from accruing
- Campaign can be re-enabled in Google Ads UI
- Local database status becomes PAUSED

**Error Responses**:
- `404 Not Found`: Campaign does not exist
- `400 Bad Request`: Campaign not published
- `500 Internal Server Error`: Google Ads API error

---

## Data Models

### Campaign Object

```typescript
{
  id: string;                    // UUID
  name: string;                  // Campaign name
  objective: string | null;      // Campaign objective
  campaign_type: string;         // Campaign type (default: DEMAND_GEN)
  daily_budget: number | null;   // Budget in micros
  start_date: string | null;     // ISO 8601 date
  end_date: string | null;       // ISO 8601 date
  status: string;                // DRAFT | PUBLISHED | PAUSED
  google_campaign_id: string | null;  // Google Ads campaign ID
  ad_group_name: string | null;  // Ad group name
  ad_headline: string | null;    // Ad headline
  ad_description: string | null; // Ad description
  asset_url: string | null;      // Final URL
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}
```

### Campaign Status Flow

```
DRAFT ──publish──> PUBLISHED ──disable──> PAUSED
  │                                          │
  └──────────────delete──────────────────────┘
```

---

## Error Codes

### Validation Errors (400)

| Error | Description |
|-------|-------------|
| Campaign name is required | Name field is empty |
| Daily budget must be positive | Budget is negative |
| End date must be after start date | Date range invalid |
| Invalid date format | Date not in ISO 8601 format |

### Not Found Errors (404)

| Error | Description |
|-------|-------------|
| Campaign not found | Campaign ID does not exist |

### Business Logic Errors (400)

| Error | Description |
|-------|-------------|
| Campaign is already published | Cannot publish twice |
| Cannot update published campaign | Must create new campaign |
| Campaign is not published to Google Ads | Cannot disable draft campaign |

### Google Ads API Errors (500)

| Error | Description |
|-------|-------------|
| Failed to initialize Google Ads client | Invalid credentials |
| Failed to create campaign | Google Ads API error |
| PERMISSION_DENIED | Invalid customer ID or access |
| QUOTA_EXCEEDED | API rate limit reached |

---

## Rate Limits

Currently no rate limiting is implemented. In production, consider:

- 100 requests per minute per IP
- 1000 requests per hour per IP
- Separate limits for publish operations (slower)

---

## Best Practices

### Creating Campaigns

1. Always provide meaningful names
2. Set realistic budgets (test with small amounts)
3. Use future start dates for review period
4. Include complete ad creative (headline, description)
5. Validate URLs before submitting

### Publishing Campaigns

1. Review campaign details before publishing
2. Ensure Google Ads credentials are valid
3. Start with small budgets for testing
4. Monitor Google Ads dashboard after publishing
5. Disable campaigns when testing is complete

### Error Handling

1. Always check response status codes
2. Log errors for debugging
3. Implement retry logic for transient errors
4. Display user-friendly error messages
5. Provide actionable error resolution steps

---

## Examples

### Complete Workflow Example

```bash
# 1. Create a campaign
CAMPAIGN_ID=$(curl -X POST http://localhost:5000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 2024 Sale",
    "objective": "SALES",
    "daily_budget": 100000,
    "start_date": "2024-03-01",
    "end_date": "2024-03-31",
    "ad_headline": "Save Big This Quarter!",
    "ad_description": "Up to 70% off selected items",
    "asset_url": "https://example.com/q1-sale"
  }' | jq -r '.campaign.id')

# 2. Review the campaign
curl http://localhost:5000/api/campaigns/$CAMPAIGN_ID

# 3. Publish to Google Ads
curl -X POST http://localhost:5000/api/campaigns/$CAMPAIGN_ID/publish

# 4. Later, disable the campaign
curl -X POST http://localhost:5000/api/campaigns/$CAMPAIGN_ID/disable

# 5. Finally, delete from database
curl -X DELETE http://localhost:5000/api/campaigns/$CAMPAIGN_ID
```

### Batch Create Campaigns

```bash
#!/bin/bash
for i in {1..5}; do
  curl -X POST http://localhost:5000/api/campaigns \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"Test Campaign $i\",
      \"objective\": \"SALES\",
      \"daily_budget\": 50000,
      \"ad_headline\": \"Headline $i\"
    }"
  echo ""
done
```

---

## Webhook Support (Future)

Future versions may support webhooks for:

- Campaign status changes
- Publishing completion notifications
- Error alerts
- Performance thresholds

---

## API Versioning

Current version: `v1`

Future versions will use URL versioning:
- `http://localhost:5000/api/v1/campaigns`
- `http://localhost:5000/api/v2/campaigns`

---

## OpenAPI Specification

For a machine-readable API specification, see `openapi.yaml` (coming soon).

Can be used with:
- Swagger UI
- Postman
- API testing tools

---

## Support

For API issues:
1. Check this documentation
2. Review TESTING_GUIDE.md
3. Check application logs
4. Open a GitHub issue

---

**Last Updated**: February 4, 2024  
**API Version**: 1.0.0
