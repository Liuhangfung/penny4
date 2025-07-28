# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MediaCrawlerPro is a Python-based social media crawling system that supports multiple platforms including XiaoHongShu (XHS), Weibo, TikTok (Douyin), Kuaishou, Bilibili, Tieba, and Zhihu. The system is designed for educational and research purposes only.

## Project Architecture

### Core Components

- **main.py**: Entry point using CrawlerFactory pattern to instantiate platform-specific crawlers
- **base/base_crawler.py**: Abstract base class (AbstractCrawler) that all platform crawlers inherit from
- **media_platform/**: Platform-specific implementations, each containing:
  - `client.py`: HTTP client for API communication
  - `core.py`: Main crawler logic
  - `handlers/`: Request handlers for different crawl types (search, detail, creator, homefeed)
  - `processors/`: Data processing logic for posts, comments, etc.
  - `field.py`: Platform-specific enums and constants
- **config/**: Configuration management
  - `base_config.py`: Main configuration file with platform and crawl settings
  - `db_config.py`: Database connection settings
  - `proxy_config.py`: Proxy configuration
  - `sign_srv_config.py`: Signature service configuration
- **pkg/**: Utility packages
  - `account_pool/`: Multi-account management system
  - `proxy/`: IP proxy management with rotation
  - `cache/`: Caching layer (local/Redis)
  - `rpc/sign_srv_client/`: Client for signature service (MediaCrawlerPro-SignSrv)
- **repo/**: Data persistence layer with platform-specific stores
- **model/**: Database models for each platform

### Architecture Pattern

The system uses a modular architecture where each platform crawler inherits from AbstractCrawler and implements:
- `async_initialize()`: Setup phase
- `start()`: Main crawling logic

Each platform follows a handler-processor pattern:
- Handlers manage different crawl types (search, detail, creator, homefeed)
- Processors handle data transformation and storage

## Common Commands

### Running the Crawler
```bash
# Basic usage - crawl XiaoHongShu search results
python main.py --platform xhs --type search

# Crawl specific platforms
python main.py --platform dy --type search    # Douyin
python main.py --platform wb --type search    # Weibo  
python main.py --platform bili --type search  # Bilibili

# Crawl types
python main.py --platform xhs --type detail    # Post details
python main.py --platform xhs --type creator   # Creator profiles
python main.py --platform xhs --type homefeed  # Home feed

# Alternative with uv (if available)
uv run main.py --platform xhs --type search
```

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync

# Type checking
mypy .

# Run tests
python -m pytest test/
```

### Database Setup
The system requires MySQL and Redis. Initialize database schema:
```bash
# Apply DDL scripts in order from schema/ directory
mysql -u user -p database < schema/tables.sql
```

## Configuration

### Key Configuration Files

1. **config/base_config.py**: Primary configuration
   - `PLATFORM`: Target platform ("xhs", "dy", "wb", etc.)
   - `KEYWORDS`: Search keywords (comma-separated)
   - `CRAWLER_TYPE`: "search", "detail", "creator", or "homefeed"
   - `SAVE_DATA_OPTION`: "db", "csv", or "json"
   - `CRAWLER_MAX_NOTES_COUNT`: Limit per crawl session
   - `ENABLE_GET_COMMENTS`: Enable comment crawling

2. **config/accounts_cookies.xlsx**: Account pool with cookies and proxies

3. **Database Configuration**: Set in config/db_config.py or environment variables

### Signature Service Dependency

This project requires the companion MediaCrawlerPro-SignSrv service for request signing. The signature service must be running before starting the crawler.

## Platform Support

Each platform in media_platform/ follows the same structure:
- **XHS (XiaoHongShu)**: Most mature implementation
- **Douyin**: TikTok crawler with video support
- **Weibo**: Microblog crawler
- **Bilibili**: Video platform crawler
- **Kuaishou**: Short video platform with GraphQL API
- **Tieba**: Baidu forum crawler
- **Zhihu**: Q&A platform crawler

## Data Storage

The system supports multiple storage backends:
- **Database (Recommended)**: MySQL with deduplication
- **CSV**: Simple file output
- **JSON**: Structured file output

Database tables are platform-specific and located in schema/ directory.

## Key Features

- **Multi-account Management**: Cookie rotation with IP proxy pairing
- **Checkpoint System**: Resume interrupted crawls using data/checkpoints/
- **Proxy Support**: IP rotation for stability
- **Comment Crawling**: Optional nested comment extraction
- **Data Deduplication**: Database-based duplicate detection

## Testing

Basic test suite in test/ directory:
- Unit tests for utilities and caching
- Test data processing functions
- Proxy pool testing

Run tests with: `python -m pytest test/`