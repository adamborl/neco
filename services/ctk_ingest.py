from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

import requests
import feedparser
from dateutil import parser as dateparser

from models import Article


def authenticate(api_key: str) -> requests.Session:
    """Create an authenticated session for API access."""
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_key}"})
    return session


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return dateparser.parse(value)
    except Exception:
        return None


def fetch_articles(
    session: requests.Session,
    api_url: Optional[str] = None,
    rss_url: Optional[str] = None,
) -> List[Dict[str, Optional[str]]]:
    """Fetch articles either from JSON API or RSS feed."""
    articles: List[Dict[str, Optional[str]]] = []

    if api_url:
        response = session.get(api_url)
        response.raise_for_status()
        data = response.json()
        items = data.get("articles", data)
        for item in items:
            articles.append(
                {
                    "title": item.get("title"),
                    "content": item.get("content") or item.get("description", ""),
                    "published_at": _parse_date(item.get("published_at")),
                    "source_url": item.get("url"),
                }
            )

    if rss_url:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            articles.append(
                {
                    "title": entry.get("title"),
                    "content": entry.get("summary", ""),
                    "published_at": _parse_date(entry.get("published")),
                    "source_url": entry.get("link"),
                }
            )

    return articles


def store_articles(articles: List[Dict[str, Optional[str]]], db_session) -> None:
    """Persist new articles into the database."""
    for data in articles:
        if not data.get("title") or not data.get("source_url"):
            continue
        exists = db_session.query(Article).filter_by(source_url=data["source_url"]).first()
        if exists:
            continue
        article = Article(
            title=data["title"],
            content=data.get("content"),
            published_at=data.get("published_at"),
            source_url=data["source_url"],
        )
        db_session.add(article)
    db_session.commit()


def ingest(
    db_session,
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    rss_url: Optional[str] = None,
) -> None:
    """High level helper to authenticate, fetch and store articles."""
    session = authenticate(api_key) if api_url and api_key else requests.Session()
    articles = fetch_articles(session, api_url=api_url, rss_url=rss_url)
    store_articles(articles, db_session)
