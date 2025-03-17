import streamlit as st
import random
import time
from PIL import Image
import os

# 페이지 설정
st.set_page_config(page_title="이프로 시음 조사 경품", page_icon="🎉")

st.title("🎉 이프로 시음 조사 경품 🎉")

# 세션 상태 초기화
if "participants" not in st.session_state:
    st.session_state.participants = [f"참가자 {i}" for i in range(1, 81)]
    st.session_state.prizes = ["100%", "20%", "3%"] + ["2%"] * 77
    random.shuffle(st.session_state.prizes)
    st.session_state.current_index = 0
    st.session_state.winners = []

# 버튼 클릭 이벤트 처리
if st.button("🎲 제비뽑기 시작!"):
    if st.session_state.current_index < len(st.session_state.participants):
        participant = st.session_state.participants[st.session_state.current_index]
        prize = st.session_state.prizes[st.session_state.current_index]

        with st.spinner(f"{participant}님의 결과를 뽑는 중입니다..."):
            time.sleep(2)

        # 이미지 경로 설정
        prize_images = {
            "100%": "gold_medal.png",
            "20%": "silver_medal.png",
            "3%": "bronze_medal.png",
            "2%": "consolation.png"
        }
        img_path = prize_images.get(prize, None)

        # 결과 표시
        st.success(f"{participant}님의 결과: {prize}")

        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, use_column_width=True)
        else:
            st.info(f"(이미지 파일 '{img_path}' 없음)")

        # 당첨자 저장 및 인덱스 증가
        st.session_state.winners.append((participant, prize))
        st.session_state.current_index += 1

    else:
        st.success("모든 참가자의 제비뽑기가 완료되었습니다!")
        st.balloons()

# 진행 상황 표시
progress = (st.session_state.current_index / len(st.session_state.participants))
st.progress(progress)

# 현재까지의 당첨자 목록 표시
if st.session_state.winners:
    with st.expander("📊 현재까지의 당첨자 목록 보기"):
        for winner, prize in st.session_state.winners:
            st.write(f"{winner}: {prize}")
