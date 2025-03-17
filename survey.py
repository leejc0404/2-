pip install pandas
import pandas as pd
chart_df = pd.DataFrame([chart_data.values()], columns=chart_data.keys())

import streamlit as st
import random
import time
from PIL import Image
import os


# Set page configuration
st.set_page_config(page_title="이프로 소비자 조사 경품", page_icon="🎉", layout="wide")

st.title("🎉 이프로복숭아 소비자 조사 경품 🎉\n - 슬로건 : 이프로부족할때, 일상의 특별함을 더하다")
#st.markdown("<h2 style='color: orange;'>슬로건: 이프로부족할때, 일상의 특별함을 더하다</h2>", unsafe_allow_html=True)

# Initialize total participants
total_participants = 10  # Set the maximum number of participants

# Session state initialization
if "participants" not in st.session_state:
    st.session_state.participants = []  # Initialize participant list
    
    # Generate prize list based on total participants
    def generate_prize_list(total_participants):
        first_third = total_participants // 3
        middle_third = total_participants // 3
        last_third = total_participants - first_third - middle_third

        first_section = ['2%'] * first_third
        middle_section = ['2%'] * middle_third
        last_section = ['2%'] * last_third

        # Place specific prizes in their respective sections
        first_section[random.randint(0, first_third - 1)] = '3%'
        middle_section[random.randint(0, middle_third - 1)] = '100%'
        last_section[random.randint(0, last_third - 1)] = '20%'

        return first_section + middle_section + last_section

    st.session_state.prizes = generate_prize_list(total_participants)
    st.session_state.winners = {"100%": [], "20%": [], "3%": [], "2%": 0}

# Participant input and processing
name_input = st.text_input("참가자 이름을 입력하세요:", key="name_input")

if name_input:
    if len(st.session_state.participants) >= total_participants:
        st.warning(f"참가자는 최대 {total_participants}명까지만 등록할 수 있습니다!")
    elif name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        st.success(f"참가자 '{name_input}'님이 등록되었습니다!")

        # 결과 확인 자동 실행 (순서대로 매칭)
        current_index = len(st.session_state.participants) - 1
        prize = st.session_state.prizes[current_index]  # 미리 섞어둔 경품 리스트에서 순서대로 가져옴

        with st.spinner(f"{name_input}님의 결과를 뽑는 중입니다... (두구두구)"):
            time.sleep(2)

        # 이미지 경로 설정
        prize_images = {
            "100%": ".devcontainer/stanley.png",
            "20%": ".devcontainer/teto.png",
            "3%": ".devcontainer/euthymol.png",
            "2%": ".devcontainer/2_percent.png"
        }
        img_path = prize_images.get(prize, None)

        # 좌우 레이아웃 설정 (결과 텍스트, 차트, 이미지)
        col1, col2, col3 = st.columns([2, 1, 1])  # 왼쪽(결과): 비율 2, 가운데(차트): 비율 1, 오른쪽(이미지): 비율 1

        # 왼쪽: 결과 텍스트 표시
        with col1:
            if prize == "100%":
                st.markdown(
                    f"<h1 style='color: pink;'>🎉 축하합니다! {name_input}님! 1등입니다! 이제 텀블러에 이프로 담아서 마셔보세요! :) 🎉</h1>",
                    unsafe_allow_html=True,
                )
                st.balloons()

            elif prize == "20%":
                st.markdown(
                    f"<h2 style='color: pink;'>🥈 축하드립니다! {name_input}님이 2등입니다! 이제 운동 후, 이프로 마시고 이 수건을 써보세요! 🥈</h2>",
                    unsafe_allow_html=True,
                )
                st.snow


            elif prize == "3%":
                st.markdown(
                    f"<h3 style='color: pink;'>🥉 축하합니다! {name_input}님이 3등입니다! 이프로가 건강해져도 마시고 양치해야겠죠? 🥉</h3>",
                    unsafe_allow_html=True,
                )
                st.star
            else:
                st.markdown(
                    f"<h4 style='color: pink;'>{name_input}님, 이프로로 오늘의 일상도 특별하게!!</h4>",
                    unsafe_allow_html=True,
                )

            # 현재까지의 당첨자 목록 표시 (결과와 함께 출력)
            st.subheader("📊 현재까지의 당첨자 목록")
            
            # 방금 결과값 포함한 당첨자 목록 업데이트
            if prize == "2%":
                st.session_state.winners["2%"] += 1
            else:
                st.session_state.winners[prize].append(name_input)

            # 총 참석 인원 및 당첨자 목록 표시
            total_registered = len(st.session_state.participants)
            two_percent_count = st.session_state.winners["2%"]
            st.write(f"총 참석 인원: {total_registered}명")
            st.write(f"이프로복숭아 설문 총 인원: {two_percent_count}명")

            # 1등, 2등, 3등 이름 공개
            for prize_key, winners in {"100%": "1등", "20%": "2등", "3%": "3등"}.items():
                names = ", ".join(st.session_state.winners[prize_key])
                if names:
                    st.write(f"{winners}: {names}")

        # 가운데: 차트 표시 (참여 인원 vs 최대 인원)
        with col2:
            total_registered = len(st.session_state.participants)
            remaining_slots = total_participants - total_registered
            
            # 차트 형태로 참여 인원 표시 (st.bar_chart 사용)
            chart_data = {
                "참여 인원": total_registered,
                "남은 자리": remaining_slots,
            }
            
            chart_df = pd.DataFrame([chart_data.values()], columns=chart_data.keys())
            st.bar_chart(chart_df)
            
        # 오른쪽: 이미지 표시 (원본 크기 유지)
        with col3:
            if img_path and os.path.exists(img_path):
                img = Image.open(img_path)
                # 원본 크기로 이미지 표시
                st.image(img)  
            else:
                st.info(f"(이미지 파일 '{img_path}' 없음)")
