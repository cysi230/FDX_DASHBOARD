#!/usr/bin/env python3
"""
FDX 대시보드 실행 스크립트
"""

import os
import sys
import subprocess

def check_dependencies():
    """필요한 패키지가 설치되어 있는지 확인"""
    try:
        import flask
        import pandas
        print("✅ 필요한 패키지가 모두 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"❌ 필요한 패키지가 설치되지 않았습니다: {e}")
        print("다음 명령어로 패키지를 설치해주세요:")
        print("pip install -r requirements.txt")
        return False

def check_database():
    """데이터베이스 파일이 존재하는지 확인"""
    db_path = os.path.join("db", "dashboard.db")
    if os.path.exists(db_path):
        print("✅ 데이터베이스 파일이 존재합니다.")
        return True
    else:
        print("❌ 데이터베이스 파일이 없습니다.")
        print("다음 명령어로 데이터베이스를 초기화해주세요:")
        print("cd db && python init_db.py")
        return False

def main():
    print("🚀 FDX 대시보드 시작 중...")
    print("-" * 50)
    
    # 의존성 확인
    if not check_dependencies():
        return
    
    # 데이터베이스 확인
    if not check_database():
        return
    
    print("-" * 50)
    print("🌐 웹 서버를 시작합니다...")
    print("브라우저에서 http://localhost:5000 으로 접속하세요.")
    print("서버를 중지하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    # Flask 애플리케이션 실행
    try:
        from dashboard.app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 서버가 종료되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 