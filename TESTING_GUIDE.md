# Testing Guide - Google Ads Campaign Manager

## Quick Start Testing

### 1. Test Without Google Ads (Local Only)

You can test the application locally without Google Ads credentials:

```bash
# Start PostgreSQL
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=google_ads_db \
  -p 5432:5432 \
  postgres:15

# Start Backend (in one terminal)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py

# Start Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

**What you can test**:
- ✅ Create campaigns locally
- ✅ View campaign list
- ✅ Update campaigns
- ✅ Delete campaigns
- ❌ Publish to Google Ads (requires credentials)
- ❌ Disable campaigns (requires published campaign)

### 2. Test With Google Ads (Full Integration)

Follow the setup in README.md to configure Google Ads credentials, then test all features.

## Manual Testing Checklist

### Backend API Testing

#### Health Check
```bash
curl http://localhost:5000/api/health
```

Expected: `200 OK` with status information

#### Create Campaign
```bash
curl -X POST http://localhost:5000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "objective": "SALES",
    "campaign_type": "DEMAND_GEN",
    "daily_budget": 50000,
    "start_date": "2024-03-01",
    "end_date": "2024-03-31",
    "ad_group_name": "Test Ad Group",
    "ad_headline": "Test Headline",
    "ad_description": "Test Description",
    "asset_url": "https://example.com"
  }'
```

Expected: `201 Created` with campaign data

#### Get All Campaigns
```bash
curl http://localhost:5000/api/campaigns
```

Expected: `200 OK` with array of campaigns

#### Get Single Campaign
```bash
curl http://localhost:5000/api/campaigns/{campaign-id}
```

Expected: `200 OK` with campaign data

#### Update Campaign
```bash
curl -X PUT http://localhost:5000/api/campaigns/{campaign-id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Campaign Name",
    "daily_budget": 100000
  }'
```

Expected: `200 OK` with updated campaign

#### Publish Campaign (Requires Google Ads)
```bash
curl -X POST http://localhost:5000/api/campaigns/{campaign-id}/publish
```

Expected: `200 OK` with Google campaign ID

#### Disable Campaign (Requires Published Campaign)
```bash
curl -X POST http://localhost:5000/api/campaigns/{campaign-id}/disable
```

Expected: `200 OK` with success message

#### Delete Campaign
```bash
curl -X DELETE http://localhost:5000/api/campaigns/{campaign-id}
```

Expected: `200 OK` with success message

### Frontend Testing

#### Test Campaign Form

1. **Open Application**
   - Navigate to http://localhost:5173
   - Verify page loads correctly

2. **Form Validation**
   - Try submitting empty form → Should show validation errors
   - Enter invalid date range (end before start) → Should show error
   - Enter negative budget → Should show error

3. **Create Campaign**
   - Fill all required fields
   - Click "Save Campaign Locally"
   - Verify success message appears
   - Verify campaign appears in list below

4. **Clear Form**
   - Fill form with data
   - Click "Clear Form"
   - Verify all fields are reset

#### Test Campaign List

1. **View Campaigns**
   - Verify all created campaigns appear
   - Check status badges (DRAFT, PUBLISHED, PAUSED)
   - Verify dates are formatted correctly
   - Verify budget is displayed in dollars

2. **Refresh List**
   - Click "🔄 Refresh" button
   - Verify list updates

3. **Publish Campaign** (With Google Ads)
   - Find a DRAFT campaign
   - Click "📤 Publish"
   - Wait for publishing (may take 10-30 seconds)
   - Verify success message with Google Campaign ID
   - Verify status changes to PUBLISHED

4. **Pause Campaign** (With Google Ads)
   - Find a PUBLISHED campaign
   - Click "⏸️ Pause"
   - Confirm in dialog
   - Verify success message
   - Verify status changes to PAUSED

5. **Delete Campaign**
   - Click "🗑️ Delete"
   - Confirm in dialog
   - Verify campaign is removed from list

## Error Testing

### Test Error Handling

#### Invalid Campaign Data
```bash
curl -X POST http://localhost:5000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "daily_budget": -1000
  }'
```

Expected: `400 Bad Request` with validation errors

#### Non-existent Campaign
```bash
curl http://localhost:5000/api/campaigns/invalid-id
```

Expected: `404 Not Found`

#### Publish Already Published Campaign
```bash
# First publish a campaign, then try again
curl -X POST http://localhost:5000/api/campaigns/{published-id}/publish
```

Expected: `400 Bad Request` with error message

#### Missing Google Ads Credentials
1. Remove `.env` file or clear Google Ads variables
2. Try to publish a campaign
3. Expected: `500 Internal Server Error` with config error

## Database Testing

### Verify Database Schema
```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d google_ads_db

# List tables
\dt

# Describe campaigns table
\d campaigns

# View all campaigns
SELECT id, name, status, google_campaign_id FROM campaigns;

