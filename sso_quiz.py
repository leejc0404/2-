# =================================
# 🎮 소혜's Birthday present event
# =================================

import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="소혜's Birthday present event", page_icon="🎮", layout="centered")

# 타이틀 출력
st.title("🎮 소혜's Birthday present event")
st.markdown("**정해진 시간에만 문제를 풀 수 있는 특별한 타임어택 퀴즈!**")

# 시간별 문제/정답/상품 데이터
QUIZ_LIST = [
    {
        "hour": 14,
        "label": "오후 2시",
        "question": """힌트 : 소설 『수난이대』(하근찬)

이 소설에서 O은 상징적으로 반복적으로 등장합니다. 주인공 박만도는 한쪽 O을 잃고, 남은 OO으로 아들을 감싸 안으려는 장면이 인상적입니다.

여기서 OO은 삶의 고통과 끈질긴 생명력, 부성애를 상징합니다. “O로 내 목을 감아야 될 끼다.”라는 대사처럼, OO은 단순한 신체 부위를 넘어 감정과 의지의 매개체로 그려집니다.

여기서 OO에 들어갈 말은!?""",
        "answer": "팔뚝",
        "prize": "두둥!! 이쁘니 상품권"
    },
    {
        "hour": 16,
        "label": "오후 4시",
        "question": "여태 OO을(를) 소혜보다 좋아하는 사람을 본적이 없다!! 여기서 OO에 들어갈 말은?",
        "answer": "과일",
        "prize": "과일 6종 세트!! 묵으라!!"
    },
    {
        "hour": 18,
        "label": "오후 6시",
        "question": "갈갈갈... (대신 [브랜드][용도][명칭] 다 맞춰야 함. 8글자)",
        "answer": "닌자휴대용블랜더",
        "prize": "블렌더 1대. 남은 과일 갈아보자!!"
    },
    {
        "hour": 20,
        "label": "오후 8시",
        "question": "\"강아지꺼 뺏은거 같아\", 4월 25일, [브랜드][명칭], 6글자",
        "answer": "잔스포츠가방",
        "prize": "귀요미 가방!!"
    },
    {
        "hour": 22,
        "label": "오후 10시",
        "question": "\"내일 필요한 거지... 활활 타라~, 5글자\"",
        "answer": "마시멜로우",
        "prize": "그렇지 캠프파이어와 마시멜로우여!!! 생일 축하해 울소혜!"
    }
]

# 현재 시간에 해당하는 퀴즈 가져오기
def get_current_quiz():
    now = pd.Timestamp.now(tz="Asia/Seoul")
    now_hour = now.hour
    for quiz in reversed(QUIZ_LIST):
        if now_hour >= quiz["hour"]:
            return quiz
    return QUIZ_LIST[0]

quiz = get_current_quiz()

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
            st.balloons()
        elif answer:
            st.error("틀렸즹~ 오답이징~")
else:
    st.info(f"이미 맞추셨습니다! 🎁 상품: {quiz['prize']}")

# 안내
st.markdown("---")
st.caption("정해진 시간에 맞는 문제만 자동으로 오픈됩니다. (오후 2시/4시/6시/8시/10시)")
