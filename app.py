import streamlit as st
import pandas as pd

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "인천ID.xlsx"  # 엑셀 파일이 있는 경로
    df = pd.read_excel(file_path)
    return df

df = load_data()

# Streamlit UI 구성
st.title("운전자 ID 조회 시스템")
st.write("운수사와 운전자 이름을 입력하여 ID를 조회하세요.")

# 운수사 선택
company_list = df["운수사"].unique().tolist()
company = st.selectbox("운수사 선택", [""] + company_list)

# 운전자 이름 입력
if company:
    driver_list = df[df["운수사"] == company]["운전자이름"].unique().tolist()
    name = st.selectbox("운전자 이름 선택", [""] + driver_list)
else:
    name = ""

# ID 검색
if st.button("검색"):
    if company and name:
        driver_id = df[(df["운수사"] == company) & (df["운전자이름"] == name)]["운전자ID"]
        if not driver_id.empty:
            st.success(f"운전자 ID: {driver_id.values[0]}")
        else:
            st.error("검색 결과가 없습니다.")
    else:
        st.warning("운수사와 운전자 이름을 선택해주세요.")

