import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Settings


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        config: Settings = obj.bot.get('config')
        return (obj.from_user.id in config.ADMIN_IDS) == self.is_admin

