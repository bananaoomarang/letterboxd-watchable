import requests

import colored
from colored import stylize

from config import config

from letterboxd_watchable import db

TMDB_API = "https://api.themoviedb.org"
HEADERS = {
    "Authorization": f"Bearer {config.tmdb_api_key}"
}

ERROR = colored.fg("red") + colored.attr("bold")
GOOD = colored.fg("white") + colored.attr("bold")
GREEN = colored.fg("green") + colored.attr("bold")


def run():
    conn = db.get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM cinemas")
    movies = c.fetchall()

    table_data = {}

    for movie in movies:
        url = f"{TMDB_API}/3/movie/{movie['tmdb_id']}/watch/providers"
        res = requests.get(
            url,
            headers=HEADERS
        )

        if res.status_code != 200:
            print(
                stylize(f"Could not find {movie['name']} (ID: {movie['tmdb_id']})", ERROR)
            )
            continue

        results = res.json()["results"]
        providers = results.get(config.region, {}).get("flatrate", [])

        if not providers:
            continue

        for provider in providers:
            provider_name = provider["provider_name"].lower().title()

            if not table_data.get(provider_name, None):
                table_data[provider_name] = []
            table_data[provider_name].append(f"{movie['name']} ({movie['year']}) {watched_text() if movie['watched'] else ''} {rated_text(movie['rated']) if movie['rated'] else '' }")

    for service, titles in table_data.items():
        if config.providers and service.lower() not in config.providers:
            continue

        print(stylize('----------------------------', GOOD))
        print(
            stylize(
                f"Available on {service}:",
                GOOD
            )
        )
        print(stylize('----------------------------', GOOD))
        for title in titles:
            print(stylize(title, GREEN))
        print()

def watched_text():
    return "Seen it!"

def rated_text(rating):
    popcorns = "\U0001F600" * rating
    return popcorns


if __name__ == "__main__":
    run()
