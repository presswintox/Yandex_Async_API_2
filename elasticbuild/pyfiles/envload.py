from pydantic import (
    BaseSettings,
    Field,
)


class Env(BaseSettings):
    host: str = Field(env='ELASTICBUILD_HOST')
    port: int = Field(env='ELASTICBUILD_PORT')
