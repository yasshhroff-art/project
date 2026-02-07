"""
Helper script to generate Google Ads API refresh token.
This is a one-time setup script to get OAuth credentials.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json


def generate_refresh_token():
    """
    Generate a refresh token for Google Ads API.
    
    Prerequisites:
    1. Create OAuth 2.0 credentials in Google Cloud Console
    2. Download the credentials as client_secret.json
    3. Place client_secret.json in the same directory as this script
    """
    
    print("Google Ads API - Refresh Token Generator")
    print("=" * 50)
    print()
    
    # Check for client_secret.json
    try:
        with open('client_secret.json', 'r') as f:
            credentials = json.load(f)
            print("✓ Found client_secret.json")
    except FileNotFoundError:
        print("✗ Error: client_secret.json not found!")
        print()
        print("Please follow these steps:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com")
        print("2. Create a new project or select existing")
        print("3. Enable Google Ads API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download credentials as client_secret.json")
        print("6. Place it in the backend directory")
        return
    
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/adwords']
    
    try:
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=SCOPES
        )
        
        # Run the OAuth flow
        print()
        print("Starting OAuth flow...")
        print("A browser window will open. Please:")
        print("1. Sign in with your Google account")
        print("2. Grant access to Google Ads API")
        print("3. Copy the authorization code")
        print()
        
        credentials = flow.run_local_server(
            port=8080,
            authorization_prompt_message='Please visit this URL: {url}',
            success_message='The authentication flow has completed. You may close this window.'
        )
        
        # Extract the refresh token
        refresh_token = credentials.refresh_token
        client_id = credentials.client_id
        client_secret = credentials.client_secret
        
        print()
        print("=" * 50)
        print("SUCCESS! Here are your credentials:")
        print("=" * 50)
        print()
        print(f"GOOGLE_ADS_CLIENT_ID={client_id}")
        print(f"GOOGLE_ADS_CLIENT_SECRET={client_secret}")
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}")
        print()
        print("=" * 50)
        print()
        print("Copy these values to your .env file!")
        print()
        
        # Save to a file
        with open('google_ads_credentials.txt', 'w') as f:
            f.write(f"GOOGLE_ADS_CLIENT_ID={client_id}\n")
            f.write(f"GOOGLE_ADS_CLIENT_SECRET={client_secret}\n")
            f.write(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}\n")
        
        print("✓ Credentials saved to google_ads_credentials.txt")
        print()
        
    except Exception as e:
        print(f"✗ Error during OAuth flow: {str(e)}")
        print()
        print("Troubleshooting:")
        print("- Make sure client_secret.json is valid")
        print("- Check that Google Ads API is enabled")
        print("- Verify OAuth consent screen is configured")


if __name__ == '__main__':
    generate_refresh_token()
