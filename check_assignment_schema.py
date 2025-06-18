import sqlite3
import os

DB_PATH = os.path.join("db", "dashboard.db")

def check_assignment_schema():
    """assignment 테이블의 스키마 확인"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 테이블 정보 조회
        cursor.execute("PRAGMA table_info(assignment)")
        columns = cursor.fetchall()
        
        print("📋 assignment 테이블 스키마:")
        print("=" * 50)
        for column in columns:
            print(f"컬럼명: {column[1]}, 타입: {column[2]}, NULL 허용: {column[3]}, 기본값: {column[4]}")
        
        # 기존 데이터 확인
        cursor.execute("SELECT COUNT(*) FROM assignment")
        count = cursor.fetchone()[0]
        print(f"\n📊 현재 배정 데이터 수: {count}개")
        
        if count > 0:
            cursor.execute("SELECT * FROM assignment LIMIT 3")
            sample_data = cursor.fetchall()
            print("\n📝 샘플 데이터:")
            for row in sample_data:
                print(row)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_assignment_schema() 