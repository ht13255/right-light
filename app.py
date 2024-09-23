import streamlit as st
import requests
from moviepy.editor import VideoFileClip
from tempfile import NamedTemporaryFile
import os

# Streamlit 앱 제목 설정
st.title("구글 드라이브 영상 링크 업로드")

# Google Drive 공유 링크 입력
drive_url = st.text_input("Enter Google Drive Video Link")

def get_drive_file_id(drive_url):
    """Google Drive 링크에서 파일 ID 추출"""
    try:
        if 'drive.google.com' in drive_url:
            if '/file/d/' in drive_url:
                return drive_url.split('/file/d/')[1].split('/')[0]
            elif 'uc?id=' in drive_url:
                return drive_url.split('uc?id=')[1].split('&')[0]
            else:
                st.error("Invalid Google Drive link format.")
                return None
        else:
            st.error("Please provide a valid Google Drive link.")
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

def process_video_with_moviepy(video_path):
    """MoviePy로 비디오 처리"""
    try:
        st.write(f"Processing video: {video_path}")

        # 다운로드된 파일의 크기 확인
        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            st.error(f"Downloaded file is either missing or empty: {video_path}")
            return
        
        # MoviePy로 비디오 파일 열기
        clip = VideoFileClip(video_path)
        
        # 비디오 정보 출력
        st.write(f"Duration: {clip.duration} seconds")
        st.write(f"Resolution: {clip.size[0]}x{clip.size[1]}")
        
        # 비디오 자르기 (10초에서 20초 구간)
        subclip = clip.subclip(10, 20)
        
        # 비디오 미리보기 (10초~20초 구간의 첫 번째 프레임)
        st.image(subclip.get_frame(0), caption="First frame of the 10-20s subclip")
        
        # 자른 비디오 저장
        output_path = "output.mp4"
        subclip.write_videofile(output_path, codec="libx264")
        st.success(f"Processed video saved as {output_path}")
        
    except Exception as e:
        st.error(f"An error occurred while processing the video: {str(e)}")

# Google Drive에서 비디오 다운로드 및 처리
if drive_url:
    file_id = get_drive_file_id(drive_url)
    
    if file_id:
        st.write(f"File ID extracted: {file_id}")
        
        # 비디오 파일 다운로드
        video_path = download_drive_file(file_id)
        
        if video_path:
            # MoviePy로 비디오 처리
            process_video_with_moviepy(video_path)
        else:
            st.error("Failed to download the video file.")
    else:
        st.error("Invalid Google Drive link.")