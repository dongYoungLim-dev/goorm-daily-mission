# =============================================================================
# 유튜브 썸네일 추출기 - 구현 순서 (가장 먼저 할 것부터)
# =============================================================================
#
# [1] 썸네일 URL 규칙 파악 (가장 먼저 할 것)
#     - YouTube 썸네일 주소 형식: https://img.youtube.com/vi/{video_id}/이미지파일명.jpg
#     - 이미지파일명 예: maxresdefault(최고해상도), hqdefault, sddefault, default 등
#     - 따라서 "video_id"만 구하면 썸네일 URL을 만들 수 있음
#
# [2] video_id 추출 방법 정하기
#     - 일반 링크: https://www.youtube.com/watch?v=VIDEO_ID  → v= 뒤 11자리
#     - 짧은 링크: https://youtu.be/VIDEO_ID                 → 경로의 11자리
#     - 정규식(re)으로 위 두 패턴에서 video_id를 추출하는 함수 작성
#
# [3] 필요한 라이브러리
#     - streamlit: URL 입력(st.text_input), 이미지 표시(st.image)
#     - re: URL 문자열에서 video_id 추출
#
# [4] 구현 순서 요약
#     ① re, streamlit import
#     ② URL에서 video_id 추출하는 함수 작성 (정규식 사용)
#     ③ video_id로 썸네일 URL 문자열 조합 (예: f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")
#     ④ st.text_input으로 YouTube URL 입력받기
#     ⑤ 입력된 URL로 video_id 추출 → 썸네일 URL 생성 → st.image()로 표시
# =============================================================================

# ① re, streamlit import
# re: URL 문자열에서 video_id를 추출하기 위해 정규식 검색에 사용
# streamlit: 웹 UI(입력창, 이미지 표시)를 만들기 위해 사용
import re
import streamlit as st


# ② URL에서 video_id 추출하는 함수 (정규식 사용)
# 왜 사용: 썸네일 URL을 만들려면 반드시 11자리 video_id가 필요하므로, 다양한 YouTube URL 형식에서 이를 뽑기 위함
def extract_video_id(url: str) -> str | None:
    """
    YouTube URL에서 video_id(11자리)를 추출합니다.
    지원 형식: watch?v=, youtu.be/, embed/
    """
    if not url or not url.strip():
        return None
    # watch?v=VIDEO_ID 형태: v= 뒤 11자리(영숫자, -, _)
    m = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    # youtu.be/VIDEO_ID 형태
    m = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    # youtube.com/embed/VIDEO_ID 형태
    m = re.search(r"youtube\.com/embed/([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    return None


# ③ video_id로 썸네일 URL 문자열 조합
# 왜 사용: YouTube가 공개적으로 제공하는 썸네일 주소 규칙에 맞춰 이미지 URL을 만듦
# quality: maxresdefault(최고해상도), hqdefault, sddefault, default 등 선택 가능
def get_thumbnail_url(video_id: str, quality: str = "hqdefault") -> str:
    return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"


# -----------------------------------------------------------------------------
# Streamlit 앱: 페이지 설정 및 제목
# -----------------------------------------------------------------------------
# set_page_config: 브라우저 탭 제목과 레이아웃 설정. 썸네일만 보여주므로 centered 사용
st.set_page_config(page_title="유튜브 썸네일 추출기", layout="centered")
st.title("유튜브 썸네일 추출기")
st.caption("YouTube 영상 URL을 입력하면 해당 영상의 썸네일 이미지를 표시합니다.")

# ④ st.text_input으로 YouTube URL 입력받기
# 왜 사용: 사용자가 썸네일을 볼 영상의 주소를 입력할 수 있게 하기 위함
url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=... 또는 https://youtu.be/...",
    value="",
)

# 해상도 선택: maxresdefault는 없는 영상이 있을 수 있어 hqdefault 등을 선택할 수 있게 함
quality = st.selectbox(
    "썸네일 해상도",
    options=["maxresdefault", "hqdefault", "sddefault", "mqdefault", "default"],
    index=1,
    help="maxresdefault가 없으면 hqdefault 등으로 바꿔 보세요.",
)

# ⑤ 입력된 URL로 video_id 추출 → 썸네일 URL 생성 → st.image()로 표시
# 어떤 기능: URL이 입력된 경우에만 추출·표시를 시도하고, 실패 시 에러 메시지를 띄움
if url:
    video_id = extract_video_id(url)
    if video_id:
        # 썸네일 URL 생성 후 st.image로 이미지 표시
        # st.image: URL 또는 이미지 데이터를 화면에 그려 줌
        thumbnail_url = get_thumbnail_url(video_id, quality)
        st.image(thumbnail_url, caption=f"Video ID: {video_id} ({quality})")
    else:
        # video_id 추출 실패 시: 잘못된 URL 형식 안내
        st.error("올바른 YouTube URL을 입력해 주세요. (예: youtube.com/watch?v=VIDEO_ID 또는 youtu.be/VIDEO_ID)")
else:
    st.info("위 입력란에 YouTube 영상 URL을 입력해 주세요.")
