import streamlit as st
import pandas as pd

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "인천ID.xlsx"  # 엑셀 파일이 있는 경로
    xls = pd.ExcelFile(file_path)
    id_list_df = pd.read_excel(xls, sheet_name="ID목록")
    grade_df = pd.read_excel(xls, sheet_name="운전자별 등급현황")
    return id_list_df, grade_df


id_list_df, grade_df = load_data()

# 등급별 색상 매핑
def get_grade_color(grade):
    if grade in ["S", "A"]:
        return "green"
    elif grade in ["B", "C"]:
        return "blue"
    elif grade in ["D", "F"]:
        return "red"
    return "gray"

# 최신 등급 및 등급 히스토리 데이터 추출 함수
def get_grade_history(driver_name, company):
    driver_data = grade_df[(grade_df["운수사"] == company) & (grade_df["운전자이름"] == driver_name)]
    if driver_data.empty:
        return "등급 정보 없음", "gray", pd.DataFrame()
    
    # 월별 등급 데이터 추출
    grade_cols = [col for col in grade_df.columns if "월" in col]
    grade_history = []
    latest_month = None
    latest_grade = None
    
    for col in reversed(grade_cols):  # 최신 데이터부터 확인
        if col in driver_data.columns and pd.notna(driver_data[col].values[0]):
            grade_value = driver_data[col].values[0]
            grade_history.append({"년월": f"{col[:2]}년 {col[2:-1]}월", "등급": f"{grade_value}등급"})
            if latest_month is None:
                latest_month = col
                latest_grade = grade_value
    
    if latest_month is None or latest_grade is None:
        return "등급 정보 없음", "gray", pd.DataFrame()
    
    grade_color = get_grade_color(latest_grade)
    grade_df_display = pd.DataFrame(grade_history)
    return f"최근 등급: {latest_month[:2]}년 {latest_month[2:-1]}월 <b style='color:{grade_color};'>{latest_grade}등급</b>", grade_color, grade_df_display

# Streamlit UI 구성
st.title("운전자 ID 및 등급 조회 시스템")
st.write("운수사와 운전자 이름을 입력하여 ID 및 최근 등급을 조회하세요.")

# 운수사 선택 필터
company_list = id_list_df["운수사"].unique().tolist()
company = st.selectbox("운수사 선택", [""] + company_list)

# 운전자 이름 검색 필드
if company:
    driver_list = id_list_df[id_list_df["운수사"] == company]["운전자이름"].unique().tolist()
    name = st.text_input("운전자 이름 입력")
else:
    name = ""

# ID 및 등급 조회
if st.button("검색"):
    if company and name:
        driver_info = id_list_df[(id_list_df["운수사"] == company) & (id_list_df["운전자이름"] == name)]
        
        if not driver_info.empty:
            # 실제 열 이름 확인 후 사용
            column_name = "운전자ID" if "운전자ID" in id_list_df.columns else id_list_df.columns[2]
            driver_id = driver_info[column_name].values[0]
            retire_status = driver_info["퇴사여부"].values[0] if "퇴사여부" in id_list_df.columns else ""
            
            if pd.notna(retire_status) and retire_status == "퇴사자":
                driver_id = f"{driver_id} (퇴사자)"
            
            latest_grade, grade_color, grade_history_df = get_grade_history(name, company)
            
            st.success(f"운전자 ID: {driver_id}")
            st.markdown(f"<div style='font-size:18px;'> {latest_grade} </div>", unsafe_allow_html=True)
            
            # 등급 히스토리 표시
            if not grade_history_df.empty:
                st.markdown("### <📝월별 등급 현황>")
                st.dataframe(grade_history_df, hide_index=True)
        else:
            st.error("검색 결과가 없습니다.")
    else:
        st.warning("운수사를 선택하고 운전자 이름을 입력해주세요.")


