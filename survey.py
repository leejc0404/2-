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
    
    # 1, 2, 3등이 반드시 포함된 경품 리스트 생성 (총 10명)
    st.session_state.prizes = ["100%", "20%", "3%"] + ["2%"] * 7
    random.shuffle(st.session_state.prizes)  # 경품 순서를 랜덤으로 섞기
    
    st.session_state.current_index = 0
    st.session_state.winners = {"100%": [], "20%": [], "3%": [], "2%": 0}

# 참가자 이름 입력받기
name_input = st.text_input("참가자 이름을 입력하세요:", key="name_input")

if name_input:  # 이름이 입력되었을 때 바로 처리
    if len(st.session_state.participants) >= 10:
        st.warning("참가자는 최대 30명까지만 등록할 수 있습니다!")
    elif name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        st.success(f"참가자 '{name_input}'님이 등록되었습니다!")

        # 결과 확인 자동 실행
        if st.session_state.current_index < len(st.session_state.participants):
            participant = st.session_state.participants[st.session_state.current_index]
            prize = st.session_state.prizes[st.session_state.current_index]
            
        # 랜덤으로 등수 부여 (1~10번 중 하나를 선택)
        prize_index = random.randint(0, len(st.session_state.prizes) - 1)
        prize = st.session_state.prizes.pop(prize_index)  # 선택된 등수 제거
    
        # 랜덤 등수 확인용 디버깅 메시지 출력 (추가됨 ✅)
        st.info(f"🔍 디버그: 랜덤으로 뽑힌 등수는 리스트의 {prize_index + 1}번째 항목이며, 당첨된 경품은 '{prize}'입니다.")
            
            with st.spinner(f"{participant}님의 결과를 뽑는 중입니다..."):
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
                        f"<h1 style='color: pink;'>🎉 축하합니다! {participant}님! 1등입니다! 이제 텀블러에 이프로 담아서 마셔보세요! :) 🎉</h1>",
                        unsafe_allow_html=True,
                    )
                    st.balloons()

                elif prize == "20%":
                    st.markdown(
                        f"<h2 style='color: pink;'>🥈 {participant}님이 2등입니다! 이제 운동 후, 이프로 마시고 이 수건을 써보세요! 축하드립니다! 🥈</h2>",
                        unsafe_allow_html=True,
                    )
                    st.snow()

                elif prize == "3%":
                    st.markdown(
                        f"<h3 style='color: pink;'>🥉 {participant}님이 3등입니다! 이프로 마시고 양치해야겠죠? 축하드립니다! 🥉</h3>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<p style='color: pink;'>{participant}님, 이프로로 오늘 일상도 특별하게!!</p>",
                        unsafe_allow_html=True,
                    )

                # 현재까지의 당첨자 목록 표시 (결과와 함께 출력)
                st.subheader("📊 현재까지의 당첨자 목록")
                
                # 방금 결과값 포함한 당첨자 목록 업데이트
                if prize == "2%":
                    st.session_state.winners["2%"] += 1
                else:
                    st.session_state.winners[prize].append(participant)

                # 2% 인원 수 표시
                two_percent_count = st.session_state.winners["2%"]
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

            # 다음 참가자로 이동
            st.session_state.current_index += 1

        else:
            if len(st.session_state.participants) < 10:
                st.warning("참가자가 아직 모두 등록되지 않았습니다!")
            else:
                st.success("모든 참가자의 제비뽑기가 완료되었습니다!")
                st.balloons()

# 진행 상황 표시 (넓은 화면에 맞게 진행 바 표시)
progress = (st.session_state.current_index / len(st.session_state.participants)) if len(st.session_state.participants) > 0 else 0
st.progress(progress)
