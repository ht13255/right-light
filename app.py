import streamlit as st
import os
from player_analysis import main  # player_analysis.py에 구현된 분석 코드

# Streamlit 페이지 설정
st.title("Player Analysis Application")

# 사용자 입력 섹션
player_id = st.text_input("Enter Player ID")
player_name = st.text_input("Enter Player Name")
player_number = st.text_input("Enter Player Number")

# 비디오 파일 업로드
uploaded_video = st.file_uploader("Upload Match Video", type=["mp4"])

# 분석 시작 버튼
if st.button("Start Analysis") and uploaded_video is not None:
    # 비디오 파일 저장
    video_path = os.path.join("uploads", uploaded_video.name)
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    
    # 분석 시작
    st.write("Running analysis...")
    main(player_id, player_name, video_path, int(player_number))
    
    # 분석 완료 후 메시지
    st.success(f"Analysis for {player_name} completed! Download the PDF report.")
    
    # 분석된 결과 파일 링크 (PDF 보고서 다운로드)
    pdf_filename = f"{player_name}_stat_report.pdf"
    st.download_button("Download PDF Report", open(pdf_filename, "rb"), file_name=pdf_filename)
