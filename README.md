
# 🧭 Travel Planner Backend

This is the Django REST API backend for the **Travel Planner App**, which creates personalized travel plans based on user **budget**, **region**, **currency**, and **lifestyle**, and allows confirming and listing saved trips.

---

## ⚙️ Tech Stack

- Python 3.12
- Django 5
- Django REST Framework
- SQLite (local development)
- Pandas (activity planning logic)

---

## 📁 Project Structure

```
travel-planner-backend/
├── ml_models/
│   ├── planner.py              # Travel plan generation logic
│   └── data/activities.csv     # Main dataset of activities
├── trips/
│   ├── models.py               # ConfirmedTrip model
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   ├── urls.py                 # App routing
├── config/
│   └── settings.py             # Project configuration
├── db.sqlite3                  # Local SQLite database
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/travel-planner-backend.git
cd travel-planner-backend
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # or 'env\Scripts\activate' on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Backend runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌍 API Endpoints

### 🔄 `POST /api/plan/`

Generates three personalized travel plans based on user preferences.

**Payload:**
```json
{
  "budget": 1000,
  "currency": "EUR",
  "region": "marrakesh",
  "lifestyle": "explorer"
}
```

**Response:**
```json
{
  "plans": [
    {
      "id": "...",
      "title": "...",
      "description": "...",
      "activities": [...],
      "totalCost": 1234,
      "duration": "3 days",
      "accommodation": {...}
    },
    ...
  ]
}
```

---

### ✅ `POST /api/confirm-trip/`

Confirms and saves a selected plan to the database.

**Payload:**
```json
{
  "region": "marrakesh",
  "budget": 1200,
  "currency": "EUR",
  "lifestyle": "explorer",
  "selectedPlan": {
    "id": "...",
    "title": "...",
    "activities": [...],
    ...
  }
}
```

**Response:**
```json
{
  "status": "confirmed",
  "message": "Trip successfully saved!",
  "data": { ... }
}
```

---

### 📦 `GET /api/confirmed-trips/`

Fetch confirmed trips (optionally filtered by `region` and/or `lifestyle`).

**Examples:**
```
GET /api/confirmed-trips/
GET /api/confirmed-trips/?region=marrakesh
GET /api/confirmed-trips/?lifestyle=food_lover
```

**Response:**
```json
[
  {
    "region": "...",
    "budget": ...,
    "currency": "...",
    "lifestyle": "...",
    "selected_plan": {...},
    ...
  },
  ...
]
```

---

## 🧾 Dataset

Your dataset (`activities.csv`) is located in `ml_models/data/` and includes fields like:

- `activity_name`, `region`, `lifestyle`, `cost_mad`, `duration_hrs`
- `description`, `type`, `difficulty`, `rating`, etc.

Each activity is labeled for use by lifestyle type: `food_lover`, `explorer`, or `comfort_seeker`.

---

## 🧪 API Testing with Postman

### Generate Plans:
- Method: `POST`
- URL: `http://127.0.0.1:8000/api/plan/`
- Body (JSON):
```json
{
  "budget": 1500,
  "currency": "USD",
  "region": "agadir",
  "lifestyle": "food_lover"
}
```

### Confirm a Trip:
- Method: `POST`
- URL: `http://127.0.0.1:8000/api/confirm-trip/`
- Body (JSON): Pass one of the plans from above into `selectedPlan`.

### Get Confirmed Trips:
- Method: `GET`
- URL: `http://127.0.0.1:8000/api/confirmed-trips/`

---

## 🧠 Future Improvements

- Add authentication (JWT)
- Export confirmed trips to PDF
- Fetch real-time currency rates via an API
- Add seasonal filtering and time-based suggestions
- Auto-email trip summary upon confirmation

---

