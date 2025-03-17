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
    
    # 총 참가자 수 (예: 최대 10명)
    total_participants = 10
    
    # 경품 리스트 생성 및 섹션별 나누기
    section_size = total_participants // 3  # 각 섹션 크기 (정수로 나눔)
    
    # 각 섹션에 해당하는 경품 리스트 생성
    prizes_100 = ["100%"] * section_size  # 첫 섹션은 100%
    prizes_3 = ["3%"] * section_size      # 두 번째 섹션은 3%
    prizes_20 = ["20%"] * (total_participants - section_size * 2)  # 나머지는 20%

    # 각 섹션을 랜덤으로 섞음
    random.shuffle(prizes_100)
    random.shuffle(prizes_3)
    random.shuffle(prizes_20)

    # 최종 경품 리스트 결합
    st.session_state.prizes = prizes_100 + prizes_3 + prizes_20
    
    st.session_state.winners = {"100%": [], "20%": [], "3%": [], "2%": 0}

# 참가자 이름 입력받기
name_input = st.text_input("참가자 이름을 입력하세요:", key="name_input")

if name_input:  # 이름이 입력되었을 때 바로 처리
    if len(st.session_state.participants) >= total_participants:
        st.warning(f"참가자는 최대 {total_participants}명까지만 등록할 수 있습니다!")
    elif name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        st.success(f"참가자 '{name_input}'님이 등록되었습니다!")

        # 결과 확인 자동 실행 (순서대로 매칭)
        current_index = len(st.session_state.participants) - 1
        prize = st.session_state.prizes[current_index]  # 미리 섞어둔 경품 리스트에서 순서대로 가져옴

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
                    f"<h1 style='color: pink;'>🎉 축하합니다! {name_input}님! 1등입니다! 이제 텀블러에 이프로 담아서 마셔보세요! :) 🎉</h1>",
                    unsafe_allow_html=True,
                )
                st.balloons()

            elif prize == "20%":
                st.markdown(
                    f"<h2 style='color: pink;'>🥈 {name_input}님이 2등입니다! 이제 운동 후, 이프로 마시고 이 수건을 써보세요! 축하드립니다! 🥈</h2>",
                    unsafe_allow_html=True,
                )
                st.snow()

            elif prize == "3%":
                st.markdown(
                    f"<h3 style='color: pink;'>🥉 {name_input}님이 3등입니다! 이프로 마시고 양치해야겠죠? 축하드립니다! 🥉</h3>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<p style='color: pink;'>{name_input}님, 이프로로 오늘 일상도 특별하게!!</p>",
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

        # 오른쪽: 이미지 표시 (원본 크기 유지)
        with col2:
            if img_path and os.path.exists(img_path):
                img = Image.open(img_path)
                # 원본 크기로 이미지 표시
                st.image(img)  
            else:
                st.info(f"(이미지 파일 '{img_path}' 없음)")

# 진행 상황 표시 (넓은 화면에 맞게 진행 바 표시)
progress = (len(st.session_state.participants) / total_participants) if total_participants > 0 else 0
st.progress(progress)
