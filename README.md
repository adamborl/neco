# neco

Example project that periodically ingests articles from an API or RSS feed and stores them in a database.

## Usage

1. Set `DATABASE_URL` to your PostgreSQL or SQLite database.
2. For API access, set `API_KEY` and `API_URL`. For RSS ingestion set `RSS_URL`.
3. Run the scheduler:
   ```bash
   python scheduler.py
   ```
