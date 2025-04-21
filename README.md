# Simple Flask API for Database Migration

This API allows uploading historical data from CSV files into a SQL database.

## Features

- Uses Flask and SQLAlchemy
- SQLite database by default
- Predefined schema for departments, jobs, and employees

## How to Run

1. Install dependencies:

```bash
pip install flask sqlalchemy
```

2. Run the API:

```bash
python app.py
```

## Database Tables

- `departments(id, department)`
- `jobs(id, job)`
- `hired_employees(id, name, datetime, department_id, job_id)`