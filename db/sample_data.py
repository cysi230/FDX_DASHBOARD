import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. 부서 데이터
        departments = [
            ("개발팀",),
            ("디자인팀",),
            ("기획팀",),
            ("운영팀",),
            ("QA팀",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO departments (name) VALUES (?)", departments)

        # 2. 기술 데이터 (참조용)
        skills = [
            ("Python",),
            ("JavaScript",),
            ("React",),
            ("Vue.js",),
            ("Node.js",),
            ("Java",),
            ("Spring",),
            ("MySQL",),
            ("PostgreSQL",),
            ("MongoDB",),
            ("Docker",),
            ("AWS",),
            ("Figma",),
            ("Photoshop",),
            ("Illustrator",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO skills (name) VALUES (?)", skills)

        # 3. 프로젝트 유형 (2가지로 제한)
        project_types = [
            ("프로젝트",),
            ("유지보수",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO project_type (type_name) VALUES (?)", project_types)

        # 4. 사원 데이터 (skills 필드 포함)
        employees = [
            ("김철수", "팀장", 1, "Python, JavaScript, React"),
            ("이영희", "과장", 1, "Python, Vue.js, Node.js"),
            ("박민수", "대리", 1, "JavaScript, React, Java"),
            ("정수진", "사원", 1, "Python, Spring, MySQL"),
            ("최지훈", "팀장", 2, "Figma, Photoshop, Illustrator"),
            ("한미영", "과장", 2, "Figma, Photoshop"),
            ("송태호", "대리", 3, "Python, JavaScript, MySQL"),
            ("윤서연", "사원", 3, "JavaScript, React, PostgreSQL"),
            ("임동현", "팀장", 4, "Docker, AWS, MySQL"),
            ("강현우", "과장", 5, "Java, Spring, MySQL")
        ]
        cursor.executemany("INSERT OR IGNORE INTO employees (name, position, department_id, skills) VALUES (?, ?, ?, ?)", employees)

        # 5. 프로젝트 데이터 (location을 TEXT로 직접 입력)
        projects = [
            ("웹사이트 리뉴얼", 1, "서울 본사", "2024-01-01", "2024-06-30"),
            ("모바일 앱 개발", 1, "서울 본사", "2024-02-01", "2024-08-31"),
            ("시스템 유지보수", 2, "서울 본사", "2024-01-01", "2024-12-31"),
            ("데이터베이스 마이그레이션", 1, "부산 지사", "2024-03-01", "2024-05-31"),
            ("UI/UX 개선", 1, "서울 본사", "2024-04-01", "2024-07-31"),
            ("클라우드 인프라 구축", 1, "원격", "2024-05-01", "2024-09-30")
        ]
        cursor.executemany("INSERT OR IGNORE INTO projects (name, type_id, location, start_date, end_date) VALUES (?, ?, ?, ?, ?)", projects)

        # 6. 프로젝트 배정
        assignments = [
            (1, 1), (2, 1), (3, 1),  # 웹사이트 리뉴얼: 김철수, 이영희, 박민수
            (2, 2), (4, 2), (5, 2),  # 모바일 앱 개발: 이영희, 정수진, 최지훈
            (1, 3), (3, 3), (10, 3),  # 시스템 유지보수: 김철수, 박민수, 강현우
            (4, 4), (8, 4), (9, 4),  # 데이터베이스 마이그레이션: 정수진, 윤서연, 임동현
            (5, 5), (6, 5), (7, 5),  # UI/UX 개선: 최지훈, 한미영, 송태호
            (1, 6), (9, 6), (10, 6)  # 클라우드 인프라 구축: 김철수, 임동현, 강현우
        ]
        cursor.executemany("INSERT OR IGNORE INTO assignment (employee_id, project_id) VALUES (?, ?)", assignments)

        conn.commit()
        print("✅ 샘플 데이터 삽입 완료!")
        print(f"  - 부서: {len(departments)}개")
        print(f"  - 기술: {len(skills)}개")
        print(f"  - 프로젝트 유형: {len(project_types)}개")
        print(f"  - 사원: {len(employees)}명")
        print(f"  - 프로젝트: {len(projects)}개")
        print(f"  - 프로젝트 배정: {len(assignments)}개")

    except Exception as e:
        print(f"❌ 샘플 데이터 삽입 중 오류 발생: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    insert_sample_data() 