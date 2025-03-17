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

# 참가자 이름 입력받기
name_input = st.text_input("참가자 이름을 입력하세요:", key="name_input")

if name_input:  # 이름이 입력되었을 때 바로 처리
    if len(st.session_state.participants) >= 10:
        st.warning("참가자는 최대 10명까지만 등록할 수 있습니다!")
    elif name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        
        # 등수 조건에 따라 경품 할당 (랜덤 선정)
        prize = None
        winner = None
        
        if len(st.session_state.participants) <= 3:  # 첫 번째 그룹 (1~3번째 참가자)
            eligible_group = [p for p in st.session_state.participants[:3] if p != st.session_state.winners["3%"]]
            if not st.session_state.winners["3%"] and eligible_group:
                random.shuffle(eligible_group)  # 그룹 내 순서를 섞음
                prize = "3%"
                winner = eligible_group[0]  # 섞인 그룹에서 첫 번째를 선택
                st.session_state.winners["3%"] = winner

        elif len(st.session_state.participants) <= 6:  # 두 번째 그룹 (4~6번째 참가자)
            eligible_group = [p for p in st.session_state.participants[3:6] if p != st.session_state.winners["20%"]]
            if not st.session_state.winners["20%"] and eligible_group:
                random.shuffle(eligible_group)  # 그룹 내 순서를 섞음
                prize = "20%"
                winner = eligible_group[0]  # 섞인 그룹에서 첫 번째를 선택
                st.session_state.winners["20%"] = winner

        elif len(st.session_state.participants) <= 10:  # 세 번째 그룹 (7~10번째 참가자)
            eligible_group = [p for p in st.session_state.participants[6:10] if p != st.session_state.winners["100%"]]
            if not st.session_state.winners["100%"] and eligible_group:
                random.shuffle(eligible_group)  # 그룹 내 순서를 섞음
                prize = "100%"
                winner = eligible_group[0]  # 섞인 그룹에서 첫 번째를 선택
                st.session_state.winners["100%"] = winner

        if prize is None:  # 기타 참가자 처리 (2%)
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
                    f"<p style='color: pink;'>등록 완료! 결과는 이미 발표되었습니다!</p>",
                    unsafe_allow_html=True,
                )

            # 현재까지의 당첨자 목록 표시 (결과와 함께 출력)
            st.subheader("📊 현재까지의 당첨자 목록")
            
            for prize_key, label in {"100%": "1등", "20%": "2등", "3%": "3등"}.items():
                winner_name = st.session_state.winners[prize_key]
                if winner_name:
                    st.write(f"{label}: {winner_name}")

            total_count = len(st.session_state.participants)
            st.write(f"총 등록된 인원: {total_count}명")

        # 오른쪽: 이미지 표시 (원본 크기 유지)
        with col2:
            if img_path and os.path.exists(img_path):
                img = Image.open(img_path)
                # 원본 크기로 이미지 표시
                st.image(img)  
            else:
                if prize is not None:
                    st.info(f"(이미지 파일 '{img_path}' 없음)")

# 진행 상황 표시 (넓은 화면에 맞게 진행 바 표시)
progress = (len(st.session_state.participants) / 10) if len(st.session_state.participants) > 0 else 0
st.progress(progress)

if len(st.session_state.participants) == 10:
    st.success("모든 참가자의 제비뽑기가 완료되었습니다!")
