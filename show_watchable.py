from pprint import pprint

import requests

from config import config

from letterboxd_watchable import db

TMDB_API = "https://api.themoviedb.org"
HEADERS = {
    "Authorization": f"Bearer {config.tmdb_api_key}"
}


def run():
    conn = db.get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM cinemas")
    movies = c.fetchall()

    for movie in movies:
        url = f"{TMDB_API}/3/movie/{movie['tmdb_id']}/watch/providers"
        res = requests.get(
            url,
            headers=HEADERS
        )

        if res.status_code != 200:
            print(f"Could not find {movie['name']} (ID: {movie['tmdb_id']})")
            continue

        results = res.json()["results"]
        providers = results.get(config.region, {}).get("flatrate", [])

        if not providers:
            continue

        print()
        print(f"{len(providers)} flatrate providers for {movie['name']} ({movie['year']}):")
        print([provider["provider_name"] for provider in providers])


if __name__ == "__main__":
    run()