# Exit
\q
```

### Test Data Integrity

#### Check UUID Generation
```sql
SELECT id FROM campaigns LIMIT 1;
-- Should be a valid UUID format
```

#### Check Timestamps
```sql
SELECT created_at, updated_at FROM campaigns ORDER BY created_at DESC;
-- Timestamps should be in UTC
```

#### Check Constraints
```sql
-- Try to insert invalid data
INSERT INTO campaigns (name, daily_budget) VALUES ('Test', -1000);
-- Should succeed (no constraint on budget sign - handled in app layer)
```

## Google Ads Integration Testing

### Test Campaign Creation in Google Ads

1. **Verify Campaign Exists**
   - Log into Google Ads UI
   - Navigate to Campaigns
   - Search for campaign by name
   - Verify campaign details match

2. **Check Campaign Status**
   - Verify campaign is PAUSED or has future start date
   - Check budget is set correctly
   - Verify dates are correct

3. **Check Ad Group**
   - Navigate to Ad Groups
   - Verify ad group exists under campaign
   - Check ad group name

4. **Check Ad**
   - Navigate to Ads & assets
   - Verify responsive display ad exists
   - Check headline and description

### Test Campaign Pause

1. **Pause Campaign**
   - Use API or UI to pause campaign
   
2. **Verify in Google Ads**
   - Refresh Google Ads UI
   - Verify campaign status is "Paused"

## Performance Testing

### Load Testing Campaign Creation

```bash
# Create 10 campaigns quickly
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/campaigns \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"Load Test Campaign $i\",
      \"objective\": \"SALES\",
      \"daily_budget\": 50000,
      \"ad_headline\": \"Headline $i\",
      \"ad_description\": \"Description $i\"
    }" &
done
wait

# Check all campaigns were created
curl http://localhost:5000/api/campaigns | jq '.campaigns | length'
```

### Database Query Performance

```sql
-- Check query plan for campaign list
EXPLAIN ANALYZE SELECT * FROM campaigns ORDER BY created_at DESC;

-- Create index if needed
CREATE INDEX idx_campaigns_created_at ON campaigns(created_at DESC);
```

## Browser Testing

### Test in Multiple Browsers

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### Test Responsive Design

1. **Desktop** (1920x1080)
   - Verify layout is comfortable
   - Check table doesn't overflow

2. **Tablet** (768x1024)
   - Verify form fields stack properly
   - Check buttons are accessible

3. **Mobile** (375x667)
   - Verify all content is readable
   - Check buttons are tap-friendly

## Debugging Tips

### Backend Debugging

#### Enable Detailed Logging
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Check Database Connection
```bash
# Test connection
python3 -c "
from config import Config
from sqlalchemy import create_engine
engine = create_engine(Config.DATABASE_URL)
print('Connected!' if engine else 'Failed')
"
```

#### Inspect Google Ads Requests
```python
# In google_ads_service.py, add:
import google.ads.googleads.errors
google.ads.googleads.errors.logger.setLevel(logging.DEBUG)
```

### Frontend Debugging

#### Check API Calls
```javascript
// Browser console
// Network tab shows all requests
// Console shows logs from api.js interceptors
```

#### React DevTools
- Install React DevTools extension
- Inspect component state
- Check props and hooks

### Common Issues

#### Issue: "Connection refused" to backend
**Solution**: 
```bash
# Check backend is running
curl http://localhost:5000/api/health

# Check port not in use
lsof -i :5000
```

#### Issue: "CORS error"
**Solution**:
```python
# Verify CORS_ORIGINS in .env includes frontend URL
CORS_ORIGINS=http://localhost:5173
```

#### Issue: "Database connection failed"
**Solution**:
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Verify DATABASE_URL in .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/google_ads_db
```

#### Issue: "Google Ads API error"
**Solution**:
- Verify all credentials in .env
- Check developer token is approved
- Ensure customer IDs have no dashes
- Verify OAuth token hasn't expired

## Automated Testing (Future)

### Unit Tests
```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm test
```

### Integration Tests
```bash
# Run integration test suite
pytest tests/integration/
```

### E2E Tests
```bash
# Run Cypress/Playwright tests
npm run test:e2e
```

## Test Data Cleanup

### Reset Database
```bash
cd backend
python init_db.py
```

### Delete Test Campaigns from Google Ads
```python
# Use Google Ads UI or write cleanup script
# Be careful not to delete production campaigns!
```

## Test Reports

### Generate Coverage Report
```bash
# Backend
pytest --cov=. --cov-report=html

# Frontend
npm run test:coverage
```

### Performance Metrics
- Average campaign creation time: < 1 second (local DB)
- Average publish time: 10-30 seconds (Google Ads API)
- Page load time: < 2 seconds
- Time to interactive: < 3 seconds

## Security Testing

### Test Input Validation
- SQL injection attempts
- XSS attempts in campaign names
- Invalid date formats
- Extremely large budget values

### Test Authentication
- Verify API requires valid session (if implemented)
- Check refresh token rotation
- Test expired credentials handling

## Conclusion

This testing guide covers:
- ✅ Manual testing procedures
- ✅ API endpoint testing
- ✅ Frontend UI testing
- ✅ Database verification
- ✅ Google Ads integration
- ✅ Error handling
- ✅ Performance considerations

Regular testing ensures the application remains reliable and bug-free!
