import streamlit as st
import random
import time
from PIL import Image

# 페이지 설정 (레이아웃을 "wide"로 설정하여 화면을 넓게 사용)
st.set_page_config(page_title="이프로 시음 조사 경품", page_icon="🎉", layout="wide")

st.title("🎉 이프로 시음 조사 경품 🎉")

# 세션 상태 초기화
if "participants" not in st.session_state:
    st.session_state.participants = []  # 참가자 이름 리스트 초기화
    st.session_state.prizes = ["100%", "20%", "3%"] + ["2%"] * 77
    random.shuffle(st.session_state.prizes)
    st.session_state.current_index = 0
    st.session_state.winners = {"100%": [], "20%": [], "3%": [], "2%": 0}

# 참가자 이름 입력받기
name_input = st.text_input("참가자 이름을 입력하세요:")

if name_input:  
    if name_input not in st.session_state.participants:
        st.session_state.participants.append(name_input)
        st.success(f"참가자 '{name_input}'가 등록되었습니다!")
        
        # 입력창 초기화 (빈칸으로 설정)
        st.experimental_set_query_params(name="")

        # 결과 확인 자동 실행
        if st.session_state.current_index < len(st.session_state.participants):
            participant = st.session_state.participants[st.session_state.current_index]
            prize = st.session_state.prizes[st.session_state.current_index]

            with st.spinner(f"{participant}님의 결과를 뽑는 중입니다..."):
                time.sleep(2)

            # 이미지 경로 설정 (루트 디렉토리 기준)
            prize_images = {
                "100%": "stanley.png",
                "20%": "teto.png",
                "3%": "euthymol.png",
                "2%": "2_percent.png"
            }
            img_path = prize_images.get(prize, None)

            # 좌우 레이아웃 설정 (화면 폭 축소: 비율 조정)
            col1, col2 = st.columns([3, 1]) 

            # 왼쪽: 결과 및 당첨자 목록 표시
            with col1:
                if prize == "100%":
                    st.markdown(
                        f"<h1 style='color: gold;'>🎉 축하합니다! {participant}님이 1등입니다! 🎉</h1>",
                        unsafe_allow_html=True,
                    )
                    st.balloons()

                elif prize == "20%":
                    st.markdown(
                        f"<h2 style='color: silver;'>🥈 {participant}님이 2등입니다! 축하드립니다! 🥈</h2>",
                        unsafe_allow_html=True,
                    )
                    st.snow()

                elif prize == "3%":
                    st.markdown(
                        f"<h3 style='color: bronze;'>🥉 {participant}님이 3등입니다! 축하드립니다! 🥉</h3>",
                        unsafe_allow_html=True,
                    )

                else:
                    st.write(f"{participant}님, 아쉽지만 다음 기회를 노려보세요!")

                # 현재까지의 당첨자 목록 표시 (결과와 함께 출력)
                st.subheader("📊 현재까지의 당첨자 목록")
                
                if prize == "2%":
                    st.session_state.winners["2%"] += 1
                else:
                    st.session_state.winners[prize].append(participant)

                two_percent_count = st.session_state.winners["2%"]
                st.write(f"2% 당첨자 총 인원: {two_percent_count}명")

                for prize_key, winners in {"100%": "1등", "20%": "2등", "3%": "3등"}.items():
                    names = ", ".join(st.session_state.winners[prize_key])
                    if names:
                        st.write(f"{winners}: {names}")

            with col2:
                if img_path and os.path.exists(img_path):
                    img = Image.open(img_path)
                    resized_img = img.resize((300, 300))
                    st.image(resized_img, use_container_width=True)
                else:
                    st.info(f"(이미지 파일 '{img_path}' 없음)")

            # 다음 참가자로 이동
            st.session_state.current_index += 1

progress = (st.session_state.current_index / len(st.session_state.participants)) if len(st.session_state.participants) > 0 else 0
st.progress(progress)
