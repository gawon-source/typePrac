import streamlit as st
import random
import time

# 1. 페이지 기본 설정 및 스타일(UI/UX) 적용
st.set_page_config(page_title="타자 광산: 자원캐기", page_icon="⛏️", layout="centered")

# 광산 분위기를 내기 위한 CSS 스타일링
st.markdown("""
    <style>
    .stApp {
        background-color: #2c251e;
        color: #ffffff;
    }
    .mine-container {
        background: linear-gradient(180deg, #1a1510 0%, #3d3125 100%);
        border: 4px solid #8b5a2b;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }
    .miner-char {
        font-size: 50px;
        animation: bounce 0.5s infinite alternate;
    }
    @keyframes bounce {
        from { transform: translateY(0px); }
        to { transform: translateY(-10px); }
    }
    .resource-box {
        background-color: #4a3c31;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        border-left: 5px solid #00ffcc;
    }
    .word-to-type {
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 2px;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0,255,204,0.5);
    }
    .score-badge {
        font-size: 20px;
        background-color: #ffcc00;
        color: #000;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 게임 데이터 및 세션 상태 초기화
WORDS = ["곡괭이", "다이아몬드", "황금", "에메랄드", "광부", "다이너마이트", "철광석", "석탄", "보물상자", "수정", "지하도시", "안전모"]

if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(WORDS)
if "mining_status" not in st.session_state:
    st.session_state.mining_status = ""

# 3. 단어 확인 및 정답 처리 로직
def check_word():
    user_input = st.session_state.user_input.strip()
    if user_input == st.session_state.current_word:
        st.session_state.score += 10
        st.session_state.mining_status = f"⛏️ 캉! 성공! {st.session_state.current_word}을(를) 캤습니다! (+10점)"
        st.session_state.current_word = random.choice(WORDS)
    else:
        if user_input:
            st.session_state.mining_status = "❌ 헛스윙! 정확하게 입력하세요!"
    # 입력창 비우기
    st.session_state.user_input = ""

# 4. 메인 UI 렌더링
st.title("⛏️ 타자 광산: 자원캐기 게임")
st.write("화면에 나타나는 자원의 이름을 정확히 입력하여 보석을 채굴하세요!")

# 광산 대시보드 영역
st.markdown("""
<div class="mine-container">
    <div class="miner-char">👨‍🏭 ⛏️ ✨</div>
    <p style="color: #aaa; font-size: 14px;">광부가 열심히 채굴할 준비를 하고 있습니다!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 점수 및 타겟 단어 표시
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### 🎯 현재 목표 자원")
    st.markdown(f'<div class="resource-box"><span class="word-to-type">{st.session_state.current_word}</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🎒 나의 배낭 (점수)")
    st.markdown(f'<p></p><span class="score-badge">💎 {st.session_state.score} 점</span>', unsafe_allow_html=True)

# 5. 입력 창 (엔터를 누르면 check_word 함수 실행)
st.text_input(
    "여기에 타자를 입력하고 [Enter]를 누르세요:", 
    key="user_input", 
    on_change=check_word,
    placeholder="자원 이름을 입력하세요..."
)

# 6. 피드백 메시지 출력
if st.session_state.mining_status:
    if "성공" in st.session_state.mining_status:
        st.success(st.session_state.mining_status)
    else:
        st.error(st.session_state.mining_status)

# 7. 게임 리셋 버튼
if st.button("🔄 광산 초기화"):
    st.session_state.score = 0
    st.session_state.current_word = random.choice(WORDS)
    st.session_state.mining_status = "광산이 초기화되었습니다. 다시 시작하세요!"
    st.rerun()
