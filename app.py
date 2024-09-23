import streamlit as st
import requests
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# Streamlit 앱 제목 설정
st.title("Player Video Analysis from Google Drive")

# Google Drive 공유 링크 입력
drive_url = st.text_input("Enter Google Drive Video Link")

def get_drive_file_id(drive_url):
    """
    Google Drive 링크에서 파일 ID 추출
    """
    if 'drive.google.com' in drive_url:
        return drive_url.split('/d/')[1].split('/')[0]
    return None

def download_drive_file(file_id):
    """
    Google Drive에서 파일을 다운로드하는 함수
    """
    download_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(download_url)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to download file: {response.status_code}")
        return None

if drive_url:
    file_id = get_drive_file_id(drive_url)
    
    if file_id:
        st.write(f"File ID extracted: {file_id}")
        
        # 비디오 파일 다운로드
        file_content = download_drive_file(file_id)
        
        if file_content:
            # 비디오를 임시 파일에 저장
            with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(file_content)
                temp_video_path = temp_file.name
            
            # OpenCV를 사용하여 비디오 읽기
            st.write("Processing video...")
            cap = cv2.VideoCapture(temp_video_path)
            
            if cap.isOpened():
                stframe = st.empty()
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # OpenCV 이미지(BGR)를 Streamlit에서 표시할 수 있는 RGB로 변환
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Streamlit에서 프레임 표시
                    stframe.image(frame, channels="RGB")
            else:
                st.error("Failed to open video file.")
            cap.release()
        else:
            st.error("Failed to download the video file.")
    else:
        st.error("Invalid Google Drive link.")
