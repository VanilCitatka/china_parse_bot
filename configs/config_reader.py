from pydantic import SecretStr, BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = 'configs/.env'
        env_file_encoding = 'utf-8'


config = Settings()
