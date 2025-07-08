# 🚀 Getting Started

## Installation

```bash
# 🎬 Clone the media_app project
git clone https://github.com/MrChike/media_app.git
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
