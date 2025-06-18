# query.py
import sqlite3
import os
import pandas as pd

# 현재 파일의 디렉토리를 기준으로 상위 디렉토리의 db 폴더를 찾음
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(parent_dir, "db", "dashboard.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 컬럼명을 딕셔너리 형태로 접근 가능하게 설정
    return conn

def get_all_summary():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM vw_dashboard_summary", conn)
    conn.close()
    return df

def get_maintenance_projects():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM vw_dashboard_summary 
        WHERE project_type = '유지보수'
    """, conn)
    conn.close()
    return df

def get_ongoing_projects():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM vw_dashboard_summary 
        WHERE date('now') BETWEEN start_date AND end_date
    """, conn)
    conn.close()
    return df

def get_project_assignment_list():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT project_name, employee_name, position, skills
        FROM vw_dashboard_summary
        ORDER BY project_name, employee_name
    """, conn)
    conn.close()
    return df

def get_all_employees():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT e.employee_id, e.name, e.position, d.name AS department, e.skills
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        ORDER BY e.employee_id
    """, conn)
    conn.close()
    return df

def get_all_projects():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT p.project_id, p.name, pt.type_name AS type, p.location AS site, 
               p.start_date, p.end_date
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        ORDER BY p.project_id
    """, conn)
    conn.close()
    return df

def get_all_departments():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT d.department_id, d.name,
            COUNT(e.employee_id) AS employee_count
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.name
        ORDER BY d.department_id
    """, conn)
    conn.close()
    return df
