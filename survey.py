import streamlit as st
import random
import time
from PIL import Image
import os

# 페이지 설정 (레이아웃을 "wide"로 설정하여 화면을 넓게 사용)
st.set_page_config(page_title="이프로 소비자 조사 경품", page_icon="🎉", layout="wide")

st.title("🎉 이프로 시음 조사 경품 🎉")

# 세션 상태 초기화
if "participants" not in st.session_state:
    st.session_state.participants = []  # 참가자 이름 리스트 초기화
    st.session_state.winners = {"100%": None, "20%": None, "3%": None}  # 당첨자 초기화
    st.session_state.prize_assigned = False  # 경품이 미리 할당되었는지 여부

# 경품을 미리 할당하는 함수
def assign_prizes():
    if not st.session_state.prize_assigned:
        # 각 그룹별로 랜덤으로 당첨자 선정
        st.session_state.group_1_winner = random.randint(1, 3)  # 1~3번 중 랜덤으로 선정 (3등)
        st.session_state.group_2_winner = random.randint(4, 6)  # 4~6번 중 랜덤으로 선정 (2등)
        st.session_state.group_3_winner = random.randint(7, 10) # 7~10번 중 랜덤으로 선정 (1등)
        st.session_state.prize_assigned = True

# 경품을 미리 할당
assign_prizes()

# 참가자 이름 입력받기
name_input = st.text_input("참가자 이름을 입력하세요:", key="name_input")

if name_input:  # 이름이 입력되었을 때 바로 처리
    if len(st.session_state.participants) >= 10:
        st.warning("참가자는 최대 10명까지만 등록할 수 있습니다!")
    elif name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        participant_index = len(st.session_state.participants)  # 현재 참가자 순서 (1부터 시작)

        # 참가자의 순서에 따라 경품 결정
        prize = None
        if participant_index == st.session_state.group_1_winner:  # 그룹 1의 당첨자 (3등)
            prize = "3%"
            winner = name_input
            st.session_state.winners["3%"] = winner
        elif participant_index == st.session_state.group_2_winner:  # 그룹 2의 당첨자 (2등)
            prize = "20%"
            winner = name_input
            st.session_state.winners["20%"] = winner
        elif participant_index == st.session_state.group_3_winner:  # 그룹 3의 당첨자 (1등)
            prize = "100%"
            winner = name_input
            st.session_state.winners["100%"] = winner
        else:  # 기타 참가자 (2%)
            prize = "2%"
            winner = name_input

        with st.spinner(f"{name_input}님의 결과를 뽑는 중입니다..."):
            time.sleep(2)

        # 이미지 경로 설정
        prize_images = {
            "100%": ".devcontainer/stanley.png",
            "20%": ".devcontainer/teto.png",
            "3%": ".devcontainer/euthymol.png",
            "2%": ".devcontainer/2_percent.png"
        }
        img_path = prize_images.get(prize, None)

        # 좌우 레이아웃 설정 (화면 폭 축소: 비율 조정)
        col1, col2 = st.columns([2, 1])  # 왼쪽(결과): 비율 2, 오른쪽(이미지): 비율 1

        # 왼쪽: 결과 및 당첨자 목록 표시
        with col1:
            if prize == "100%":
                st.markdown(
                    f"<h1 style='color: pink;'>🎉 축하합니다! {winner}님! 1등입니다! 이제 텀블러에 이프로 담아서 마셔보세요! :) 🎉</h1>",
                    unsafe_allow_html=True,
                )
                st.balloons()

            elif prize == "20%":
                st.markdown(
                    f"<h2 style='color: pink;'>🥈 {winner}님이 2등입니다! 이제 운동 후, 이프로 마시고 이 수건을 써보세요! 축하드립니다! 🥈</h2>",
                    unsafe_allow_html=True,
                )
                st.snow()

            elif prize == "3%":
                st.markdown(
                    f"<h3 style='color: pink;'>🥉 {winner}님이 3등입니다! 이프로 마시고 양치해야겠죠? 축하드립니다! 🥉</h3>",
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    f"<p style='color: pink;'>{name_input}님은 특별한 날을 만들어줄 이프로와 함께하세요!</p>",
                    unsafe_allow_html=True,
                )

            # 현재까지의 당첨자 목록 표시 (결과와 함께 출력)
            st.subheader("📊 현재까지의 당첨자 목록")
            
            for prize_key, label in {"100%": "1등", "20%": "2등", "3%": "3등"}.items():
                winner_name = st.session_state.winners[prize_key]
