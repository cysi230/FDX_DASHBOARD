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

        # 2. 기술 데이터
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

        # 3. 프로젝트 유형
        project_types = [
            ("신규 개발",),
            ("유지보수",),
            ("개선",),
            ("마이그레이션",),
            ("설치",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO project_type (type_name) VALUES (?)", project_types)

        # 4. 장소
        locations = [
            ("서울 본사",),
            ("부산 지사",),
            ("대구 지사",),
            ("광주 지사",),
            ("대전 지사",),
            ("원격",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO locations (name) VALUES (?)", locations)

        # 5. 사원 데이터
        employees = [
            ("김철수", "팀장", 1),
            ("이영희", "과장", 1),
            ("박민수", "대리", 1),
            ("정수진", "사원", 1),
            ("최지훈", "팀장", 2),
            ("한미영", "과장", 2),
            ("송태호", "대리", 3),
            ("윤서연", "사원", 3),
            ("임동현", "팀장", 4),
            ("강현우", "과장", 5)
        ]
        cursor.executemany("INSERT OR IGNORE INTO employees (name, position, department_id) VALUES (?, ?, ?)", employees)

        # 6. 프로젝트 데이터
        projects = [
            ("웹사이트 리뉴얼", 1, 1, "2024-01-01", "2024-06-30"),
            ("모바일 앱 개발", 1, 1, "2024-02-01", "2024-08-31"),
            ("시스템 유지보수", 2, 1, "2024-01-01", "2024-12-31"),
            ("데이터베이스 마이그레이션", 4, 2, "2024-03-01", "2024-05-31"),
            ("UI/UX 개선", 3, 1, "2024-04-01", "2024-07-31"),
            ("클라우드 인프라 구축", 1, 6, "2024-05-01", "2024-09-30")
        ]
        cursor.executemany("INSERT OR IGNORE INTO projects (name, type_id, site_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)", projects)

        # 7. 사원-기술 매핑
        skill_mappings = [
            (1, 1), (1, 2), (1, 3),  # 김철수: Python, JavaScript, React
            (2, 1), (2, 4), (2, 5),  # 이영희: Python, Vue.js, Node.js
            (3, 2), (3, 3), (3, 6),  # 박민수: JavaScript, React, Java
            (4, 1), (4, 7), (4, 8),  # 정수진: Python, Spring, MySQL
            (5, 13), (5, 14), (5, 15),  # 최지훈: Figma, Photoshop, Illustrator
            (6, 13), (6, 14),  # 한미영: Figma, Photoshop
            (7, 1), (7, 2), (7, 8),  # 송태호: Python, JavaScript, MySQL
            (8, 2), (8, 3), (8, 9),  # 윤서연: JavaScript, React, PostgreSQL
            (9, 11), (9, 12), (9, 8),  # 임동현: Docker, AWS, MySQL
            (10, 6), (10, 7), (10, 8)  # 강현우: Java, Spring, MySQL
        ]
        cursor.executemany("INSERT OR IGNORE INTO skill_mapping (employee_id, skill_id) VALUES (?, ?)", skill_mappings)

        # 8. 프로젝트 배정
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
        print(f"  - 장소: {len(locations)}개")
        print(f"  - 사원: {len(employees)}명")
        print(f"  - 프로젝트: {len(projects)}개")
        print(f"  - 기술 매핑: {len(skill_mappings)}개")
        print(f"  - 프로젝트 배정: {len(assignments)}개")

    except Exception as e:
        print(f"❌ 샘플 데이터 삽입 중 오류 발생: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    insert_sample_data() 