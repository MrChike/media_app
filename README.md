# 🎬 Media APP

## 📚 Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Description

This project serves as a scaffolding tool for building Python applications that are production-ready. It emphasizes **modularity**, **scalability**, and a clear **separation of concerns**, providing a solid foundation for developing maintainable and well-structured codebases.

Whether you're starting a new project or looking to standardize your development practices, this scaffold helps you adopt best practices from the ground up.

## Installation

Clone the repo and the application locally:

```bash
# 🎬 Clone the media_app project
git clone --branch=seriesB https://github.com/MrChike/media_app.git
cd media_app

# 📦 Setup environment
cp .example.env .env  # Populate .env with your local credentials

# 🐍 Create and activate virtual environment
python3 -m venv env && source env/bin/activate

# 📥 Install dependencies
pip install -r requirements.txt

# 🚀 Launch Project
docker-compose -f docker-compose.db.yaml -f docker-compose.api.yaml up --build
```

## 📚 Full Tutorial Available

You can follow the full walkthrough of [`🔥SeriesA`](https://dev.to/mrchike/fastapi-in-production-build-scale-deploy-series-a-codebase-design-ao3), [`🛠️SeriesB`](https://dev.to/mrchike/fastapi-in-production-build-scale-deploy-series-b-services-queues-containers-2i08) on [**DEV**](https://dev.to/mrchike/). it covers everything from project setup, architecture decisions, dependency injection, and async patterns in production-grade FastAPI apps.

## 🗂️ Project Structure

Below is the project layout, along with the defined responsibility of each file and folder:

```bash
media_app/

├── base/                                # Core feature module
│   ├── __init__.py
│   ├── router.py                        # Defines HTTP API endpoints and maps them to controller functions
│   ├── controller.py                    # Handles request-response cycle; delegates business logic to services
│   ├── service.py                       # Core business logic for async I/O operations
│   ├── model.py                         # SQLAlchemy ORM models representing database tables
│   ├── schema.py                        # Pydantic models for input validation and output serialization
│   ├── dependencies.py                  # Module-specific DI components like authentication and DB sessions
│   └── tasks.py                         # Core business logic for CPU-bound operations

├── movies/                              # Movie feature module (same layout as base)
│   ├── __init__.py
│   ├── router.py
│   ├── controller.py
│   ├── service.py
│   ├── model.py
│   ├── schema.py
│   ├── dependencies.py
│   └── tasks.py

├── static/                              # (Optional) Static files (e.g., images, CSS)
├── templates/                           # (Optional) Jinja2 or HTML templates for frontend rendering
├── docs/                                # (Optional) API documentation, design specs, or OpenAPI enhancements

├── shared/                              # Project-wide shared codebase
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base_settings.py             # Base config for environments
│   │   └── settings.py                  # Pydantic-based config management
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py                # DB engine/session handling
│   ├── dependencies/                    # Shared DI functions (e.g., auth, DB session)
│   │   └── __init__.py
│   ├── middleware/                      # Global middlewares (e.g., logging, error handling)
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── external_apis/               # Third-party integrations
│   │   │   ├── __init__.py
│   │   │   └── omdb_movies.py           # Integration with OMDB API
│   │   └── internal_operations/         # CPU-intensive logic, background tasks
│   │       └── __init__.py
│   └── utils/                           # Generic helpers
│       ├── __init__.py
│       └── fetch_request_with_error_handling.py  # Error-resilient HTTP requests

├── scripts/                             # Developer or DevOps utilities
│   ├── __init__.py
│   └── sanity_check.py                  # A friendly reminder not to lose your mind while debugging

tests/                                     # Root of all tests
├── __init__.py
│
├── unit/                                  # Fast, isolated logic-level tests
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   └── test_service.py
│   └── movies/
│       ├── __init__.py
│       ├── test_controller.py
│       ├── test_service.py
│       └── test_tasks.py
│
├── integration/                           # DB/API/network dependent tests
│   ├── __init__.py
│
├── e2e/                                   # High-level, full user flow tests
│   ├── __init__.py
│
├── system/                                # System resilience, performance, fault-tolerance tests
│   ├── __init__.py

├── migrations/                          # Alembic migration files
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/                        # Versioned migration scripts

├── alembic.ini                          # Alembic configuration for database migrations
├── celeryconfig.py                      # Celery settings for async task queue

├── docker-compose.api.yaml              # Docker Compose API
├── docker-compose.db.yaml               # Docker Compose DB
├── Dockerfile                           # Base app Dockerfile
├── Dockerfile.nginx                     # Nginx reverse proxy Dockerfile
├── nginx.conf                           # Nginx configuration
├── entrypoint.sh                        # Shell script to run app container
├── series_a_setup.sh                    # SeriesA Environment setup script
├── series_b_setup.sh                    # SeriesB Environment setup script

├── .example.env                         # Template for environment variables
├── .coveragerc                          # Code coverage settings
├── .gitignore                           # Files and folders ignored by Git

├── main.py                              # FastAPI application entrypoint
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Python dependency list
├── JOURNAL.md                           # Development log: issues faced, solutions, and resources
└── README.md                            # Project overview, setup, and usage

```

## Usage

Run `docker-compose -f docker-compose.db.yaml -f docker-compose.api.yaml up --build` in the root directory of the project to start the application locally.

## Features

- 🎬 Modular architecture with separate domains for Movies
- 🧩 Well-defined API layer with routers, controllers, and dependency injection
- ⚙️ Centralized configuration management under shared/config with Pydantic settings
- 🔗 Integration with external APIs (OMDb) in shared/services/external_apis
- 📜 Comprehensive project documentation and logs maintained in docs and JOURNAL.md
- 📁 Static assets management for project documentation
- 🧪 Unit tests covering controllers, tasks and services for movie module
- 🐞 Graceful exception handling with low-level error logging for internal teams and user-friendly messages for a smooth experience.
- 🔧 Utility and helper functions centralized in shared/utils for reuse across modules
- 🐳 Dockerized environment including app, Nginx reverse proxy, and Redis for Celery broker/backend
- 📦 Database Setup and Integration for Redis, Postgres & MongoDB
- 📦 Database management with Alembic migrations and SQLAlchemy models per module
- ⚡ Caching layer with Redis or Memcached for improved performance
- 🚀 Asynchronous task processing using Celery for CPU-intensive tasks offloaded to workers

## Upcoming Features (Series-X)

- 🧪 Integration, System and E2E tests covering controllers, tasks and services for all modules
- 🔒 Middleware for cross-cutting concerns and security
- 🎯 JWT-based user authentication and profile management
- 🔔 Notifications system for updates, new releases, and user interactions
- 🌐 Localization and internationalization for multi-language and regional support
- 🛡️ IP-based rate limiting (e.g., via Redis or FastAPI-limiter)
- 🚀 CI/CD pipeline setup for automated testing, build, and deployment
- 🔐 OAuth2 support (e.g., Google or GitHub login)
- 📄 Audit logs for user actions and system changes
- 👥 User registration and management system
- 🔑 Password reset flow
- 👮‍♂️ Role-based access control (RBAC) or attribute-based access control (ABAC)
- 📬 Email verification and support
- 📊 Event tracking for analytics (e.g., user interactions, API usage)
- 🔍 Search capabilities (e.g., Elasticsearch integration for advanced movie/actor queries)
- 💾 Data export/import utilities (CSV, JSON)
- 🔐 Brute force protection on login routes
- 🌍 Multitenancy / SaaS Setup
- 📹 Integration with multiple cloud storage (e.g., S3) for media uploads

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## Acknowledgements

- Firstly, I want to acknowledge myself for staying committed to continuous learning and growth in a challenging field.
- This section will be updated as the project evolves...

## Contact

Feel free to connect with me on

- 💼 [LinkedIn](https://www.linkedin.com/in/chikeegonu/)
- 🐙 [Github](https://github.com/MrChike)
