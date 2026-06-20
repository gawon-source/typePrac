import streamlit as st
import random

# 1. 페이지 설정 및 오리지널 감성 CSS 스타일링
st.set_page_config(page_title="한컴타자: 자원캐기 Web", page_icon="⛏️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #d7c4a9;
        color: #333333;
        font-family: 'Malgun Gothic', sans-serif;
    }
    .mine-field {
        background-color: #a68b7c;
        border: 5px solid #6e5547;
        border-radius: 10px;
        min-height: 480px;
        position: relative;
        padding: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.4);
    }
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
    .sidebar-panel {
        background-color: #eedcc5;
        border: 3px solid #b59d83;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .score-txt {
        font-size: 22px;
        font-weight: bold;
        color: #b85a00;
    }
    .quest-txt {
        font-size: 16px;
        color: #2e7d32;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 단어 풀 및 캐릭터
WORD_POOL = [
    "마음씨", "괄목", "치후", "아름", "밀기울", "안채", "날씨", "바라지", "도막말",
    "옹고집", "나부굴다", "나이", "까닥이다", "끼릉하다", "제법", "가풀막", "바글비율",
    "벼랑길", "살갗", "오목하다", "구르다", "바로잡다", "스르르", "때문", "달구다", "때때로",
    "말굽", "동니다", "니오다", "하품", "포중", "치증기", "동조", "나래", "보습", "무디다",
    "술래잡기", "중고봉긋", "활짝", "첫줄", "가기"
]

CHARACTERS = {
    "열정 광부 👦": "👦",
    "탐험가 리사 👧": "👧",
    "우주 광부 🧑‍🚀": "🧑‍🚀",
    "로봇 굴착기 🤖": "🤖",
    "판다 광부 🐼": "🐼"
}

STAGE_QUESTS = {
    1: {"target": 5, "name": "광산의 첫걸음", "reward_msg": "💎 희귀한 황석을 발견했습니다! 보너스 +50점"},
    2: {"target": 8, "name": "깊어지는 어둠", "reward_msg": "📜 고대 광부의 숨겨진 일지를 찾았습니다! 보너스 +100점"},
    3: {"target": 12, "name": "수정 동굴 탐험", "reward_msg": "🔮 전설의 보라색 거대 수정을 캤습니다! 보너스 +200점"},
    4: {"target": 15, "name": "용암 지대 진입", "reward_msg": "🔥 불타는 다이아몬드를 획득했습니다! 보너스 +300점"},
    5: {"target": 999, "name": "무한의 심연", "reward_msg": "👑 당신은 이제 전설의 마스터 광부입니다!"}
}

# 3. 세션 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "초보 광부"
if "selected_char" not in st.session_state:
    st.session_state.selected_char = "열정 광부 👦"
if "active_words" not in st.session_state:
    st.session_state.active_words = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "mined_count" not in st.session_state:
    st.session_state.mined_count = 0
if "quest_alert" not in st.session_state:
    st.session_state.quest_alert = ""

# 4. 단어 타이핑 정답 확인 함수
def check_typing():
    user_word = st.session_state.typing_input.strip()
    if user_word in st.session_state.active_words:
        st.session_state.active_words.remove(user_word)
        st.session_state.score += 10
        st.session_state.mined_count += 1
        st.session_state.quest_alert = ""
        
        current_stage_info = STAGE_QUESTS.get(st.session_state.stage, STAGE_QUESTS[5])
        if st.session_state.mined_count >= current_stage_info["target"]:
            bonus = st.session_state.stage * 50
            st.session_state.score += bonus
            st.session_state.quest_alert = f"🎉 Stage {st.session_state.stage} 클리어! {current_stage_info['reward_msg']}"
            st.session_state.stage += 1
            st.session_state.mined_count = 0
        
        # 새 단어 보충
        available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
        if available_words:
            st.session_state.active_words.append(random.choice(available_words))
            
    st.session_state.typing_input = "" # 엔터 후 입력창 비우기

# 5. 메인 UI 빌드
st.title("⛏️ 한컴타자: 자원캐기 (Web Edition)")

# --- [대기 화면] ---
if not st.session_state.game_started:
    st.markdown("### 🎒 광산에 들어가기 전 준비")
    col_setup1, col_setup2 = st.columns([2, 1])
    
    with col_setup1:
        st.info("이름을 입력하고 광부 캐릭터를 선택한 뒤 '게임 시작' 버튼을 누르세요!")
        input_name = st.text_input("광부의 이름을 입력하세요:", value="초보 광부", max_chars=12)
        
        st.session_state.selected_char = st.radio(
            "플레이할 캐릭터를 선택하세요:", options=list(CHARACTERS.keys()), horizontal=True
        )
        
        if st.button("🚀 광산 진입 (게임 시작)", type="primary", use_container_width=True):
            st.session_state.user_name = input_name.strip() if input_name.strip() else "초보 광부"
            st.session_state.game_started = True
            st.session_state.active_words = random.sample(WORD_POOL, 8) # 시작 단어 8개로 상향
            st.session_state.stage = 1
            st.session_state.mined_count = 0
            st.session_state.score = 0
            st.session_state.quest_alert = f"⛏️ {st.session_state.user_name} 광부님, 광산에 진입했습니다!"
            st.rerun()
            
    with col_setup2:
        chosen_emoji = CHARACTERS[st.session_state.selected_char]
        st.markdown(f"""
        <div class="sidebar-panel" style="padding: 30px;">
            <div style="font-size: 80px; margin-bottom: 10px;">{chosen_emoji}</div>
            <h3>{st.session_state.selected_char}</h3>
            <p style="color: #666;">준비 완료!</p>
        </div>
        """, unsafe_allow_html=True)

# --- [게임 화면] ---
else:
    if st.session_state.quest_alert:
        st.success(st.session_state.quest_alert)

    # 좌우 구조 정의 (좌측: 광산 필드만 집중, 우측: 진행 상황 및 타이핑 입력창)
    col_left, col_right = st.columns([3, 1])

    with col_left:
        # 광산 필드만 3초마다 부분 리프레시 수행
        @st.fragment(run_every=3.0)
        def render_mine_field():
            if len(st.session_state.active_words) < 25:
                available_words = [w for w in WORD_POOL if w not in st.session_state.active_words]
                if available_words:
                    st.session_state.active_words.append(random.choice(available_words))
            
            st.markdown("### ⛰️ 광산 필드")
            word_html = "".join([f'<div class="resource-item">💎 {word}</div>' for word in st.session_state.active_words])
            st.markdown(f'<div class="mine-field">{word_html}</div>', unsafe_allow_html=True)

        render_mine_field()

    with col_right:
        st.markdown('### 📊 진행 상황')
        chosen_emoji = CHARACTERS[st.session_state.selected_char]
        current_quest = STAGE_QUESTS.get(st.session_state.stage, STAGE_QUESTS[5])
        
        # 유저 대시보드
        st.markdown(f"""
        <div class="sidebar-panel">
            <div style="font-size: 50px;">{chosen_emoji}</div>
            <p style="font-size: 18px; margin-bottom: 2px;"><b>User: {st.session_state.user_name}</b></p>
            <p style="color: #666; font-size: 12px; margin-top: 0px;">({st.session_state.selected_char})</p>
            <hr style="margin: 10px 0; border-color: #b59d83;">
            <p style="font-size: 20px; font-weight: bold; color: #d32f2f;">제 {st.session_state.stage} 단계</p>
            <div class="score-txt">💰 {st.session_state.score} 점</div>
            <hr style="margin: 10px 0; border-color: #b59d83;">
            <div class="quest-txt">🎯 현재 퀘스트</div>
            <p style="font-size: 14px; margin-bottom: 5px;"><b>{current_quest['name']}</b></p>
            <p style="font-size: 13px; color: #555;">광물 채굴: {st.session_state.mined_count} / {current_quest['target']} 개</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # 🌟 핵심 수정 1: 타이핑 입력 칸을 광산 우측(진행 상황판 바로 밑)으로 이동
        # 🌟 핵심 수정 2: 오류를 뿜던 autofocus=True 제거하여 수동 마우스 클릭 입력으로 변경 (안정성 확보)
        st.text_input(
            "⌨️ 여기에 타자를 입력하세요:",
            key="typing_input",
            on_change=check_typing,
            placeholder="단어 입력 후 Enter!"
        )
        
        st.write("")
        if st.button("⏹️ 게임 종료 (대기실로)", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
