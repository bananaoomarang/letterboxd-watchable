from typing import Literal, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_location: str = "data/data.db"
    username: str = "username"
    password: str = "secret"

    tmdb_api_key: str = "secret"

    region: Literal["CA", "ES", "GB", "PT", "US"] = "US"

    providers: List[str] = [
        "criterion channel",
        "shudder",
        "hbo max",
        #"amazon prime video",
        "classix",
        # "mubi",
        "hulu",
        "netflix",
        "indieflix"
    ]

    class Config:
        env_file = '.env'
        env_prefix = "lbox_"

config = Settings()
