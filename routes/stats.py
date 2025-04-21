from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/hires-per-quarter-2021', methods=['GET'])
def hires_per_quarter_2021():
    query = """
    SELECT
        d.department,
        j.job,
        COUNT(CASE WHEN strftime('%m', he.datetime) BETWEEN '01' AND '03' THEN 1 END) AS Q1,
        COUNT(CASE WHEN strftime('%m', he.datetime) BETWEEN '04' AND '06' THEN 1 END) AS Q2,
        COUNT(CASE WHEN strftime('%m', he.datetime) BETWEEN '07' AND '09' THEN 1 END) AS Q3,
        COUNT(CASE WHEN strftime('%m', he.datetime) BETWEEN '10' AND '12' THEN 1 END) AS Q4
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
    WHERE strftime('%Y', he.datetime) = '2021'
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job;
    """

    with engine.connect() as conn:
        result = conn.execute(text(query)).mappings().all()
        data = [dict(row) for row in result]
    return jsonify(data)

@stats_bp.route('/stats/top-departments-hired', methods=['GET'])
def top_departments_hired():
    query = """
        SELECT
            d.id,
            d.department,
            COUNT(he.id) AS hired
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        WHERE strftime('%Y', he.datetime) = '2021'
        GROUP BY d.id, d.department
        HAVING COUNT(he.id) > (
            SELECT AVG(hired_count) FROM (
                SELECT COUNT(*) AS hired_count
                FROM hired_employees
                WHERE strftime('%Y', datetime) = '2021'
                GROUP BY department_id
            )
        )
        ORDER BY hired DESC;
    """

    with engine.connect() as conn:
        result = conn.execute(text(query)).mappings().all()
        data = [dict(row) for row in result]
    return jsonify(data)