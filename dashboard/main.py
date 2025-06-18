# dashboard/main.py
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from query import (
    get_all_summary,
    get_maintenance_projects,
    get_ongoing_projects,
    get_project_assignment_list
)

st.set_page_config(page_title="프로젝트 인원 대시보드", layout="wide")

st.title("📊 프로젝트 인원 대시보드")

tab1, tab2, tab3, tab4 = st.tabs([
    "전체 요약",
    "유지보수 프로젝트",
    "진행 중인 프로젝트",
    "프로젝트별 인원"
])

with tab1:
    st.subheader("전체 프로젝트 참여 현황")
    df = get_all_summary()
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("🛠 유지보수 프로젝트")
    df = get_maintenance_projects()
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("⏳ 현재 진행 중인 프로젝트")
    df = get_ongoing_projects()
    st.dataframe(df, use_container_width=True)

with tab4:
    st.subheader("👥 프로젝트별 인원 및 기술")
    df = get_project_assignment_list()
    st.dataframe(df, use_container_width=True)
