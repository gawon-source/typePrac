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
        min-height: 400px;
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
    /* 우측 대시보드 스타일 */
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

# 2. 게임에 사용할 한국어 단어 풀 (오리지널 자원캐기 감성 단어)
WORD_POOL = [
    "마음씨", "괄목", "치후", "아름", "밀기울", "안채", "날씨", "바라지", "도막말",
    "옹고집", "나부굴다", "나이", "까닥이다", "끼릉하다", "제법", "가풀막", "바글비율",
    "벼랑길", "살갗", "오목하다", "구르다", "바로잡다", "스르르", "때문", "달구다", "때때로",
    "말굽", "동니다", "니오다", "하품", "포중", "치증기", "동조", "나래", "보습", "무디다"
]

# 3. 세션 상태(Session State) 초기화
if "active_words" not in st.session_state:
    # 게임 시작 시 화면에 깔려있을 기본 단어 7개 무작위 선택
    st.session_state.active_words = random.sample(WORD_POOL, 7)
if "score" not in st.session_state:
    st.session_state.score = 0
if "stage" not in st.session_state:
    st.session_state.stage = 10  # 예시 사진의 10단계 매칭
if "last_spawn_time" not in st.session_state:
    st.session_state.last_spawn_time = time.time()

# 4. 단어 타이핑 정답 확인 함수
def check_typing():
    user_word = st.session_state.typing_input.strip()
    if user_word in st.session_state.active_words:
        st.session_state.active_words.remove(user_word)
        st.session_state.score += 10
        # 채굴 성공 시 단어 풀에서 새로운 단어 하나 보충
        available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
        if available_words:
            st.session_state.active_words.append(random.choice(available_words))
    st.session_state.typing_input = ""  # 입력창 비우기

# 5. 시간 흐름에 따른 새로운 자원(단어) 자동 생성 로직 (3초마다 1개씩 추가)
current_time = time.time()
if current_time - st.session_state.last_spawn_time > 3.0:
    # 화면에 단어가 너무 꽉 차지 않도록 최대 25개로 제한
    if len(st.session_state.active_words) < 25:
        available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
        if available_words:
            st.session_state.active_words.append(random.choice(available_words))
    st.session_state.last_spawn_time = current_time

# 6. 메인 화면 레이아웃 구성
st.title("⛏️ 한컴타자: 자원캐기 (Web Edition)")

col_left, col_right = st.columns([3, 1])

# 좌측 영역: 실제 광산 필드 (단어들이 나타나는 곳)
with col_left:
    st.markdown("### ⛰️ 광산 필드")
    
    # HTML을 활용해 화면에 현재 활성화된 단어들을 광물 조각처럼 뿌려줌
    word_html = "".join([f'<div class="resource-item">💎 {word}</div>' for word in st.session_state.active_words])
    st.markdown(f'<div class="mine-field">{word_html}</div>', unsafe_allow_html=True)
    
    st.write("")
    # 유저 입력창 (Enter를 누르면 check_typing 함수 실행)
    st.text_input(
        "광물을 캐기 위해 단어를 입력하세요:",
        key="typing_input",
        on_change=check_typing,
        placeholder="화면에 보이는 단어를 입력하고 Enter!"
    )

# 우측 영역: 스코어보드 및 캐릭터 정보 (사진 속 UI 모방)
with col_right:
    st.markdown('### 👤 유저 정보')
    with st.container():
        st.markdown("""
        <div class="sidebar-panel">
            <div style="font-size: 60px;">👦</div>
            <p><b>User: JooandKyu</b></p>
            <hr style="margin: 10px 0; border-color: #b59d83;">
            <p style="font-size: 18px; font-weight: bold;">제 10 단계</p>
            <div class="score-txt">현재 점수: {score} 점</div>
        </div>
        """.format(score=st.session_state.score), unsafe_allow_html=True)
    
    st.write("")
    if st.button("🔄 게임 리셋", use_container_width=True):
        st.session_state.active_words = random.sample(WORD_POOL, 7)
        st.session_state.score = 0
        st.session_state.last_spawn_time = time.time()
        st.rerun()

# 7. 주기적 화면 리프레시를 유도하여 실시간으로 단어가 추가되게 만듦
# (유저가 입력하지 않아도 2초마다 백엔드가 감지하여 화면을 다시 그림)
time.sleep(2.0)
st.rerun()
