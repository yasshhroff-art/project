"""
Google Ads API service layer.
Handles all interactions with the Google Ads API including campaign creation,
ad group creation, and ad creation.
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GoogleAdsService:
    """Service class for Google Ads API operations."""
    
    def __init__(self, credentials):
        """
        Initialize Google Ads client with credentials.
        
        Args:
            credentials (dict): Dictionary containing Google Ads API credentials
        """
        self.credentials = credentials
        self.client = None
        self.customer_id = credentials.get('customer_id', '').replace('-', '')
        
    def initialize_client(self):
        """Initialize the Google Ads client from credentials."""
        try:
            # Create credentials dictionary in the format expected by Google Ads API
            credentials_dict = {
                'developer_token': self.credentials['developer_token'],
                'client_id': self.credentials['client_id'],
                'client_secret': self.credentials['client_secret'],
                'refresh_token': self.credentials['refresh_token'],
                'login_customer_id': self.credentials['login_customer_id'].replace('-', ''),
                'use_proto_plus': True
            }
            
            self.client = GoogleAdsClient.load_from_dict(credentials_dict)
            logger.info("Google Ads client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Google Ads client: {str(e)}")
            raise Exception(f"Failed to initialize Google Ads client: {str(e)}")
    
    def create_demand_gen_campaign(self, campaign_data):
        """
        Create a Demand Gen campaign in Google Ads.
        
        Args:
            campaign_data (dict): Campaign details from database
            
        Returns:
            str: Google Ads campaign ID
        """
        if not self.client:
            self.initialize_client()
        
        try:
            campaign_service = self.client.get_service("CampaignService")
            campaign_operation = self.client.get_type("CampaignOperation")
            
            campaign = campaign_operation.create
            
            # Set campaign name
            campaign.name = campaign_data['name']
            
            # Set campaign type to DEMAND_GEN
            campaign.advertising_channel_type = self.client.enums.AdvertisingChannelTypeEnum.DEMAND_GEN
            
            # Set campaign status to PAUSED (inactive) or based on start date
            start_date = campaign_data.get('start_date')
            if start_date:
                start_datetime = datetime.fromisoformat(str(start_date))
                if start_datetime > datetime.now():
                    campaign.status = self.client.enums.CampaignStatusEnum.ENABLED
                else:
                    campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            else:
                campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            
            # Set bidding strategy - Maximize Conversions for Demand Gen
            campaign.maximize_conversions.target_cpa = 0
            
            # Set budget
            budget_resource_name = self._create_campaign_budget(
                campaign_data['name'],
                campaign_data.get('daily_budget', 50000)
            )
            campaign.campaign_budget = budget_resource_name
            
            # Set dates if provided
            if start_date:
                campaign.start_date = start_datetime.strftime('%Y%m%d')
            
            end_date = campaign_data.get('end_date')
            if end_date:
                end_datetime = datetime.fromisoformat(str(end_date))
                campaign.end_date = end_datetime.strftime('%Y%m%d')
            
            # Execute the operation
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            campaign_resource_name = response.results[0].resource_name
            campaign_id = campaign_resource_name.split('/')[-1]
            
            logger.info(f"Created Demand Gen campaign with ID: {campaign_id}")
            return campaign_id
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            error_message = self._parse_google_ads_error(ex)
            raise Exception(f"Failed to create campaign: {error_message}")
        except Exception as e:
            logger.error(f"Unexpected error creating campaign: {str(e)}")
            raise Exception(f"Failed to create campaign: {str(e)}")
    
    def _create_campaign_budget(self, campaign_name, daily_budget_micros):
        """
        Create a campaign budget.
        
        Args:
            campaign_name (str): Name for the budget
            daily_budget_micros (int): Daily budget in micros
            
        Returns:
            str: Resource name of the created budget
        """
        campaign_budget_service = self.client.get_service("CampaignBudgetService")
        campaign_budget_operation = self.client.get_type("CampaignBudgetOperation")
        
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"Budget for {campaign_name}"
        campaign_budget.amount_micros = daily_budget_micros
        campaign_budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
        
        response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=self.customer_id,
            operations=[campaign_budget_operation]
        )
        
        return response.results[0].resource_name
    
    def create_ad_group(self, campaign_id, ad_group_data):
        """
        Create an ad group for a campaign.
        
        Args:
            campaign_id (str): Google Ads campaign ID
            ad_group_data (dict): Ad group details
            
        Returns:
            str: Ad group ID
        """
        if not self.client:
            self.initialize_client()
        
        try:
            ad_group_service = self.client.get_service("AdGroupService")
            ad_group_operation = self.client.get_type("AdGroupOperation")
            
            ad_group = ad_group_operation.create
            ad_group.name = ad_group_data.get('name', 'Ad Group 1')
            ad_group.campaign = self.client.get_service("CampaignService").campaign_path(
                self.customer_id, campaign_id
            )
            ad_group.status = self.client.enums.AdGroupStatusEnum.ENABLED
            
            # Set ad group type for Demand Gen
            ad_group.type_ = self.client.enums.AdGroupTypeEnum.DISPLAY_STANDARD
            
            response = ad_group_service.mutate_ad_groups(
                customer_id=self.customer_id,
                operations=[ad_group_operation]
            )
            
            ad_group_resource_name = response.results[0].resource_name
            ad_group_id = ad_group_resource_name.split('/')[-1]
            
            logger.info(f"Created ad group with ID: {ad_group_id}")
            return ad_group_id
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error creating ad group: {ex}")
            error_message = self._parse_google_ads_error(ex)
            raise Exception(f"Failed to create ad group: {error_message}")
    
    def create_responsive_display_ad(self, campaign_id, ad_group_id, ad_data):
        """
        Create a responsive display ad.
        
        Args:
            campaign_id (str): Google Ads campaign ID
            ad_group_id (str): Ad group ID
            ad_data (dict): Ad creative details
            
        Returns:
            str: Ad ID
        """
        if not self.client:
            self.initialize_client()
        
        try:
            ad_group_ad_service = self.client.get_service("AdGroupAdService")
            ad_group_ad_operation = self.client.get_type("AdGroupAdOperation")
            
            ad_group_ad = ad_group_ad_operation.create
            ad_group_ad.ad_group = self.client.get_service("AdGroupService").ad_group_path(
                self.customer_id, ad_group_id
            )
            ad_group_ad.status = self.client.enums.AdGroupAdStatusEnum.ENABLED
            
            # Create responsive display ad
            ad = ad_group_ad.ad
            ad.responsive_display_ad.headlines.append(
                self._create_ad_text_asset(ad_data.get('headline', 'Default Headline'))
            )
            ad.responsive_display_ad.descriptions.append(
                self._create_ad_text_asset(ad_data.get('description', 'Default Description'))
            )
            
            # Add business name
            ad.responsive_display_ad.business_name = ad_data.get('name', 'Business Name')
            
            # Add final URL if provided
            if ad_data.get('asset_url'):
                ad.final_urls.append(ad_data['asset_url'])
            
            response = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=self.customer_id,
                operations=[ad_group_ad_operation]
            )
            
            ad_resource_name = response.results[0].resource_name
            ad_id = ad_resource_name.split('~')[-1]
            
            logger.info(f"Created ad with ID: {ad_id}")
            return ad_id
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error creating ad: {ex}")
            error_message = self._parse_google_ads_error(ex)
            raise Exception(f"Failed to create ad: {error_message}")
    
    def _create_ad_text_asset(self, text):
        """Helper to create ad text asset."""
        ad_text_asset = self.client.get_type("AdTextAsset")
        ad_text_asset.text = text[:30]  # Max 30 chars for headline
        return ad_text_asset
    
    def disable_campaign(self, campaign_id):
        """
        Disable (pause) a campaign.
        
        Args:
            campaign_id (str): Google Ads campaign ID
            
        Returns:
            bool: Success status
        """
        if not self.client:
            self.initialize_client()
        
        try:
            campaign_service = self.client.get_service("CampaignService")
            campaign_operation = self.client.get_type("CampaignOperation")
            
            campaign = campaign_operation.update
            campaign.resource_name = campaign_service.campaign_path(
                self.customer_id, campaign_id
            )
            campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            
            campaign_operation.update_mask.paths.append("status")
            
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            logger.info(f"Disabled campaign {campaign_id}")
            return True
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error disabling campaign: {ex}")
            error_message = self._parse_google_ads_error(ex)
            raise Exception(f"Failed to disable campaign: {error_message}")
    
    def _parse_google_ads_error(self, ex):
        """Parse Google Ads exception to extract meaningful error message."""
        error_messages = []
        for error in ex.failure.errors:
            error_messages.append(f"{error.error_code.name}: {error.message}")
        return " | ".join(error_messages) if error_messages else str(ex)
    
    def publish_campaign(self, campaign_data):
        """
        Complete workflow to publish a campaign to Google Ads.
        Creates campaign, ad group, and ad.
        
        Args:
            campaign_data (dict): Complete campaign data
            
        Returns:
            dict: Contains campaign_id, ad_group_id, ad_id
        """
        try:
            # Step 1: Create campaign
            campaign_id = self.create_demand_gen_campaign(campaign_data)
            
            # Step 2: Create ad group
            ad_group_data = {
                'name': campaign_data.get('ad_group_name', 'Main Ad Group')
            }
            ad_group_id = self.create_ad_group(campaign_id, ad_group_data)
            
            # Step 3: Create ad
            ad_data = {
                'name': campaign_data['name'],
                'headline': campaign_data.get('ad_headline', 'Default Headline'),
                'description': campaign_data.get('ad_description', 'Default Description'),
                'asset_url': campaign_data.get('asset_url')
            }
            ad_id = self.create_responsive_display_ad(campaign_id, ad_group_id, ad_data)
            
            return {
                'campaign_id': campaign_id,
                'ad_group_id': ad_group_id,
                'ad_id': ad_id
            }
            
        except Exception as e:
            logger.error(f"Error in publish_campaign workflow: {str(e)}")
            raise
