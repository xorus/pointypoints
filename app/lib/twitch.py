from twitchAPI.twitch import Twitch

from app.settings import settings

# unused for now, but I have plans (tm)
class TwitchInstance:
    api = None

    async def init(self):
        self.api = await Twitch(settings.twitch_client_id, settings.twitch_client_secret)
        # self.api.authenticate_app()


twitch = TwitchInstance()

# auth = UserAuthenticator(twitch, [], force_verify=False)
# token, refreshToken = await auth.authenticate()
