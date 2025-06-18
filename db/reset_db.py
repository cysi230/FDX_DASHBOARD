import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def reset_database():
    """데이터베이스를 완전히 초기화하고 2개의 프로젝트 유형만 설정"""
    
    # 기존 데이터베이스 파일 삭제
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  기존 데이터베이스 파일 삭제됨")
    
    # 새 데이터베이스 생성
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. 부서
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """)

        # 2. 기술
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

        # 5. 사원-기술 매핑
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_mapping (
            employee_id INTEGER,
            skill_id INTEGER,
            PRIMARY KEY (employee_id, skill_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        );
        """)

        # 6. 프로젝트 (location을 TEXT 필드로 변경)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type_id INTEGER,
            location TEXT,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (type_id) REFERENCES project_type(type_id)
        );
        """)

        # 7. 프로젝트 배정
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignment (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            project_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        );
        """)

        # 8. 대시보드 뷰 (skills 필드를 직접 사용)
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

        # 9. 프로젝트 유형 데이터 삽입 (2개만)
        project_types = [
            ("프로젝트",),
            ("유지보수",)
        ]
        cursor.executemany("INSERT INTO project_type (type_name) VALUES (?)", project_types)
        
        print("✅ 프로젝트 유형 2개 설정 완료:")
        for type_name in project_types:
            print(f"  - {type_name[0]}")

        conn.commit()
        print("✅ 데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 중 오류 발생: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database() 