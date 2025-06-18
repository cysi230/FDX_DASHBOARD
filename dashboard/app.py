from flask import Flask, render_template
import sys
import os
from query import get_all_employees, get_all_projects, get_all_departments  # 상단에 추가
from flask import request, redirect, url_for, flash
import sqlite3
import pandas as pd
from datetime import datetime
import io
from flask import send_file

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from query import (
    get_all_summary,
    get_maintenance_projects_grouped,
    get_ongoing_projects_grouped,
    get_project_assignment_grouped,
    get_all_employees,
    get_all_projects,
    get_all_departments,
    get_project_assignment_detail,
    get_project_info,
    get_assignment_info
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
        return render_template("dashboard.html", title="전체 프로젝트 요약", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="전체 프로젝트 요약", data=pd.DataFrame())

@app.route("/maintenance")
def maintenance():
    try:
        data = get_maintenance_projects_grouped()
        return render_template("dashboard.html", title="유지보수 프로젝트", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="유지보수 프로젝트", data=pd.DataFrame())

@app.route("/ongoing")
def ongoing():
    try:
        data = get_ongoing_projects_grouped()
        return render_template("dashboard.html", title="진행 중인 프로젝트", data=data)
    except Exception as e:
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}", "danger")
        return render_template("dashboard.html", title="진행 중인 프로젝트", data=pd.DataFrame())

@app.route("/assignment")
def assignment():
    try:
        data = get_project_assignment_grouped()
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
            print(f"부서 등록 중 중복 오류: {e}")  # 디버깅용
            flash("이미 존재하는 부서명입니다.", "danger")
        except Exception as e:
            print(f"부서 등록 중 오류: {e}")  # 디버깅용
            flash(f"부서 등록 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    return render_template("department_add.html")

# --- 부서 수정 페이지 ---
@app.route("/departments/<int:department_id>/edit", methods=["GET", "POST"])
def edit_department(department_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("department_page"))

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            
            if not name:
                flash("부서명은 필수 입력 항목입니다.", "danger")
                return render_template("department_edit.html", department={"department_id": department_id, "name": name})

            cur = conn.cursor()
            cur.execute("UPDATE departments SET name = ? WHERE department_id = ?", (name, department_id))
            conn.commit()
            flash(f"부서 '{name}' 수정 성공", "success")
            return redirect(url_for("department_page"))
        else:
            cur = conn.cursor()
            cur.execute("SELECT department_id, name FROM departments WHERE department_id = ?", (department_id,))
            department = cur.fetchone()
            
            if department is None:
                flash("부서를 찾을 수 없습니다.", "danger")
                return redirect(url_for("department_page"))
            
            return render_template("department_edit.html", department=dict(department))
    except Exception as e:
        flash(f"부서 수정 중 오류가 발생했습니다: {str(e)}", "danger")
        return redirect(url_for("department_page"))
    finally:
        conn.close()

# --- 부서 삭제 ---
@app.route("/departments/<int:department_id>/delete")
def delete_department(department_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("department_page"))

    try:
        cur = conn.cursor()
        
        # 부서명 조회
        cur.execute("SELECT name FROM departments WHERE department_id = ?", (department_id,))
        department = cur.fetchone()
        
        if department is None:
            flash("부서를 찾을 수 없습니다.", "danger")
            return redirect(url_for("department_page"))
        
        # 해당 부서에 속한 사원이 있는지 확인
        cur.execute("SELECT COUNT(*) FROM employees WHERE department_id = ?", (department_id,))
        employee_count = cur.fetchone()[0]
        
        if employee_count > 0:
            flash(f"'{department[0]}' 부서에 속한 사원이 {employee_count}명 있어 삭제할 수 없습니다.", "danger")
            return redirect(url_for("department_page"))
        
        # 부서 삭제
        cur.execute("DELETE FROM departments WHERE department_id = ?", (department_id,))
        conn.commit()
        flash(f"부서 '{department[0]}' 삭제 성공", "success")
        
    except Exception as e:
        flash(f"부서 삭제 중 오류가 발생했습니다: {str(e)}", "danger")
    finally:
        conn.close()
    
    return redirect(url_for("department_page"))

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

# --- 사원 수정 페이지 ---
@app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("employee_page"))

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            position = request.form.get("position", "").strip()
            department_id = request.form.get("department_id")
            skills = request.form.get("skills", "").strip()
            
            if not name:
                flash("이름은 필수 입력 항목입니다.", "danger")
                departments = get_departments()
                return render_template("employee_edit.html", 
                                     employee={"employee_id": employee_id, "name": name, "position": position, "department_id": department_id, "skills": skills}, 
                                     departments=departments)

            if not department_id:
                flash("부서는 필수 선택 항목입니다.", "danger")
                departments = get_departments()
                return render_template("employee_edit.html", 
                                     employee={"employee_id": employee_id, "name": name, "position": position, "department_id": department_id, "skills": skills}, 
                                     departments=departments)

            cur = conn.cursor()
            cur.execute("UPDATE employees SET name = ?, position = ?, department_id = ?, skills = ? WHERE employee_id = ?", 
                       (name, position, department_id, skills, employee_id))
            conn.commit()
            flash(f"사원 '{name}' 수정 성공", "success")
            return redirect(url_for("employee_page"))
        else:
            cur = conn.cursor()
            cur.execute("SELECT employee_id, name, position, department_id, skills FROM employees WHERE employee_id = ?", (employee_id,))
            employee = cur.fetchone()
            
            if employee is None:
                flash("사원을 찾을 수 없습니다.", "danger")
                return redirect(url_for("employee_page"))
            
            departments = get_departments()
            return render_template("employee_edit.html", employee=dict(employee), departments=departments)
    except Exception as e:
        flash(f"사원 수정 중 오류가 발생했습니다: {str(e)}", "danger")
        return redirect(url_for("employee_page"))
    finally:
        conn.close()

