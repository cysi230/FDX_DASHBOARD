#!/usr/bin/env python3
"""
프로젝트 유형 확인 스크립트
"""

import sqlite3
import os

def check_project_types():
    """현재 데이터베이스의 프로젝트 유형을 확인"""
    
    # 데이터베이스 경로 계산
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "db", "dashboard.db")
    
    print(f"🔍 데이터베이스 경로: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ 데이터베이스 파일이 존재하지 않습니다.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 프로젝트 유형 조회
        cursor.execute("SELECT type_id, type_name FROM project_type ORDER BY type_id")
        project_types = cursor.fetchall()
        
        print(f"\n📋 현재 등록된 프로젝트 유형 ({len(project_types)}개):")
        if project_types:
            for type_id, type_name in project_types:
                print(f"  - {type_id}: {type_name}")
        else:
            print("  ⚠️  등록된 프로젝트 유형이 없습니다.")
        
        # 프로젝트 유형별 프로젝트 수 확인
        cursor.execute("""
            SELECT pt.type_name, COUNT(p.project_id) as project_count
            FROM project_type pt
            LEFT JOIN projects p ON pt.type_id = p.type_id
            GROUP BY pt.type_id, pt.type_name
            ORDER BY pt.type_id
        """)
        type_counts = cursor.fetchall()
        
        print(f"\n📊 프로젝트 유형별 프로젝트 수:")
        for type_name, count in type_counts:
            print(f"  - {type_name}: {count}개")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 데이터베이스 조회 중 오류 발생: {e}")

def reset_to_two_types():
    """프로젝트 유형을 2개로 리셋"""
    print("\n🔄 프로젝트 유형을 2개로 리셋합니다...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "db/reset_db.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ 데이터베이스 리셋 완료")
            print(result.stdout)
            
            # 샘플 데이터 추가
            print("\n📊 샘플 데이터 추가 중...")
            result = subprocess.run([sys.executable, "db/sample_data.py"], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("✅ 샘플 데이터 추가 완료")
                print(result.stdout)
            else:
                print("⚠️  샘플 데이터 추가 실패")
                print(result.stderr)
        else:
            print("❌ 데이터베이스 리셋 실패")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 리셋 중 오류 발생: {e}")

def main():
    print("🔧 프로젝트 유형 확인")
    print("=" * 50)
    
    # 현재 프로젝트 유형 확인
    check_project_types()
    
    # 사용자에게 리셋 여부 확인
    response = input("\n프로젝트 유형을 2개(프로젝트/유지보수)로 리셋하시겠습니까? (y/N): ")
    if response.lower() in ['y', 'yes']:
        import sys
        reset_to_two_types()
        print("\n🔄 리셋 후 프로젝트 유형 확인:")
        check_project_types()
    else:
        print("\n⚠️  리셋을 건너뜁니다.")
    
    print("\n" + "=" * 50)
    print("🔧 확인 완료")

if __name__ == "__main__":
    main() 