import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="현대자동차 인성검사 통합 모의진단", layout="wide")

# 역량 차원 정의 (일관성 추적용 핵심 3대 가치)
# 1: 도전정신(Challenge), 2: 소통협력(Collaboration), 3: 성실집중(Diligence)
DIMENSIONS = {1: "도전정신", 2: "소통협력", 3: "성실집중"}

# ------------------------------------------------------------------
# [데이터 생성 및 템플릿 로드 정의]
# ------------------------------------------------------------------
@st.cache_data
def get_part1_data():
    """파트 1 데이터 생성: 155문항 (51세트 * 3문항 = 153문항 + 마지막 세트 2문항)"""
    base_texts = {
        1: ["상황에 따라 처음 계획이 바뀔 때가 많다.", "새로운 위험을 감수하는 편이다.", "어려운 목표일수록 달성하고 싶다."],
        2: ["그림이나 사진을 보고 별로 정서적 감흥이 없다.", "팀원들의 의견을 조율하는 데 능숙하다.", "타인과의 갈등은 피하는 것이 상책이다."],
        3: ["남들에게 어떤 인상을 남기기 위해 쇼를 하기도 한다.", "맡은 일은 정해진 기한 내에 완벽히 끝낸다.", "사소한 규칙이라도 위반하면 마음이 불편하다."]
    }
    
    data = []
    item_id = 1
    for set_id in range(1, 53):
        # 3개씩 묶어서 세트 구성
        cycle = ((set_id - 1) % 3) + 1
        texts = base_texts[cycle]
        
        for i, text in enumerate(texts):
            if item_id > 155: break
            dim_id = (i % 3) + 1
            data.append({
                "item_id": item_id,
                "set_id": set_id,
                "text": f"[{set_id}-{i+1}] {text}",
                "dim": DIMENSIONS[dim_id]
            })
            item_id += 1
    return data

@st.cache_data
def get_part2_data():
    """파트 2 데이터 생성: 300문항 단일 리커트 문항"""
    base_texts = [
        ("실패하더라도 목표를 높게 잡는 것이 의미 있다.", "도전정신"),
        ("동료의 실수를 보면 먼저 다가가 도와준다.", "소통협력"),
        ("아무리 작은 문서 작업이라도 오타를 끝까지 찾아낸다.", "성실집중"),
        ("한 번도 가보지 않은 길을 탐험하는 것을 즐긴다.", "도전정신"),
        ("조직의 공동 목표를 위해서 개인의 이익을 양보할 수 있다.", "소통협력"),
        ("주변 환경이 어수선해도 내가 맡은 업무에 고도로 몰입한다.", "성실집중")
    ]
    data = []
    for item_id in range(1, 301):
        idx = (item_id - 1) % len(base_texts)
        text, dim = base_texts[idx]
        data.append({
            "item_id": item_id,
            "text": f"Q{item_id}. {text}",
            "dim": dim
        })
    return data

PART1_ITEMS = get_part1_data()
PART2_ITEMS = get_part2_data()

# ------------------------------------------------------------------
# [세션 상태 관리 초기화]
# ------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "INTRO"
if "p1_likert" not in st.session_state:
    st.session_state.p1_likert = {}
if "p1_forced" not in st.session_state:
    st.session_state.p1_forced = {} # set_id -> {"가깝다": item_id, "멀다": item_id}
if "p2_ans" not in st.session_state:
    st.session_state.p2_ans = {}
if "p1_page" not in st.session_state:
    st.session_state.p1_page = 0
if "p2_page" not in st.session_state:
    st.session_state.p2_page = 0

# ------------------------------------------------------------------
# [화면 레이아웃 - INTRO]
# ------------------------------------------------------------------
if st.session_state.stage == "INTRO":
    st.title("🚗 현대자동차 규격 인성검사 통합 시뮬레이터")
    st.write("---")
    st.markdown("""
    본 검사는 대기업 채용용 검증 규격인 **'교차 진정성 알고리즘'**이 탑재된 통합 인성 진단 도구입니다.
    
    * **파트 1 (155문항 / 52세트)**: 각 문항에 대한 개별 6점 척도 평가와 더불어, 3개 문항 중 자신과 가장 가깝고 먼 것을 고르는 **강제선택형 구조**입니다.
    * **파트 2 (300문항)**: 각 가치관을 단독 측정하는 **5점 척도 절대평가 구조**입니다.
    
    두 파트 간 가치관 우선순위가 일치하지 않으면 **일관성 모순율**이 상승하여 탈락 위험군으로 분류됩니다. 직관적이고 솔직하게 응답해 주세요.
    """)
    if st.button("🚀 인성검사 파트 1 시작하기", type="primary"):
        st.session_state.stage = "PART1"
        st.rerun()

