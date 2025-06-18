from flask import Flask, render_template
import sys
import os
from query import get_all_employees, get_all_projects, get_all_departments  # 상단에 추가
from flask import request, redirect, url_for, flash
import sqlite3
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from query import (
    get_all_summary,
    get_maintenance_projects,
    get_ongoing_projects,
    get_project_assignment_list
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Flash 메시지를 위한 시크릿 키

def get_connection():
    try:
        # 현재 파일의 디렉토리를 기준으로 상위 디렉토리의 db 폴더를 찾음
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        db_path = os.path.join(parent_dir, "db", "dashboard.db")
        print(f"데이터베이스 경로: {db_path}")  # 디버깅용
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None

@app.route("/")
def home():
    try:
        data = get_all_summary()
        return render_template("dashboard.html", title="전체 요약", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="전체 요약", data=pd.DataFrame())

@app.route("/maintenance")
def maintenance():
    try:
        data = get_maintenance_projects()
        return render_template("dashboard.html", title="유지보수 프로젝트", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="유지보수 프로젝트", data=pd.DataFrame())

@app.route("/ongoing")
def ongoing():
    try:
        data = get_ongoing_projects()
        return render_template("dashboard.html", title="진행 중인 프로젝트", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="진행 중인 프로젝트", data=pd.DataFrame())

@app.route("/assignment")
def assignment():
    try:
        data = get_project_assignment_list()
        return render_template("dashboard.html", title="프로젝트별 인원", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="프로젝트별 인원", data=pd.DataFrame())

@app.route("/employees")
def employee_page():
    try:
        df = get_all_employees()
        return render_template("dashboard.html", title="사원 목록", data=df)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="사원 목록", data=pd.DataFrame())

@app.route("/projects")
def project_page():
    try:
        df = get_all_projects()
        return render_template("dashboard.html", title="프로젝트 목록", data=df)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="프로젝트 목록", data=pd.DataFrame())

@app.route("/departments")
def department_page():
    try:
        df = get_all_departments()
        return render_template("dashboard.html", title="부서 목록", data=df)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="부서 목록", data=pd.DataFrame())

