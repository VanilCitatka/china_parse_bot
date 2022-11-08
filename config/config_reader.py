from pydantic import SecretStr, BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        enf_file = '.env'
        enf_file_encoding = 'utf-8'


config = Settings()