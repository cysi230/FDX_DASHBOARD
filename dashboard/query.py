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
    df = pd.read_sql_query("""
        SELECT 
            p.project_id,
            p.name AS project_name,
            pt.type_name AS project_type,
            p.location AS site_name,
            p.start_date,
            p.end_date,
            p.status,
            GROUP_CONCAT(e.name) AS employees
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        LEFT JOIN assignment a ON p.project_id = a.project_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
        GROUP BY p.project_id, p.name, pt.type_name, p.location, p.start_date, p.end_date, p.status
        ORDER BY p.project_id
    """, conn)
    
    # employees 컬럼의 사원들을 정렬
    if not df.empty and 'employees' in df.columns:
        df['employees'] = df['employees'].apply(lambda x: ', '.join(sorted(x.split(', '))) if x else None)
    
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
        SELECT a.assignment_id, project_name, employee_name, position, skills
        FROM vw_dashboard_summary vw
        JOIN assignment a ON vw.employee_id = a.employee_id AND vw.project_id = a.project_id
        ORDER BY project_name, employee_name
    """, conn)
    conn.close()
    return df

def get_project_assignment_grouped():
    """프로젝트별로 사원들을 그룹화하여 한 줄에 표시"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            p.project_id,
            p.name AS project_name,
            pt.type_name AS project_type,
            p.location,
            p.start_date,
            p.end_date,
            p.status,
            GROUP_CONCAT(e.name) AS employees
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        LEFT JOIN assignment a ON p.project_id = a.project_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
        GROUP BY p.project_id, p.name, pt.type_name, p.location, p.start_date, p.end_date, p.status
        ORDER BY p.project_id
    """, conn)
    
    # employees 컬럼의 사원들을 정렬
    if not df.empty and 'employees' in df.columns:
        df['employees'] = df['employees'].apply(lambda x: ', '.join(sorted(x.split(', '))) if x else None)
    
    conn.close()
    return df

def get_ongoing_projects_grouped():
    """진행중인 프로젝트를 사원 그룹화하여 표시"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            p.project_id,
            p.name AS project_name,
            pt.type_name AS project_type,
            p.location,
            p.start_date,
            p.end_date,
            p.status,
            GROUP_CONCAT(e.name) AS employees
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        LEFT JOIN assignment a ON p.project_id = a.project_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
        WHERE date('now') BETWEEN p.start_date AND p.end_date
        GROUP BY p.project_id, p.name, pt.type_name, p.location, p.start_date, p.end_date, p.status
        ORDER BY p.project_id
    """, conn)
    
    # employees 컬럼의 사원들을 정렬
    if not df.empty and 'employees' in df.columns:
        df['employees'] = df['employees'].apply(lambda x: ', '.join(sorted(x.split(', '))) if x else None)
    
    conn.close()
    return df

def get_maintenance_projects_grouped():
    """유지보수 프로젝트를 사원 그룹화하여 표시"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            p.project_id,
            p.name AS project_name,
            pt.type_name AS project_type,
            p.location,
            p.start_date,
            p.end_date,
            p.status,
            GROUP_CONCAT(e.name) AS employees
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        LEFT JOIN assignment a ON p.project_id = a.project_id
        LEFT JOIN employees e ON a.employee_id = e.employee_id
        WHERE pt.type_name = '유지보수'
        GROUP BY p.project_id, p.name, pt.type_name, p.location, p.start_date, p.end_date, p.status
        ORDER BY p.project_id
    """, conn)
    
    # employees 컬럼의 사원들을 정렬
    if not df.empty and 'employees' in df.columns:
        df['employees'] = df['employees'].apply(lambda x: ', '.join(sorted(x.split(', '))) if x else None)
    
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
               p.start_date, p.end_date, p.status
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

def get_project_assignment_detail(project_id):
    """특정 프로젝트의 배정 상세 정보 조회"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            a.assignment_id,
            e.employee_id,
            e.name AS employee_name,
            e.position,
            d.name AS department,
            e.skills
        FROM assignment a
        JOIN employees e ON a.employee_id = e.employee_id
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE a.project_id = ?
        ORDER BY e.name
    """, conn, params=(project_id,))
    conn.close()
    return df

def get_project_info(project_id):
    """특정 프로젝트 정보 조회"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            p.project_id,
            p.name AS project_name,
            pt.type_name AS project_type,
            p.location,
            p.start_date,
            p.end_date,
            p.status
        FROM projects p
        LEFT JOIN project_type pt ON p.type_id = pt.type_id
        WHERE p.project_id = ?
    """, conn, params=(project_id,))
    conn.close()
    return df

def get_assignment_info(assignment_id):
    """특정 배정 정보 조회"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            a.assignment_id,
            a.project_id,
            a.employee_id,
            a.start_date,
            a.end_date,
            a.role,
            e.name AS employee_name,
            p.name AS project_name
        FROM assignment a
        JOIN employees e ON a.employee_id = e.employee_id
        JOIN projects p ON a.project_id = p.project_id
        WHERE a.assignment_id = ?
    """, conn, params=(assignment_id,))
    conn.close()
    return df