# --- 사원 삭제 ---
@app.route("/employees/<int:employee_id>/delete")
def delete_employee(employee_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("employee_page"))

    try:
        cur = conn.cursor()
        
        # 사원명 조회
        cur.execute("SELECT name FROM employees WHERE employee_id = ?", (employee_id,))
        employee = cur.fetchone()
        
        if employee is None:
            flash("사원을 찾을 수 없습니다.", "danger")
            return redirect(url_for("employee_page"))
        
        # 해당 사원이 프로젝트에 배정되어 있는지 확인
        cur.execute("SELECT COUNT(*) FROM assignment WHERE employee_id = ?", (employee_id,))
        assignment_count = cur.fetchone()[0]
        
        if assignment_count > 0:
            flash(f"'{employee[0]}' 사원이 {assignment_count}개의 프로젝트에 배정되어 있어 삭제할 수 없습니다.", "danger")
            return redirect(url_for("employee_page"))
        
        # 사원 삭제
        cur.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        conn.commit()
        flash(f"사원 '{employee[0]}' 삭제 성공", "success")
        
    except Exception as e:
        flash(f"사원 삭제 중 오류가 발생했습니다: {str(e)}", "danger")
    finally:
        conn.close()
    
    return redirect(url_for("employee_page"))

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

# --- 프로젝트 수정 페이지 ---
@app.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("project_page"))

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            type_name = request.form.get("type", "").strip()
            location = request.form.get("location", "").strip()
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            status = request.form.get("status", "").strip()
            
            if not name:
                flash("프로젝트명은 필수 입력 항목입니다.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})

            if not type_name:
                flash("프로젝트 유형은 필수 선택 항목입니다.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})

            if not location:
                flash("장소는 필수 입력 항목입니다.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})

            if not start_date or not end_date:
                flash("시작일과 종료일은 필수 입력 항목입니다.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})

            # 날짜 검증
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                if start_dt >= end_dt:
                    flash("종료일은 시작일보다 늦어야 합니다.", "danger")
                    return render_template("project_edit.html", 
                                         project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})
            except ValueError:
                flash("올바른 날짜 형식을 입력해주세요.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})

            # 유형 ID 조회
            cur = conn.cursor()
            cur.execute("SELECT type_id FROM project_type WHERE type_name = ?", (type_name,))
            type_result = cur.fetchone()
            
            if type_result is None:
                flash("유효하지 않은 프로젝트 유형입니다.", "danger")
                return render_template("project_edit.html", 
                                     project={"project_id": project_id, "name": name, "type": type_name, "location": location, "start_date": start_date, "end_date": end_date, "status": status})
            
            type_id = type_result[0]
            
            # 프로젝트 업데이트
            cur.execute("UPDATE projects SET name = ?, type_id = ?, location = ?, start_date = ?, end_date = ?, status = ? WHERE project_id = ?", 
                       (name, type_id, location, start_date, end_date, status, project_id))
            conn.commit()
            flash(f"프로젝트 '{name}' 수정 성공", "success")
            return redirect(url_for("project_page"))
        else:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.project_id, p.name, pt.type_name as type, p.location, p.start_date, p.end_date, p.status 
                FROM projects p
                LEFT JOIN project_type pt ON p.type_id = pt.type_id
                WHERE p.project_id = ?
            """, (project_id,))
            project = cur.fetchone()
            
            if project is None:
                flash("프로젝트를 찾을 수 없습니다.", "danger")
                return redirect(url_for("project_page"))
            
            return render_template("project_edit.html", project=dict(project))
    except Exception as e:
        flash(f"프로젝트 수정 중 오류가 발생했습니다: {str(e)}", "danger")
        return redirect(url_for("project_page"))
    finally:
        conn.close()

# --- 프로젝트 삭제 ---
@app.route("/projects/<int:project_id>/delete")
def delete_project(project_id):
    conn = get_connection()
    if conn is None:
        flash("데이터베이스 연결에 실패했습니다.", "danger")
        return redirect(url_for("project_page"))

    try:
        cur = conn.cursor()
        
        # 프로젝트명 조회
        cur.execute("SELECT name FROM projects WHERE project_id = ?", (project_id,))
        project = cur.fetchone()
        
        if project is None:
            flash("프로젝트를 찾을 수 없습니다.", "danger")
            return redirect(url_for("project_page"))
        
        # 해당 프로젝트에 배정된 사원 수 확인
        cur.execute("SELECT COUNT(*) FROM assignment WHERE project_id = ?", (project_id,))
        assignment_count = cur.fetchone()[0]
        
        # 먼저 해당 프로젝트의 모든 배정 삭제
        if assignment_count > 0:
            cur.execute("DELETE FROM assignment WHERE project_id = ?", (project_id,))
        
        # 프로젝트 삭제
        cur.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
        conn.commit()
        
        if assignment_count > 0:
            flash(f"프로젝트 '{project[0]}'과 {assignment_count}명의 사원 배정이 삭제되었습니다.", "success")
        else:
            flash(f"프로젝트 '{project[0]}' 삭제 성공", "success")
        
    except Exception as e:
        flash(f"프로젝트 삭제 중 오류가 발생했습니다: {str(e)}", "danger")
    finally:
        conn.close()
    
    # 이전 페이지가 프로젝트별 인원 화면이었다면 assignment 페이지로 리다이렉트
    referer = request.headers.get('Referer', '')
    if 'assignment' in referer:
        return redirect(url_for("assignment"))
    else:
        return redirect(url_for("project_page"))

# --- 프로젝트 배정 페이지 ---
@app.route("/assignment/add", methods=["GET", "POST"])
def add_assignment():
    if request.method == "POST":
        project_id = request.form.get("project_id")
        employee_ids = request.form.getlist("employee_ids")

        # 데이터 검증
        if not project_id:
            flash("프로젝트는 필수 선택 항목입니다.", "danger")
            employees = get_available_employees()
            projects = get_available_projects()
            return render_template("assignment_add_multiple.html", employees=employees, projects=projects)

        if not employee_ids:
            flash("최소 한 명의 사원을 선택해야 합니다.", "danger")
            employees = get_available_employees()
            projects = get_available_projects()
            return render_template("assignment_add_multiple.html", employees=employees, projects=projects)

        conn = get_connection()
        if conn is None:
            flash("데이터베이스 연결에 실패했습니다.", "danger")
            employees = get_available_employees()
            projects = get_available_projects()
            return render_template("assignment_add_multiple.html", employees=employees, projects=projects)

        try:
            cur = conn.cursor()
            success_count = 0
            error_count = 0
            
            for employee_id in employee_ids:
                # 중복 배정 확인
                cur.execute(
                    "SELECT COUNT(*) FROM assignment WHERE employee_id = ? AND project_id = ?",
                    (employee_id, project_id)
                )
                if cur.fetchone()[0] > 0:
                    error_count += 1
                    continue
                
                # 배정 추가
                cur.execute(
                    "INSERT INTO assignment (employee_id, project_id) VALUES (?, ?)",
                    (employee_id, project_id)
                )
                success_count += 1
            
            conn.commit()
            
            if success_count > 0:
                flash(f"{success_count}명의 사원 배정 성공", "success")
            if error_count > 0:
                flash(f"{error_count}명의 사원은 이미 배정되어 있습니다.", "warning")
            
            return redirect(url_for("assignment"))
            
        except Exception as e:
            flash(f"다중 배정 중 오류가 발생했습니다: {str(e)}", "danger")
        finally:
            conn.close()

    # GET 요청: 사원, 프로젝트 목록 받아서 폼 렌더링
    employees = get_available_employees()
    projects = get_available_projects()
    return render_template("assignment_add_multiple.html", employees=employees, projects=projects)

# --- 프로젝트 배정 수정 페이지 ---
@app.route("/assignment/<int:assignment_id>/edit", methods=["GET", "POST"])
def edit_assignment(assignment_id):
    """개별 배정 수정"""
    try:
        assignment_info = get_assignment_info(assignment_id)
        
        if assignment_info.empty:
            flash('배정 정보를 찾을 수 없습니다.', 'error')
            return redirect(url_for('assignment'))
        
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            role = request.form.get('role')
            
            if not start_date or not end_date:
                flash('시작일과 종료일은 필수입니다.', 'error')
                return render_template('assignment_edit.html', assignment_info=assignment_info)
            
            if start_date > end_date:
                flash('시작일은 종료일보다 이전이어야 합니다.', 'error')
                return render_template('assignment_edit.html', assignment_info=assignment_info)
            
            # 배정 정보 업데이트
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE assignment 
                SET start_date = ?, end_date = ?, role = ?
                WHERE assignment_id = ?
            """, (start_date, end_date, role, assignment_id))
            conn.commit()
            conn.close()
            
            flash('배정 정보가 성공적으로 수정되었습니다.', 'success')
            return redirect(url_for('assignment_detail', project_id=assignment_info.iloc[0]['project_id']))
        
        return render_template('assignment_edit.html', assignment_info=assignment_info)
        
    except Exception as e:
        flash(f'배정 수정 중 오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('assignment'))

# --- 프로젝트 배정 삭제 ---
@app.route("/assignment/<int:assignment_id>/delete")
def delete_assignment(assignment_id):
    """개별 배정 삭제"""
    try:
        # 삭제 전에 프로젝트 ID를 가져옴
        assignment_info = get_assignment_info(assignment_id)
        
        if assignment_info.empty:
            flash('배정 정보를 찾을 수 없습니다.', 'error')
            return redirect(url_for('assignment'))
        
        project_id = assignment_info.iloc[0]['project_id']
        employee_name = assignment_info.iloc[0]['employee_name']
        
        # 배정 삭제
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assignment WHERE assignment_id = ?", (assignment_id,))
        conn.commit()
        conn.close()
        
        flash(f'사원 {employee_name}의 배정이 삭제되었습니다.', 'success')
        return redirect(url_for('assignment_detail', project_id=project_id))
        
    except Exception as e:
        flash(f'배정 삭제 중 오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('assignment'))

@app.route('/assignment/<int:project_id>/detail')
def assignment_detail(project_id):
    """프로젝트별 배정 상세 화면"""
    try:
        assignments = get_project_assignment_detail(project_id)
        project_info = get_project_info(project_id)
        
        if project_info.empty:
            flash('프로젝트를 찾을 수 없습니다.', 'error')
            return redirect(url_for('assignment'))
            
        return render_template('assignment_detail.html', 
                             assignments=assignments, 
                             project_info=project_info)
    except Exception as e:
        flash(f'데이터 조회 중 오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('assignment'))

@app.route('/assignment/<int:project_id>/add', methods=['GET', 'POST'])
def add_assignment_to_project(project_id):
    """특정 프로젝트에 인원 추가"""
    try:
        project_info = get_project_info(project_id)
        
        if project_info.empty:
            flash('프로젝트를 찾을 수 없습니다.', 'error')
            return redirect(url_for('assignment'))
        
        if request.method == 'POST':
            employee_ids = request.form.getlist('employee_ids')
            
            if not employee_ids:
                flash('최소 한 명의 사원을 선택해야 합니다.', 'error')
                employees = get_available_employees()
                return render_template('assignment_add_to_project.html', 
                                     employees=employees, 
                                     project_info=project_info)
            
            conn = get_connection()
            cursor = conn.cursor()
            success_count = 0
            error_count = 0
            
            for employee_id in employee_ids:
                # 중복 배정 확인
                cursor.execute(
                    "SELECT COUNT(*) FROM assignment WHERE employee_id = ? AND project_id = ?",
                    (employee_id, project_id)
                )
                if cursor.fetchone()[0] > 0:
                    error_count += 1
                    continue
                
                # 배정 추가
                cursor.execute(
                    "INSERT INTO assignment (employee_id, project_id) VALUES (?, ?)",
                    (employee_id, project_id)
                )
                success_count += 1
            
            conn.commit()
            conn.close()
            
            if success_count > 0:
                flash(f'{success_count}명의 사원이 성공적으로 배정되었습니다.', 'success')
            if error_count > 0:
                flash(f'{error_count}명의 사원은 이미 배정되어 있습니다.', 'warning')
            
            return redirect(url_for('assignment_detail', project_id=project_id))
        
        # GET 요청: 사원 목록 받아서 폼 렌더링
        employees = get_available_employees()
        return render_template('assignment_add_to_project.html', 
                             employees=employees, 
                             project_info=project_info)
        
    except Exception as e:
        flash(f'인원 추가 중 오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('assignment_detail', project_id=project_id))

@app.route("/employees/download")
def download_employees():
    try:
        df = get_all_employees()
        if 'employee_id' in df.columns:
            df = df.drop(columns=['employee_id'])
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Employees")
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="employees.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        flash(f"엑셀 다운로드 중 오류: {str(e)}", "danger")
        return redirect(url_for("employee_page"))

@app.route("/employees/upload", methods=["POST"])
def upload_employees():
    file = request.files.get("file")
    if not file or file.filename == '':
        flash("엑셀 파일을 선택해주세요.", "danger")
        return redirect(url_for("employee_page"))
    try:
        df = pd.read_excel(file)
        required_cols = {"name", "position", "department", "skills"}
        if not required_cols.issubset(df.columns):
            flash("엑셀 파일에 필수 컬럼이 없습니다. (name, position, department, skills)", "danger")
            return redirect(url_for("employee_page"))
        conn = get_connection()
        cur = conn.cursor()
        
        # 기존 사원 정보 모두 삭제
        cur.execute("DELETE FROM employees")
        
        for _, row in df.iterrows():
            # 부서명으로 department_id 찾기
            cur.execute("SELECT department_id FROM departments WHERE name = ?", (row["department"],))
            dept = cur.fetchone()
            if dept:
                department_id = dept[0]
            else:
                # 부서가 없으면 새로 추가
                cur.execute("INSERT INTO departments (name) VALUES (?)", (row["department"],))
                department_id = cur.lastrowid
            cur.execute(
                "INSERT INTO employees (name, position, department_id, skills) VALUES (?, ?, ?, ?)",
                (row["name"], row["position"], department_id, row["skills"])
            )
        conn.commit()
        conn.close()
        flash("엑셀 업로드 성공! 기존 사원 정보가 새로운 데이터로 덮어쓰여졌습니다.", "success")
    except Exception as e:
        flash(f"엑셀 업로드 중 오류: {str(e)}", "danger")
    return redirect(url_for("employee_page"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
