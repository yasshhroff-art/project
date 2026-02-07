# Google Ads Campaign Manager

A full-stack application for creating and publishing marketing campaigns to Google Ads.

## 🏗️ Architecture

- **Frontend**: React 18 with Vite, Axios, React Hook Form
- **Backend**: Python Flask with SQLAlchemy
- **Database**: PostgreSQL
- **API Integration**: Google Ads API (official library)

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Google Ads Account (for API credentials)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd google-ads-campaign-manager
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials (see Google Ads Setup section)

# Initialize database
python init_db.py

# Run the server
python app.py
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env if needed (default backend URL is localhost:5000)

# Run the development server
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🔑 Google Ads Setup

### Step 1: Create a Google Ads Account
1. Go to [Google Ads](https://ads.google.com)
2. Create a test account (use test mode for development)

### Step 2: Get API Credentials

1. **Developer Token**
   - Go to [Google Ads API Center](https://ads.google.com/aw/apicenter)
   - Apply for a developer token
   - For testing, use test account mode

2. **OAuth2 Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing
   - Enable Google Ads API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download client_secret.json

3. **Generate Refresh Token**
   ```bash
   cd backend
   python generate_refresh_token.py
   ```
   - Follow the prompts
   - Copy the refresh token

4. **Get Customer IDs**
   - Login Customer ID: Your MCC account ID (without dashes)
   - Customer Account ID: The account where campaigns will be created

### Step 3: Configure Backend

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/google_ads_db
SECRET_KEY=your-secret-key-change-this

# Google Ads Credentials
GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token
GOOGLE_ADS_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your-client-secret
GOOGLE_ADS_REFRESH_TOKEN=your-refresh-token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
GOOGLE_ADS_CUSTOMER_ID=9876543210
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Create Campaign (Local DB)
```http
POST /api/campaigns
Content-Type: application/json

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

**Response:**
```json
{
  "id": "uuid-here",
  "name": "Summer Sale Campaign",
  "status": "DRAFT",
  "created_at": "2024-02-04T10:00:00Z"
}
```

#### 2. Get All Campaigns
```http
GET /api/campaigns
```

**Response:**
```json
{
  "campaigns": [
    {
      "id": "uuid-here",
      "name": "Summer Sale Campaign",
      "objective": "SALES",
      "status": "DRAFT",
      "daily_budget": 50000,
      "google_campaign_id": null,
      "created_at": "2024-02-04T10:00:00Z"
    }
  ]
}
```

#### 3. Publish Campaign to Google Ads
```http
POST /api/campaigns/{id}/publish
```

**Response:**
```json
{
  "message": "Campaign published successfully",
  "google_campaign_id": "1234567890",
  "status": "PUBLISHED"
}
```

#### 4. Disable Campaign
```http
POST /api/campaigns/{id}/disable
```

**Response:**
```json
{
  "message": "Campaign disabled successfully",
  "status": "PAUSED"
}
```

#### 5. Get Campaign by ID
```http
GET /api/campaigns/{id}
```

#### 6. Delete Campaign
```http
DELETE /api/campaigns/{id}
```

## 🗄️ Database Schema

```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    objective VARCHAR(50),
    campaign_type VARCHAR(50) DEFAULT 'DEMAND_GEN',
    daily_budget INTEGER,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'DRAFT',
    google_campaign_id VARCHAR(100),
    ad_group_name VARCHAR(255),
    ad_headline VARCHAR(500),
    ad_description VARCHAR(1000),
    asset_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🏛️ Project Structure

```
google-ads-campaign-manager/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── models.py              # SQLAlchemy models
│   ├── routes.py              # API routes
│   ├── google_ads_service.py  # Google Ads API integration
│   ├── config.py              # Configuration management
│   ├── init_db.py             # Database initialization
│   ├── generate_refresh_token.py  # OAuth helper
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CampaignForm.jsx
│   │   │   ├── CampaignList.jsx
│   │   │   └── Layout.jsx
│   │   ├── services/
│   │   │   └── api.js        # Axios API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🔧 Design Decisions

### Backend Architecture
- **Flask-RESTful**: Clean API design with proper HTTP methods
- **SQLAlchemy ORM**: Type-safe database operations
- **Service Layer**: `google_ads_service.py` separates business logic
- **Error Handling**: Comprehensive try-catch with proper HTTP status codes

### Database Design
- **UUID Primary Keys**: Better for distributed systems
- **Status Enum**: DRAFT, PUBLISHED, PAUSED lifecycle
- **Timestamps**: Track creation and updates
- **Flexible Schema**: Additional fields can be easily added

### Google Ads Integration
- **Demand Gen Campaigns**: Modern campaign type for discovery
- **Inactive Creation**: Campaigns created with future start dates
- **Resource Names**: Proper handling of Google Ads resource identifiers
- **Error Recovery**: Graceful handling of API failures

### Frontend Design
- **React Hook Form**: Efficient form handling with validation
- **Component Separation**: Reusable, maintainable components
- **API Service Layer**: Centralized HTTP requests
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🐳 Docker Deployment (Optional)

```bash
docker-compose up
```

This will start:
- PostgreSQL database
- Flask backend
- React frontend (production build)

## 🔒 Security Notes

- Never commit `.env` files
- Use strong SECRET_KEY in production
- Rotate Google Ads credentials regularly
- Enable CORS only for trusted origins
- Use HTTPS in production

## 📈 Future Enhancements

- [ ] Campaign analytics dashboard
- [ ] Budget optimization suggestions
- [ ] A/B testing support
- [ ] Multi-account management
- [ ] Automated reporting
- [ ] Campaign templates

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo service postgresql status

# Create database manually
psql -U postgres
CREATE DATABASE google_ads_db;
```