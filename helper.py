API_ZAMG_10MIN =\
    'https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min?parameters=DD,DDX,FFAM,FFX&station_ids=11121,11112,11325'
WEB_URL_IBK = 'https://www.uv-index.at/station/?site=Innsbruck&prod=uve'

TELEGRAM_TOKEN = open('./api_key').readline().rstrip('\n')
print(TELEGRAM_TOKEN)
CHANNEL_NAME = '@uvibk'
