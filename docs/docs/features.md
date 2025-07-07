# ✨ Features

## Project Features

- 🎬 Modular architecture with separate domains for Movies
- 🧩 Well-defined API layer with routers, controllers, and dependency injection
- ⚙️ Centralized configuration management under shared/config with Pydantic settings
- 🔗 Integration with external APIs (OMDb) in shared/services/external_apis
- 📜 Comprehensive project documentation and logs maintained in docs and JOURNAL.md
- 🧪 Unit tests covering controllers, tasks and services for movie module
- 🐞 Graceful exception handling with low-level error logging for internal teams and user-friendly messages for a smooth experience.
- 🔧 Utility and helper functions centralized in shared/utils for reuse across modules
- 🐳 Dockerized environment including app, Nginx reverse proxy, and Redis for Celery broker/backend
- 📦 Database Setup and Integration for Redis, Postgres & MongoDB
- 📦 Database management with Alembic migrations and SQLAlchemy models per module
- ⚡ Caching layer with Redis or Memcached for improved performance
- 🚀 Asynchronous task processing using Celery for CPU-intensive tasks offloaded to workers