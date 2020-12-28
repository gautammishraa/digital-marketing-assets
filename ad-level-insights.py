from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount

app_id = 'xxx'
app_secret = 'xxx'
access_token = 'xxx'

FacebookAdsApi.init(app_id, app_secret, access_token)

params = {'time_range': {'since': '2020-01-01', 'until': '2020-12-25'},
          'time_increment':1,
          'level': 'adset',
          'sort': ['spend_descending'],
          'export_format':'csv'}
fields = ['account_name',
          'campaign_name',
          'campaign_id',
          'adset_name',
          'adset_id',
          'impressions',
          'clicks',
          'cpm',
          'spend',
          'ctr']

me = User(fbid='me')
my_accounts = list(me.get_ad_accounts())
print(my_accounts)

insights = AdAccount('act_332828570147114').get_insights(params=params, fields=fields)
print(insights)