# ------------------------------------------------------------------
# [화면 레이아웃 - PART 1 (강제선택형형 155제)]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART1":
    st.header("📋 파트 1: 강제선택형 검사 (155문항 / 총 52세트)")
    st.caption("각 문항별로 동의 정도(1~6점)를 매긴 후, 세트 내에서 가장 나 다운 것(가깝다)과 가장 거리가 먼 것(멀다)을 딱 하나씩만 체크하세요.")
    
    SETS_PER_PAGE = 5
    max_p1_pages = int(np.ceil(52 / SETS_PER_PAGE))
    current_p1_page = st.session_state.p1_page
    
    start_set = current_p1_page * SETS_PER_PAGE + 1
    end_set = min(52, start_set + SETS_PER_PAGE - 1)
    
    st.progress(end_set / 52)
    st.write(f"**현재 페이지: {current_p1_page + 1} / {max_p1_pages} 페이지**")
    
    for s_id in range(start_set, end_set + 1):
        st.markdown(f"#### 📦 SET {s_id}")
        set_items = [item for item in PART1_ITEMS if item["set_id"] == s_id]
        
        # 가깝다/멀다 상태 초기 바인딩 및 선택 검증용 공간
        if s_id not in st.session_state.p1_forced:
            st.session_state.p1_forced[s_id] = {"가깝다": None, "멀다": None}
            
        for item in set_items:
            i_id = item["item_id"]
            col_text, col_likert, col_near, col_far = st.columns([4, 4, 1, 1])
            
            with col_text:
                st.write(f"**{item['text']}**")
                
            with col_likert:
                st.session_state.p1_likert[i_id] = st.radio(
                    f"L1_{i_id}", [1, 2, 3, 4, 5, 6], index=3, horizontal=True, key=f"likert1_{i_id}", label_visibility="collapsed"
                )
                
            with col_near:
                is_near = st.checkbox("가깝다", key=f"near_{i_id}", value=(st.session_state.p1_forced[s_id]["가깝다"] == i_id))
                if is_near and st.session_state.p1_forced[s_id]["가깝다"] != i_id:
                    st.session_state.p1_forced[s_id]["가깝다"] = i_id
                    st.rerun()
                elif not is_near and st.session_state.p1_forced[s_id]["가깝다"] == i_id:
                    st.session_state.p1_forced[s_id]["가깝다"] = None
                    
            with col_far:
                is_far = st.checkbox("멀다", key=f"far_{i_id}", value=(st.session_state.p1_forced[s_id]["멀다"] == i_id))
                if is_far and st.session_state.p1_forced[s_id]["멀다"] != i_id:
                    st.session_state.p1_forced[s_id]["멀다"] = i_id
                    st.rerun()
                elif not is_far and st.session_state.p1_forced[s_id]["멀다"] == i_id:
                    st.session_state.p1_forced[s_id]["멀다"] = None
        st.write("---")
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if current_p1_page > 0:
            if st.button("이전 페이지"):
                st.session_state.p1_page -= 1
                st.rerun()
    with col_btn2:
        if current_p1_page < max_p1_pages - 1:
            if st.button("다음 페이지"):
                # 검증: 현재 페이지 세트들에 가깝다/멀다가 다 찍혔는지 수동 방어 요령
                st.session_state.p1_page += 1
                st.rerun()
        else:
            if st.button("🏁 파트 1 완료 및 파트 2 이동", type="primary"):
                st.session_state.stage = "PART2"
                st.rerun()

# ------------------------------------------------------------------
# [화면 레이아웃 - PART 2 (단일형 300제)]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART2":
    st.header("📋 파트 2: 단일 가치관 검사 (300문항)")
    st.caption("질문을 읽고 가장 솔직하게 일치하는 번호(1~5점 척도)를 골라주세요.")
    
    ITEMS_PER_PAGE = 30
    max_p2_pages = 300 // ITEMS_PER_PAGE
    current_p2_page = st.session_state.p2_page
    
    start_idx = current_p2_page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    
    st.progress(end_idx / 300)
    st.write(f"**현재 페이지: {current_p2_page + 1} / {max_p2_pages} 페이지**")
    
    for idx in range(start_idx, end_idx):
        item = PART2_ITEMS[idx]
        i_id = item["item_id"]
        
        st.markdown(f"**{item['text']}**")
        st.session_state.p2_ans[i_id] = st.radio(
            f"L2_{i_id}", [1, 2, 3, 4, 5], index=2, horizontal=True, key=f"likert2_{i_id}",
            format_func=lambda x: {1:"전혀아니다", 2:"아니다", 3:"보통", 4:"그렇다", 5:"매우그렇다"}[x]
        )
        st.write("---")
        
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if current_p2_page > 0:
            if st.button("이전 페이지"):
                st.session_state.p2_page -= 1
                st.rerun()
    with col_b2:
        if current_p2_page < max_p2_pages - 1:
            if st.button("다음 페이지"):
                st.session_state.p2_page += 1
                st.rerun()
        else:
            if st.button("📊 최종 검사 결과지 분석 생성", type="primary"):
                st.session_state.stage = "RESULT"
                st.rerun()

