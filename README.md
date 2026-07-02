# Baoiam Backend

## Setup Steps

### 1. Clone the repo
git clone https://github.com/kajalgautam2105-art/baoiam_backend.git
cd baoiam_backend

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure .env
Copy .env.example to .env and fill in your values

### 5. Run the server
uvicorn app.main:app --reload

### 6. Health Check
GET http://localhost:8000/health
Response: {"status": "ok"}