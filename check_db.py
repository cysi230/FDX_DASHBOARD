#!/usr/bin/env python3
"""
데이터베이스 상태 확인 및 초기화 스크립트
"""

import os
import sqlite3
import sys

def check_database():
    """데이터베이스 파일 존재 여부와 상태를 확인"""
    
    # 데이터베이스 경로 계산
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "db", "dashboard.db")
    
    print(f"🔍 데이터베이스 경로: {db_path}")
    
    # 데이터베이스 파일 존재 확인
    if os.path.exists(db_path):
        print("✅ 데이터베이스 파일이 존재합니다.")
        
        # 데이터베이스 연결 테스트
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # departments 테이블 존재 확인
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'")
            if cursor.fetchone():
                print("✅ departments 테이블이 존재합니다.")
                
                # 부서 데이터 확인
                cursor.execute("SELECT COUNT(*) FROM departments")
                count = cursor.fetchone()[0]
                print(f"📊 현재 부서 수: {count}개")
                
                if count > 0:
                    cursor.execute("SELECT department_id, name FROM departments")
                    departments = cursor.fetchall()
                    print("📋 등록된 부서:")
                    for dept_id, name in departments:
                        print(f"  - {dept_id}: {name}")
                else:
                    print("⚠️  부서 데이터가 없습니다.")
            else:
                print("❌ departments 테이블이 존재하지 않습니다.")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ 데이터베이스 연결 오류: {e}")
            return False
    else:
        print("❌ 데이터베이스 파일이 존재하지 않습니다.")
        return False

def initialize_database():
    """데이터베이스 초기화"""
    print("\n🔄 데이터베이스 초기화를 시작합니다...")
    
    try:
        # db/init_db.py 실행
        import subprocess
        result = subprocess.run([sys.executable, "db/init_db.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ 데이터베이스 초기화 완료")
            print(result.stdout)
        else:
            print("❌ 데이터베이스 초기화 실패")
            print(result.stderr)
            return False
            
        # 샘플 데이터 추가
        print("\n📊 샘플 데이터 추가 중...")
        result = subprocess.run([sys.executable, "db/sample_data.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ 샘플 데이터 추가 완료")
            print(result.stdout)
        else:
            print("⚠️  샘플 데이터 추가 실패 (무시 가능)")
            print(result.stderr)
            
        return True
        
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")
        return False

def main():
    print("🔧 FDX 대시보드 데이터베이스 상태 확인")
    print("=" * 50)
    
    # 데이터베이스 상태 확인
    if check_database():
        print("\n✅ 데이터베이스가 정상적으로 설정되어 있습니다.")
    else:
        print("\n❌ 데이터베이스에 문제가 있습니다.")
        
        # 사용자에게 초기화 여부 확인
        response = input("\n데이터베이스를 초기화하시겠습니까? (y/N): ")
        if response.lower() in ['y', 'yes']:
            if initialize_database():
                print("\n✅ 데이터베이스 초기화가 완료되었습니다.")
                check_database()  # 다시 확인
            else:
                print("\n❌ 데이터베이스 초기화에 실패했습니다.")
        else:
            print("\n⚠️  데이터베이스 초기화를 건너뜁니다.")
    
    print("\n" + "=" * 50)
    print("🔧 확인 완료")

if __name__ == "__main__":
    main() 