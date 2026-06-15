import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 페이지 기본 설정
st.set_page_config(page_title="현대자동차 10대 Hyundai Way 통합 인성검사 PRO", layout="wide")

# 🎯 [오타 수정 완료] 민찮한 -> 민첩한 실행으로 완벽하게 고쳤습니다!
HYUNDAI_WAY = {
    1: "최고 수준의 안전과 품질",
    2: "집요함",
    3: "시도와 발전",
    4: "민첩한 실행", 
    5: "협업",
    6: "회복탄력성",
    7: "다양성 포용",
    8: "전문성",
    9: "윤리준수",
    10: "데이터 기반 사고"
}

# ------------------------------------------------------------------
# [정적 마스터 데이터 및 가중치 정의]
# ------------------------------------------------------------------
@st.cache_data
def get_master_part1():
    base_texts = {
        1: "품질 기준을 맞추기 위해 사소한 예외도 두지 않는다.",
        2: "해결하기 어려운 과제라도 끝까지 물고 늘어진다.",
        3: "실패 위험이 있더라도 새로운 방식을 시도한다.",
        4: "결정이 내려지면 망설이지 않고 민첩하게 행동한다.",
        5: "조직의 목표를 위해 동료들과 완벽한 호흡을 맞춘다.",
        6: "극심한 스트레스나 시련이 와도 금방 털고 일어난다.",
        7: "나와 가치관이 다른 사람들의 의견도 귀담아듣는다.",
        8: "담당 분야의 전문 지식을 쌓기 위해 꾸준히 노력한다.",
        9: "사소한 사내 규정이나 윤리 원칙도 반드시 사수한다.",
        10: "감정에 치우치기보다 철저히 데이터에 근거해 판단한다."
    }
    data = []
    item_id = 1
    for set_id in range(1, 53):
        for i in range(3):
            if item_id > 155: break
            dim_idx = ((item_id - 1) % 10) + 1
            np.random.seed(item_id)
            weight = float(np.random.uniform(0.7, 1.5))
            
            data.append({
                "item_id": item_id,
                "original_set_id": set_id,
                "text": base_texts[dim_idx],
                "dim": HYUNDAI_WAY[dim_idx],
                "weight": weight
            })
            item_id += 1
    return data

@st.cache_data
def get_master_part2():
    base_samples = [
        ("아무리 촉박한 상황이라도 안전 규정은 100% 준수해야 한다.", "최고 수준의 안전과 품질"),
        ("한 번 시작한 일은 결과가 나올 때까지 결코 포기하지 않는다.", "집요함"),
        ("현실에 안주하기보다 더 나은 혁신 방식을 제안하는 편이다.", "시도와 발전"),
        ("예상치 못한 변수가 생기면 신속하고 기민하게 대안을 실행한다.", "민첩한 실행"),
        ("팀의 공동 성과를 위해서라면 개인의 선호를 양보할 수 있다.", "협업"),
        ("실패나 지적을 받더라도 감정에 빠지지 않고 빠르게 페이스를 찾는다.", "회복탄력성"),
        ("나와 다른 업무 스타일을 가진 동료와도 조화롭게 협업한다.", "다양성 포용"),
        ("내 직무 분야에서 최고의 전문가가 되기 위한 구체적 루틴이 있다.", "전문성"),
        ("누가 보지 않는 상황에서도 도덕적 원칙을 타협하지 않는다.", "윤리준수"),
        ("경험이나 직관보다 객관적인 통계 데이터와 지표를 신뢰한다.", "데이터 기반 사고")
    ]
    data = []
    for item_id in range(1, 301):
        idx = (item_id - 1) % len(base_samples)
        text, dim = base_samples[idx]
        np.random.seed(item_id + 200)
        weight = float(np.random.uniform(0.8, 1.4))
        
        data.append({
            "item_id": item_id,
            "text": text,
            "dim": dim,
            "weight": weight
        })
    return data

# ------------------------------------------------------------------
# [세션 상태 구조화 및 무작위 셔플링 초기화]
# ------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "INTRO"
if "p1_likert" not in st.session_state:
    st.session_state.p1_likert = {}
if "p1_forced" not in st.session_state:
    st.session_state.p1_forced = {}
if "p2_ans" not in st.session_state:
    st.session_state.p2_ans = {}
if "p1_page" not in st.session_state:
    st.session_state.p1_page = 0
if "p2_page" not in st.session_state:
    st.session_state.p2_page = 0

if "p1_shuffled_sets" not in st.session_state:
    p1_master = get_master_part1()
    random.seed(42) 
    random.shuffle(p1_master)
    
    shuffled_sets = []
    chunk_size = 3
    for i in range(0, len(p1_master), chunk_size):
        shuffled_sets.append(p1_master[i:i+chunk_size])
    st.session_state.p1_shuffled_sets = shuffled_sets

if "p2_shuffled_items" not in st.session_state:
    p2_master = get_master_part2()
    random.seed(42)
    random.shuffle(p2_master)
    st.session_state.p2_shuffled_items = p2_master

# ------------------------------------------------------------------
# [화면 구성 - INTRO]
# ------------------------------------------------------------------
if st.session_state.stage == "INTRO":
    st.title("🚗 현대자동차 10대 Hyundai Way 인성검사 PRO")
    st.write("---")
    st.markdown("""
    본 버전은 대기업 채용 프로그램 실전 구동 환경과 동일한 **통계학적 블랙박스(IRT 가중치 모델)**와 **인지 과부하용 문항 셔플링** 기능이 활성화된 모의고사입니다.
    
    ### ⚙️ 시스템 동작 규칙
    1. **문항 완전 무작위 배치 (Shuffling)**: 문항 순서가 완전히 뒤섞여 출제되므로 직전 답변에 의존해 끼워 맞추는 거짓 응답이 통하지 않습니다.
    2. **6점 척도 및 체크박스 검증**: 파트 1 질문에 대해 1~6점 마킹 및 세트 내 가깝다/멀다를 직접 체크합니다.
    3. **정규분포 환산형 점수제**: 가상의 합격자 집단 분포 곡선과 비교하여 내 최종 위치를 상대점수로 도출합니다.
    """)
    if st.button("🚀 실전 셔플링 테스트 시작", type="primary"):
        st.session_state.stage = "PART1"
        st.rerun()

# ------------------------------------------------------------------
# [화면 구성 - PART 1]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART1":
    st.header("📋 파트 1: 셔플링 강제선택형 검사 (155문항 / 총 52세트)")
    st.caption("6
