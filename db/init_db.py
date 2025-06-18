import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

# DB 파일 삭제 후 새로 만들고 싶다면 아래 주석 해제
# if os.path.exists(DB_PATH):
#     os.remove(DB_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. 부서
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # 2. 기술 (참조용으로만 유지)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # 3. 프로젝트 유형 (2가지로 제한)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_type (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT NOT NULL
    );
    """)

    # 4. 사원 (skills 필드 추가)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        department_id INTEGER,
        skills TEXT,
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
    );
    """)

    # 5. 프로젝트 (location을 TEXT 필드로 변경)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type_id INTEGER,
        location TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT DEFAULT '대기',
        FOREIGN KEY (type_id) REFERENCES project_type(type_id)
    );
    """)

    # 6. 프로젝트 배정
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignment (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        project_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );
    """)

    # 7. 대시보드 뷰 (skills 필드를 직접 사용)
    cursor.execute("DROP VIEW IF EXISTS vw_dashboard_summary;")  # 재생성 가능하도록
    cursor.execute("""
    CREATE VIEW vw_dashboard_summary AS
    SELECT
        p.project_id,
        p.name AS project_name,
        pt.type_name AS project_type,
        p.location AS site_name,
        p.start_date,
        p.end_date,
        e.employee_id,
        e.name AS employee_name,
        e.position,
        d.name AS department_name,
        e.skills
    FROM
        assignment a
    JOIN employees e ON a.employee_id = e.employee_id
    JOIN departments d ON e.department_id = d.department_id
    JOIN projects p ON a.project_id = p.project_id
    JOIN project_type pt ON p.type_id = pt.type_id;
    """)

    conn.commit()
    conn.close()
    print("✅ SQLite DB 및 뷰 초기화 완료!")

if __name__ == "__main__":
    init_db()
