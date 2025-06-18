import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def reset_db():
    # 기존 DB 파일 삭제
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("기존 데이터베이스 파일 삭제 완료")
    
    # 새로 생성
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

    # 5. 프로젝트 (status 필드 추가)
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
        p.status,
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

    # 샘플 데이터 삽입
    # 부서
    cursor.execute("INSERT INTO departments (name) VALUES ('개발팀')")
    cursor.execute("INSERT INTO departments (name) VALUES ('인프라팀')")
    cursor.execute("INSERT INTO departments (name) VALUES ('보안팀')")
    
    # 프로젝트 유형
    cursor.execute("INSERT INTO project_type (type_name) VALUES ('프로젝트')")
    cursor.execute("INSERT INTO project_type (type_name) VALUES ('유지보수')")
    
    # 사원
    cursor.execute("INSERT INTO employees (name, position, department_id, skills) VALUES ('김철수', '팀장', 1, 'Python, Django, React')")
    cursor.execute("INSERT INTO employees (name, position, department_id, skills) VALUES ('이영희', '개발자', 1, 'Java, Spring, MySQL')")
    cursor.execute("INSERT INTO employees (name, position, department_id, skills) VALUES ('박민수', '시스템관리자', 2, 'Linux, Docker, AWS')")
    
    # 프로젝트
    cursor.execute("INSERT INTO projects (name, type_id, location, start_date, end_date, status) VALUES ('웹사이트 구축', 1, '서울', '2024-01-01', '2024-06-30', '진행중')")
    cursor.execute("INSERT INTO projects (name, type_id, location, start_date, end_date, status) VALUES ('서버 유지보수', 2, '부산', '2024-02-01', '2024-12-31', '진행중')")
    cursor.execute("INSERT INTO projects (name, type_id, location, start_date, end_date, status) VALUES ('보안 시스템 구축', 1, '대구', '2024-03-01', '2024-08-31', '대기')")
    
    # 프로젝트 배정
    cursor.execute("INSERT INTO assignment (employee_id, project_id) VALUES (1, 1)")
    cursor.execute("INSERT INTO assignment (employee_id, project_id) VALUES (2, 1)")
    cursor.execute("INSERT INTO assignment (employee_id, project_id) VALUES (3, 2)")

    conn.commit()
    conn.close()
    print("✅ 데이터베이스 재생성 및 샘플 데이터 삽입 완료!")

if __name__ == "__main__":
    reset_db() 