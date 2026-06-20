import streamlit as st
import random
import time

# 1. 페이지 설정 및 오리지널 감성 CSS 스타일링
st.set_page_config(page_title="한컴타자: 자원캐기 Web", page_icon="⛏️", layout="wide")

st.markdown("""
    <style>
    /* 클래식한 광산 느낌의 배경색 */
    .stApp {
        background-color: #d7c4a9;
        color: #333333;
        font-family: 'Malgun Gothic', sans-serif;
    }
    /* 메인 광산 필드 */
    .mine-field {
        background-color: #a68b7c;
        border: 5px solid #6e5547;
        border-radius: 10px;
        min-height: 420px;
        position: relative;
        padding: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.4);
    }
    /* 광산 내부에서 무작위로 배치되는 자원 스타일 */
    .resource-item {
        display: inline-block;
        background: rgba(255, 255, 255, 0.85);
        border: 2px solid #cd7f32;
        border-radius: 5px;
        padding: 5px 10px;
        margin: 8px;
        font-weight: bold;
        font-size: 18px;
        color: #2b1d11;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    /* 우측 대시보드 및 설정 패널 스타일 */
    .sidebar-panel {
        background-color: #eedcc5;
        border: 3px solid #b59d83;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .score-txt {
        font-size: 24px;
        font-weight: bold;
        color: #b85a00;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 게임에 사용할 한국어 단어 풀 (이미지 원본 단어 대거 포함)
WORD_POOL = [
    "마음씨", "괄목", "치후", "아름", "밀기울", "안채", "날씨", "바라지", "도막말",
    "옹고집", "나부굴다", "나이", "까닥이다", "끼릉하다", "제법", "가풀막", "바글비율",
    "벼랑길", "살갗", "오목하다", "구르다", "바로잡다", "스르르", "때문", "달구다", "때때로",
    "말굽", "동니다", "니오다", "하품", "포중", "치증기", "동조", "나래", "보습", "무디다",
    "술래잡기", "중고봉긋", "활짝", "무디다", "두디다", "첫줄", "가기"
]

# 3. 선택 가능한 캐릭터 이모지 목록
CHARACTERS = {
    "열정 광부 👦": "👦",
    "탐험가 리사 👧": "👧",
    "우주 광부 🧑‍🚀": "🧑‍🚀",
    "로봇 굴착기 🤖": "🤖",
    "판다 광부 🐼": "🐼"
}

# 4. 세션 상태(Session State) 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "selected_char" not in st.session_state:
    st.session_state.selected_char = "열정 광부 👦"
if "active_words" not in st.session_state:
    st.session_state.active_words = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "last_spawn_time" not in st.session_state:
    st.session_state.last_spawn_time = 0

# 5. 단어 타이핑 정답 확인 함수
def check_typing():
    user_word = st.session_state.typing_input.strip()
    if user_word in st.session_state.active_words:
        st.session_state.active_words.remove(user_word)
        st.session_state.score += 10
        
        # 채굴 성공 시 즉시 새로운 단어 하나 공급해 흐름 유지
        available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
        if available_words:
            st.session_state.active_words.append(random.choice(available_words))
    st.session_state.typing_input = ""  # 입력창 초기화

# 6. 메인 타이틀
st.title("⛏️ 한컴타자: 자원캐기 (Web Edition)")

# --- [대기 화면] 게임이 시작되지 않았을 때 설정창 표시 ---
if not st.session_state.game_started:
    st.markdown("### 🎒 광산에 들어가기 전 준비")
    
    col_setup1, col_setup2 = st.columns([2, 1])
    
    with col_setup1:
        st.info("원하는 광부 캐릭터를 선택하고 아래 '광산 진입 (게임 시작)' 버튼을 누르세요!")
        # 캐릭터 선택 라디오 버튼
        st.session_state.selected_char = st.radio(
            "플레이할 캐릭터를 선택하세요:",
            options=list(CHARACTERS.keys()),
            horizontal=True
        )
        
        # 거대한 시작 버튼
        if st.button("🚀 광산 진입 (게임 시작)", type="primary", use_container_width=True):
            st.session_state.game_started = True
            # 시작할 때 기본 단어 6개 배치
            st.session_state.active_words = random.sample(WORD_POOL, 6)
            st.session_state.last_spawn_time = time.time()
            st.rerun()
            
    with col_setup2:
        # 선택한 캐릭터 미리보기용 카드 UI
        chosen_emoji = CHARACTERS[st.session_state.selected_char]
        st.markdown(f"""
        <div class="sidebar-panel" style="padding: 30px;">
            <div style="font-size: 80px; margin-bottom: 10px;">{chosen_emoji}</div>
            <h3>{st.session_state.selected_char}</h3>
            <p style="color: #666;">준비 완료!</p>
        </div>
        """, unsafe_allow_html=True)

# --- [게임 화면] 게임이 진행 중일 때 레이아웃 구성 ---
else:
    # 시간 흐름에 따른 새로운 자원(단어) 자동 생성 로직 (3초마다 1개씩 추가)
    current_time = time.time()
    if current_time - st.session_state.last_spawn_time > 3.0:
        if len(st.session_state.active_words) < 25:  # 화면 최대 단어 수 제한
            available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
            if available_words:
                st.session_state.active_words.append(random.choice(available_words))
        st.session_state.last_spawn_time = current_time

    col_left, col_right = st.columns([3, 1])

    # 좌측 영역: 실제 광산 필드 (단어들이 나타나는 곳)
    with col_left:
        st.markdown("### ⛰️ 광산 필드")
        
        # 현재 화면의 단어들을 광물 조각 형태로 뿌려줌
        word_html = "".join([f'<div class="resource-item">💎 {word}</div>' for word in st.session_state.active_words])
        st.markdown(f'<div class="mine-field">{word_html}</div>', unsafe_allow_html=True)
        
        st.write("")
        # 유저 입력창
        st.text_input(
            "광물을 캐기 위해 단어를 입력하세요:",
            key="typing_input",
            on_change=check_typing,
            placeholder="화면에 보이는 단어를 입력하고 Enter!",
            label_visibility="collapsed"
        )

    # 우측 영역: 선택한 캐릭터 정보 및 스코어보드 (사진 속 UI 모방)
    with col_right:
        st.markdown('### 👤 유저 정보')
        chosen_emoji = CHARACTERS[st.session_state.selected_char]
        
        st.markdown(f"""
        <div class="sidebar-panel">
            <div style="font-size: 60px;">{chosen_emoji}</div>
            <p><b>User: JooandKyu</b></p>
            <p style="color: #666; font-size: 13px;">({st.session_state.selected_char})</p>
            <hr style="margin: 10px 0; border-color: #b59d83;">
            <p style="font-size: 18px; font-weight: bold;">제 10 단계</p>
            <div class="score-txt">현재 점수: {st.session_state.score} 점</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        # 게임 종료 및 리셋 버튼
        if st.button("⏹️ 게임 종료 (대기실로)", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.score = 0
            st.session_state.active_words = []
            st.rerun()

    # 실시간 단어 리프레시를 유도하기 위한 루프 트리거 (가만히 있어도 2초마다 갱신)
    time.sleep(2.0)
    st.rerun()
