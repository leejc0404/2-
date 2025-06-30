# =================================
# 🎮 소혜's Birthday present event
# =================================
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="소혜's Birthday present event", page_icon="🎮", layout="centered")

# 타이틀 출력
st.title("🎮 소혜's Birthday present event")
st.markdown("**정해진 시간에만 문제를 풀 수 있는 소혜's Birthday present event!**")

# 시간별 문제/정답/상품 데이터 (시간대 구간 추가)
QUIZ_LIST = [
    {
        "start_hour": 11,  # 오전 11시 시작
        "end_hour": 12,    # 오전 12시 전까지
        "label": "오전 11시",
        "question": "우리가 갈 식당은!? 우리나라에서 가장 비싼....ㄱ....ㅂ??",
        "answer": "정식당",
        "prize": "정식당 식사권!!"
    },
    {
        "start_hour": 14,
        "end_hour": 16,
        "label": "오후 2시",
        "question": """힌트 : 소설 『수난이대』(하근찬)

이 소설에서 O은 상징적으로 반복적으로 등장합니다. 주인공 박만도는 한쪽 O을 잃고, 남은 OO으로 아들을 감싸 안으려는 장면이 인상적입니다.

여기서 OO은 삶의 고통과 끈질긴 생명력, 부성애를 상징합니다. “O로 내 목을 감아야 될 끼다.”라는 대사처럼, OO은 단순한 신체 부위를 넘어 감정과 의지의 매개체로 그려집니다.

여기서 OO에 들어갈 말은!?""",
        "answer": "팔뚝",
        "prize": "두둥!! 이쁘니 상품권 (https://drive.google.com/file/d/1oBzlfLweKRhdB9Y6Vri9kkBuKvj-0GKw/view?usp=drive_link)"
    },
    {
        "start_hour": 16,
        "end_hour": 18,
        "label": "오후 4시",
        "question": "여태 OO을(를) 소혜보다 좋아하는 사람을 본적이 없다!! 여기서 OO에 들어갈 말은?",
        "answer": "과일",
        "prize": "과일 6종 세트!! 묵으라!!"
    },
    {
        "start_hour": 18,
        "end_hour": 20,
        "label": "오후 6시",
        "question": "갈갈갈... (대신 [브랜드][용도][명칭] 다 맞춰야 함. 8글자)",
        "answer": "닌자휴대용블랜더",
        "prize": "블렌더 1대. 남은 과일 갈아보자!!"
    },
    {
        "start_hour": 20,
        "end_hour": 22,
        "label": "오후 8시",
        "question": "\"강아지꺼 뺏은거 같아\", 4월 25일, [브랜드][명칭], 6글자",
        "answer": "잔스포츠가방",
        "prize": "귀요미 가방!!"
    },
    {
        "start_hour": 22,
        "end_hour": 24,
        "label": "오후 10시",
        "question": "\"내일 필요한 거지... 활활 타라~, 5글자\"",
        "answer": "마시멜로우",
        "prize": "그렇지 캠프파이어와 마시멜로우여!!! 생일 축하해 울소혜!"
    }
]

# 현재 시간에 해당하는 퀴즈 가져오기 (시간대 구간 체크)
def get_current_quiz():
    now = pd.Timestamp.now(tz="Asia/Seoul")
    now_hour = now.hour
    now_minute = now.minute
    
    for quiz in QUIZ_LIST:
        # 현재 시간이 해당 퀴즈의 시간대에 속하는지 확인
        if now_hour >= quiz["start_hour"] and now_hour < quiz["end_hour"]:
            return quiz
    return None  # 해당 시간대 없음

quiz = get_current_quiz()

if quiz:
    # 문제 표시
    st.header(f"🕒 {quiz['label']} 문제")
    st.write(quiz["question"])

    # 세션 상태 확인 및 초기화
    if "solved" not in st.session_state:
        st.session_state.solved = False

    # 정답 입력 및 판별
    if not st.session_state.solved:
        answer = st.text_input("정답을 입력하세요 (띄어쓰기 없이):", key="answer_input")
        if st.button("제출") or (answer and st.session_state.get("last_answer") != answer):
            st.session_state.last_answer = answer
            if answer and answer.replace(" ", "") == quiz["answer"]:
                st.success(f"정답! 🎉 상품: {quiz['prize']}")
                st.session_state.solved = True

                # 문제별 애니메이션
                if quiz["start_hour"] == 11:
                    st.balloons()
                elif quiz["start_hour"] == 14:
                    st.balloons()
                elif quiz["start_hour"] == 16:
                    st.markdown("""
                    <div style="position:relative;width:100%;height:0;padding-bottom:56.25%;">
                        <iframe src="https://giphy.com/embed/26ufdipQqU2lhNA4g" 
                                width="100%" height="100%" 
                                style="position:absolute" frameBorder="0" allowFullScreen>
                        </iframe>
                    </div>
                    """, unsafe_allow_html=True)
                elif quiz["start_hour"] == 18:
                    st.markdown("""
                    <style>
                    .star {
                        animation: spin 2s linear infinite;
                        font-size: 40px;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    </style>
                    <div class="star">✨✨✨</div>
                    """, unsafe_allow_html=True)
                elif quiz["start_hour"] == 20:
                    st.markdown("""
                    <style>
                    .gift {
                        animation: shake 0.5s;
                        animation-iteration-count: infinite;
                        font-size: 40px;
                    }
                    @keyframes shake {
                      0% { transform: translate(1px, 1px) rotate(0deg); }
                      25% { transform: translate(-1px, -2px) rotate(-1deg); }
                      50% { transform: translate(-3px, 0px) rotate(1deg); }
                      75% { transform: translate(3px, 2px) rotate(0deg); }
                      100% { transform: translate(1px, -1px) rotate(1deg); }
                    }
                    </style>
                    <div class="gift">🎁🎁🎁</div>
                    """, unsafe_allow_html=True)
                elif quiz["start_hour"] == 22:
                    st.markdown("""
                    <div style="text-align:center">
                        <img src="https://media.giphy.com/media/L0N9j5QzZk3hM/giphy.gif" width="100%">
                    </div>
                    """, unsafe_allow_html=True)
            elif answer:
                st.error("틀렸즹~ 오답이징~")
else:
    # LOADING... 애니메이션 적용
    components.html("""
    <div style="font-size:24px; text-align:center; margin-bottom:10px;">
        <div id="loading" style="font-weight:bold;">LOADING.</div>
    </div>
    <script>
    let dots = 1;
    setInterval(function() {
        document.getElementById("loading").innerHTML = "LOADING" + ".".repeat(dots);
        dots = dots % 3 + 1;
    }, 500);
    </script>
    """, height=60)
    st.write("아직 문제 시간이 아닙니다. 조금만 기다려 주세요!")

# 안내
st.markdown("---")
st.markdown("""
<div style='background-color:#f8f9fa; border-left:4px solid #ff6b6b; padding:12px 16px; border-radius:4px; margin:12px 0;'>
  <p style='color:#333; font-size:16px; font-weight:500; margin:0;'>⏰ 정해진 시간(오전 11시, 오후 2시/4시/6시/8시/10시)에만 문제가 오픈됩니다</p>
  <p style='color:#666; font-size:14px; margin-top:8px; margin-bottom:0;'>제한 시간 내에 맞추지 못하면 선물은 출제자의 몫입니다</p>
</div>
""", unsafe_allow_html=True)
