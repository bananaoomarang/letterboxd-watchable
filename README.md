Scripts to allow letterboxd free tier users to tell what is available to stream to them from the watchlist.

### Setup ###

This project uses [Poetry](https://python-poetry.org/) to manage the python deps/venv, so will need to install that first

The project configuration is controlled by `config.py`. To override specific config vars you can use a `.env` file, minimal example:

```bash
LBOX_USERNAME=youremail@email.com
LBOX_PASSWORD=yourletterboxdpassword
LBOX_TMDB_API_KEY=your-tmdb-api-key
```

To get a TMDB API key you need a (free) account and to request on on the account settings page (see docs)[https://developers.themoviedb.org/3/getting-started/introduction].

You may also want to customise the providers list in `config.py` as this is tedious to specify as an environment variable. To show all providers just make it a blank list like:

```python
providers: List[str] = []
```

### Running ###

```bash
$ poetry install
$ poetry run python -m update_watchlist (need to rerun if watchlist changes)
$ poetry run python -m show_watchable
```

If it worked you should be able to see a list of movies available by streaming provider:

![Example result](images/example.png?raw=true "Example result")
