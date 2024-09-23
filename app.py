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
    """Google Drive 링크에서 파일 ID 추출"""
    try:
        if 'drive.google.com' in drive_url and '/d/' in drive_url:
            return drive_url.split('/d/')[1].split('/')[0]
        else:
            st.error("Invalid Google Drive link. Make sure the link is in the correct format.")
            return None
    except IndexError:
        st.error("Error extracting file ID from the Google Drive link.")
        return None

def generate_download_link(file_id):
    """Google Drive 파일 ID로 다운로드 링크 생성"""
    return f"https://drive.google.com/uc?id={file_id}&export=download"

def download_drive_file(file_id):
    """Google Drive에서 파일을 다운로드하는 함수"""
    download_url = generate_download_link(file_id)
    response = requests.get(download_url, stream=True)
    
    if response.status_code == 200:
        file_size = int(response.headers.get('Content-Length', 0))
        if file_size == 0:
            st.error("The downloaded file is empty. Please check the Google Drive link or file permissions.")
            return None
        st.write(f"File size: {file_size / (1024 * 1024):.2f} MB")
        
        # 임시 파일 생성
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp4")
        with temp_file as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        st.write(f"Video saved to temporary file: {temp_file.name}")
        return temp_file.name
    else:
        st.error(f"Failed to download file: {response.status_code}")
        return None

if drive_url:
    file_id = get_drive_file_id(drive_url)
    
    if file_id:
        st.write(f"File ID extracted: {file_id}")
        
        # 비디오 파일 다운로드
        video_path = download_drive_file(file_id)
        
        if video_path:
            # OpenCV를 사용하여 비디오 읽기
            st.write(f"Opening video: {video_path}")
            cap = cv2.VideoCapture(video_path)
            
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
                st.error(f"Failed to open video file: {video_path}")
            cap.release()
        else:
            st.error("Failed to download the video file.")
    else:
        st.error("Invalid Google Drive link.")