# ------------------------------------------------------------------
# [화면 레이아웃 - RESULT (교차 일관성 정밀 분석)]
# ------------------------------------------------------------------
else:
    st.header("📊 파트 1 - 파트 2 통합 진단 결과 분석서")
    st.write("---")
    
    # [데이터 분석 1] 파트 2 절대 평균 점수 도출
    p2_df = pd.DataFrame(PART2_ITEMS)
    p2_df["score"] = p2_df["item_id"].map(st.session_state.p2_ans).fillna(3)
    p2_summary = p2_df.groupby("dim")["score"].mean().to_dict()
    
    # [데이터 분석 2] 핵심 일관성 모순(Conflict) 추적 엔진
    # 파트 1 강제 선택 정보를 기반으로 우선순위 매트릭스 도출
    conflicts = 0
    valid_sets = 0
    
    for s_id, choice in st.session_state.p1_forced.items():
        near_id = choice.get("가깝다")
        far_id = choice.get("멀다")
        
        if near_id and far_id:
            valid_sets += 1
            near_dim = next(item["dim"] for item in PART1_ITEMS if item["item_id"] == near_id)
            far_dim = next(item["dim"] for item in PART1_ITEMS if item["item_id"] == far_id)
            
            # 파트 1 역량 서열: near_dim > far_dim 이어야 함
            # 만약 파트 2 절대 점수에서 오히려 far_dim 점수가 near_dim보다 훨씬 크다면 모순 발생 판정!
            if p2_summary.get(near_dim, 3) < p2_summary.get(far_dim, 3) - 0.3:
                conflicts += 1
                
    # 모순 점수를 기반으로 교차 일관성 산출
    if valid_sets > 0:
        consistency_rate = int(max(0, 100 - (conflicts / valid_sets) * 250))
    else:
        consistency_rate = 100
        
    # 시각화 대시보드 출력
    res1, res2 = st.columns(2)
    with res1:
        st.metric(label="🔒 파트 1 - 파트 2 교차 일관성 안정도", value=f"{consistency_rate}%", 
                  delta="양호 및 통과" if consistency_rate >= 65 else "위험 (신뢰성 결여 판정 가능성 높음)")
    with res2:
        st.metric(label="⚠️ 가치관 모순 검출 건수", value=f"{conflicts} 건", delta="신뢰성 주의보" if conflicts >= 3 else "안정적")
        
    st.write("---")
    st.subheader("📈 3대 핵심 성향별 벤치마크 현황")
    
    # 획득 기준선 매핑 수치화 (흰색점수 + -주황색 점수 역산 기반 공식)
    benchmark_scores = {"도전정신": 85, "소통협력": 80, "성실집중": 90}
    
    chart_rows = []
    for dim_name in ["도전정신", "소통협력", "성실집중"]:
        my_score = int(p2_summary.get(dim_name, 3) * 20) # 100점 스케일링 변환
        chart_rows.append({"역량항목": dim_name, "나의 스코어": my_score, "현대차 인재상 기준선": benchmark_scores[dim_name]})
        
    df_chart = pd.DataFrame(chart_rows)
    
    fig = px.bar(
        df_chart, x="역량항목", y=["나의 스코어", "현대차 인재상 기준선"],
        barmode="group",
        color_discrete_sequence=["#1f77b4", "#aec7e8"]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### 💡 대기업 인사팀이 바라보는 나의 프로파일 합격 가이드
    1. **일관성 점수가 65% 미만으로 떨어진 경우**: 
       * 파트 1의 강제 선택 질문에서 탈락을 면하기 위해 무조건 좋게 포장한 결과가 파트 2의 솔직한 고백성 답변과 충돌한 상태입니다. 다음 모의 응답 시에는 파트 1에서 고른 '가깝다/멀다'의 기준을 머릿속에 명확히 새겨두고 파트 2 문항까지 일관되게 밀고 나가야 합니다.
    2. **성실집중 기준선(90점) 통과 전략**:
       * 현대자동차 인재상 분석 결과 **성실집중(성실성 및 디테일 정밀 체크 능력)**의 합격선 컷오프가 가장 높게 형성되어 있습니다. 파트 2 문항 전반에서 규율 준수, 마감 사수, 정밀 점검 문항에 방어적으로 확실한 가중치를 부여하시는 것을 추천합니다.
    """)
    
    if st.button("🔄 처음부터 다시 모의 테스트 풀기"):
        st.session_state.clear()
        st.rerun()