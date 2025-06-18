import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def migrate_assignment_table():
    """assignment 테이블에 start_date, end_date, role 컬럼 추가"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 기존 컬럼 확인
        cursor.execute("PRAGMA table_info(assignment)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # start_date 컬럼 추가
        if 'start_date' not in columns:
            cursor.execute("ALTER TABLE assignment ADD COLUMN start_date TEXT")
            print("✅ start_date 컬럼 추가 완료")
        
        # end_date 컬럼 추가
        if 'end_date' not in columns:
            cursor.execute("ALTER TABLE assignment ADD COLUMN end_date TEXT")
            print("✅ end_date 컬럼 추가 완료")
        
        # role 컬럼 추가
        if 'role' not in columns:
            cursor.execute("ALTER TABLE assignment ADD COLUMN role TEXT")
            print("✅ role 컬럼 추가 완료")
        
        conn.commit()
        print("✅ assignment 테이블 마이그레이션 완료!")
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_assignment_table() 