from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    host: str
    password: str
    user: str
    database: str
    port: int


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = ''


@dataclass
class Config:
    bot: TelegramBot
    database: DatabaseConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=TelegramBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS'))),
            use_redis=env.bool('USE_REDIS'),
        ),
        database=DatabaseConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT')
        ),
        misc=Miscellaneous()
    )