# 부서, 기술, 프로젝트 유형, 장소 목록 조회 함수
def get_departments():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query("SELECT department_id, name FROM departments", conn)
        return df
    except Exception as e:
        print(f"부서 목록 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_skills():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query("SELECT skill_id, name FROM skills", conn)
        return df
    except Exception as e:
        print(f"기술 목록 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_project_types():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query("SELECT type_id, type_name FROM project_type", conn)
        return df
    except Exception as e:
        print(f"프로젝트 유형 목록 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_available_employees():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query("""
            SELECT e.employee_id, e.name, e.position, d.name AS department
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.department_id
            ORDER BY e.name
        """, conn)
        return df
    except Exception as e:
        print(f"사용 가능한 사원 목록 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_available_projects():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query("""
            SELECT p.project_id, p.name, pt.type_name AS type
            FROM projects p
            LEFT JOIN project_type pt ON p.type_id = pt.type_id
            ORDER BY p.name
        """, conn)
        return df
    except Exception as e:
        print(f"사용 가능한 프로젝트 목록 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# --- 부서 등록 페이지 ---
@app.route("/departments/add", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        print(f"부서 등록 시도: '{name}'")  # 디버깅용

        # 데이터 검증
        if not name:
            flash("부서명은 필수 입력 항목입니다.", "danger")
            return render_template("department_add.html")

        conn = get_connection()
        if conn is None:
            flash("데이터베이스 연결에 실패했습니다.", "danger")
            return render_template("department_add.html")

        try:
            cur = conn.cursor()
            print(f"데이터베이스에 부서 '{name}' 삽입 시도")  # 디버깅용
            cur.execute("INSERT INTO departments (name) VALUES (?)", (name,))
            conn.commit()
            print(f"부서 '{name}' 등록 성공")  # 디버깅용
            flash(f"부서 '{name}' 등록 성공", "success")
            return redirect(url_for("department_page"))
        except sqlite3.IntegrityError as e:
            print(f"부서 등록 중 무결성 오류: {e}")  # 디버깅용
            flash(f"중복된 부서명입니다: {str(e)}", "danger")
        except Exception as e:
            print(f"부서 등록 중 일반 오류: {e}")  # 디버깅용
            flash(f"부서 등록 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    # GET 요청: 폼 렌더링
    print("부서 등록 페이지 GET 요청")  # 디버깅용
    return render_template("department_add.html")

# --- 사원 등록 페이지 ---
@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        position = request.form.get("position", "").strip()
        department_id = request.form.get("department_id")
        skills = request.form.get("skills", "").strip()

        # 데이터 검증
        if not name:
            flash("이름은 필수 입력 항목입니다.", "danger")
            departments = get_departments()
            return render_template("employee_add.html", departments=departments)

        if not department_id:
            flash("부서는 필수 선택 항목입니다.", "danger")
            departments = get_departments()
            return render_template("employee_add.html", departments=departments)

        conn = get_connection()
        if conn is None:
            flash("데이터베이스 연결에 실패했습니다.", "danger")
            departments = get_departments()
            return render_template("employee_add.html", departments=departments)

        try:
            cur = conn.cursor()
            # 사원 테이블에 insert (skills 필드 포함)
            cur.execute(
                "INSERT INTO employees (name, position, department_id, skills) VALUES (?, ?, ?, ?)",
                (name, position, department_id, skills)
            )
            conn.commit()
            flash(f"사원 '{name}' 등록 성공", "success")
            return redirect(url_for("employee_page"))
        except sqlite3.IntegrityError as e:
            flash(f"중복된 데이터가 있습니다: {str(e)}", "danger")
        except Exception as e:
            flash(f"사원 등록 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    # GET 요청: 부서 목록 받아서 폼 렌더링
    departments = get_departments()
    return render_template("employee_add.html", departments=departments)

# --- 프로젝트 등록 페이지 ---
@app.route("/projects/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        type_id = request.form.get("type_id")
        location = request.form.get("location", "").strip()
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # 데이터 검증
        if not name:
            flash("프로젝트명은 필수 입력 항목입니다.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        if not type_id:
            flash("프로젝트 유형은 필수 선택 항목입니다.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        if not location:
            flash("장소는 필수 입력 항목입니다.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        if not start_date or not end_date:
            flash("시작일과 종료일은 필수 입력 항목입니다.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        # 날짜 검증
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if start_dt >= end_dt:
                flash("종료일은 시작일보다 늦어야 합니다.", "danger")
                project_types = get_project_types()
                return render_template("project_add.html", project_types=project_types)
        except ValueError:
            flash("올바른 날짜 형식을 입력해주세요.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        conn = get_connection()
        if conn is None:
            flash("데이터베이스 연결에 실패했습니다.", "danger")
            project_types = get_project_types()
            return render_template("project_add.html", project_types=project_types)

        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO projects (name, type_id, location, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
                (name, type_id, location, start_date, end_date)
            )
            conn.commit()
            flash(f"프로젝트 '{name}' 등록 성공", "success")
            return redirect(url_for("project_page"))
        except sqlite3.IntegrityError as e:
            flash(f"중복된 데이터가 있습니다: {str(e)}", "danger")
        except Exception as e:
            flash(f"프로젝트 등록 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    # GET 요청: 프로젝트 유형 목록 받아서 폼 렌더링
    project_types = get_project_types()
    return render_template("project_add.html", project_types=project_types)

# --- 프로젝트 배정 페이지 ---
@app.route("/assignment/add", methods=["GET", "POST"])
def add_assignment():
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        project_id = request.form.get("project_id")

        # 데이터 검증
        if not employee_id or not project_id:
            flash("사원과 프로젝트는 필수 선택 항목입니다.", "danger")
            employees = get_available_employees()
            projects = get_available_projects()
            return render_template("assignment_add.html", employees=employees, projects=projects)

        conn = get_connection()
        if conn is None:
            flash("데이터베이스 연결에 실패했습니다.", "danger")
            employees = get_available_employees()
            projects = get_available_projects()
            return render_template("assignment_add.html", employees=employees, projects=projects)

        try:
            cur = conn.cursor()
            # 중복 배정 확인
            cur.execute(
                "SELECT COUNT(*) FROM assignment WHERE employee_id = ? AND project_id = ?",
                (employee_id, project_id)
            )
            if cur.fetchone()[0] > 0:
                flash("이미 배정된 사원-프로젝트 조합입니다.", "danger")
                employees = get_available_employees()
                projects = get_available_projects()
                return render_template("assignment_add.html", employees=employees, projects=projects)

            cur.execute(
                "INSERT INTO assignment (employee_id, project_id) VALUES (?, ?)",
                (employee_id, project_id)
            )
            conn.commit()
            flash("프로젝트 배정 성공", "success")
            return redirect(url_for("assignment"))
        except sqlite3.IntegrityError as e:
            flash(f"데이터 무결성 오류: {str(e)}", "danger")
        except Exception as e:
            flash(f"프로젝트 배정 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    # GET 요청: 사원, 프로젝트 목록 받아서 폼 렌더링
    employees = get_available_employees()
    projects = get_available_projects()
    return render_template("assignment_add.html", employees=employees, projects=projects)

if __name__ == "__main__":
    app.run(debug=True)
