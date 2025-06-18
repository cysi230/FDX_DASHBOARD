# FDX 대시보드

프로젝트 및 사원 관리를 위한 웹 기반 대시보드 애플리케이션입니다.

## ✨ 주요 기능

- 📊 **전체 요약**: 모든 프로젝트와 사원 정보를 한눈에 확인
- 🛠 **유지보수 프로젝트**: 유지보수 타입의 프로젝트만 필터링하여 조회
- ⏳ **진행 중인 프로젝트**: 현재 진행 중인 프로젝트 조회
- 👥 **프로젝트별 인원**: 프로젝트에 배정된 사원 정보 조회
- 👤 **사원 관리**: 사원 등록 및 조회 (부서, 기술 스택 포함)
- 📁 **프로젝트 관리**: 프로젝트 등록 및 조회 (유형, 장소, 기간 포함)
- 🔗 **프로젝트 배정**: 사원을 프로젝트에 배정하는 기능

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone <repository-url>
cd FDX_DASHBOARD
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화
```bash
cd db
python init_db.py
python sample_data.py  # 샘플 데이터 추가 (선택사항)
cd ..
```

### 4. 애플리케이션 실행
```bash
python run.py
```

### 5. 브라우저에서 접속
```
http://localhost:5000
```

## 📁 프로젝트 구조

```
FDX_DASHBOARD/
├── dashboard/
│   ├── app.py              # Flask 애플리케이션 메인 파일
│   ├── query.py            # 데이터베이스 쿼리 함수들
│   └── templates/          # HTML 템플릿
│       ├── dashboard.html  # 메인 대시보드 템플릿
│       ├── employee_add.html
│       ├── project_add.html
│       └── assignment_add.html
├── db/
│   ├── dashboard.db        # SQLite 데이터베이스
│   ├── init_db.py         # 데이터베이스 초기화 스크립트
│   └── sample_data.py     # 샘플 데이터 삽입 스크립트
├── requirements.txt        # Python 패키지 의존성
├── run.py                 # 애플리케이션 실행 스크립트
└── README.md
```

## 🗄️ 데이터베이스 스키마

- **departments**: 부서 정보
- **skills**: 기술 스택 정보
- **project_type**: 프로젝트 유형
- **locations**: 프로젝트 장소
- **employees**: 사원 정보
- **skill_mapping**: 사원-기술 매핑
- **projects**: 프로젝트 정보
- **assignment**: 프로젝트-사원 배정

## 💡 사용법

### 대시보드 조회
1. **전체 요약**: 모든 프로젝트와 사원 정보를 한눈에 확인
2. **유지보수 프로젝트**: 유지보수 타입의 프로젝트만 필터링
3. **진행 중인 프로젝트**: 현재 진행 중인 프로젝트 조회
4. **프로젝트별 인원**: 프로젝트에 배정된 사원 정보 조회

### 데이터 관리
1. **사원 등록**: 사이드바의 "사원 등록" 또는 사원 목록 페이지의 "사원 등록" 버튼
2. **프로젝트 등록**: 사이드바의 "프로젝트 등록" 또는 프로젝트 목록 페이지의 "프로젝트 등록" 버튼
3. **프로젝트 배정**: 사이드바의 "프로젝트 배정" 또는 프로젝트별 인원 페이지의 "프로젝트 배정" 버튼

## 🔧 주요 개선사항

### 에러 처리 및 검증
- ✅ 데이터베이스 연결 실패 시 적절한 에러 메시지 표시
- ✅ 폼 입력값 검증 (필수 필드, 날짜 형식 등)
- ✅ 중복 데이터 입력 방지
- ✅ Flash 메시지를 통한 사용자 피드백

### 사용자 경험 개선
- ✅ 사이드바에 모든 기능에 대한 직관적인 네비게이션
- ✅ 각 페이지에 관련 액션 버튼 추가
- ✅ Bootstrap을 활용한 반응형 디자인
- ✅ 성공/실패 메시지 표시

### 기능 확장
- ✅ 프로젝트 배정 기능 추가
- ✅ 샘플 데이터 제공
- ✅ 실행 스크립트로 쉬운 시작
- ✅ 의존성 관리 (requirements.txt)

## 🛠️ 기술 스택

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5
- **Data Processing**: Pandas
- **Template Engine**: Jinja2

## 📝 개발 가이드

### 새로운 기능 추가
1. `dashboard/app.py`에 라우트 추가
2. `dashboard/query.py`에 필요한 쿼리 함수 추가
3. `dashboard/templates/`에 HTML 템플릿 생성
4. 필요시 데이터베이스 스키마 수정

### 데이터베이스 수정
1. `db/init_db.py`에서 테이블 구조 수정
2. 기존 데이터베이스 파일 삭제 후 재생성
3. `db/sample_data.py`에서 샘플 데이터 업데이트

## 🐛 문제 해결

### 일반적인 문제
1. **패키지 설치 오류**: `pip install -r requirements.txt` 재실행
2. **데이터베이스 오류**: `db/init_db.py` 재실행
3. **포트 충돌**: 다른 포트 사용 또는 기존 프로세스 종료

### 로그 확인
- Flask 디버그 모드에서 상세한 오류 정보 확인 가능
- 콘솔에서 데이터베이스 연결 및 쿼리 오류 확인

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
