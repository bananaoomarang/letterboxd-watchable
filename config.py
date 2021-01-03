from typing import Literal, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_location: str = "data/data.db"

    #
    # Letterboxd username/password
    #
    username: str = "username"
    password: str = "secret"

    #
    # tmdb_api_key: get from https://developers.themoviedb.org/3/getting-started/introduction
    #
    tmdb_api_key: str = "secret"

    #
    # Streaming region
    #
    region: Literal["CA", "ES", "GB", "PT", "US"] = "US"

    #
    # Whitelist providers
    # to show all providers make a blank list instead
    #
    providers: List[str] = [
        "criterion channel",
        "shudder",
        "hbo max",
        # "amazon prime video",
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
