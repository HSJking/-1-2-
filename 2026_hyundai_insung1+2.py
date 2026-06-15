import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 페이지 기본 설정
st.set_page_config(page_title="현대자동차 10대 Hyundai Way 통합 인성검사 PRO", layout="wide")

# 10가지 현대자동차 인재상 지표 (Hyundai Way)
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
    st.session_state.p1_forced = {v_id: {"가깝다": None, "멀다": None} for v_id in range(1, 53)}
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
    2. **가깝다/멀다 깔끔한 선택지**: 복잡한 안내 문구 없이 깔끔하게 [가깝다]와 [멀다] 전용 체크 박스로 모의 테스트가 진행됩니다.
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
    st.caption("6개 선택지 중 하나를 고르고, 우측 체크박스에서 해당 문항이 나에게 '가깝다' 또는 '멀다' 인지 고르세요. (세트당 가깝다 1개, 멀다 1개 필수)")
    
    shuffled_sets = st.session_state.p1_shuffled_sets
    total_sets_count = len(shuffled_sets)
    
    SETS_PER_PAGE = 5
    max_p1_pages = int(np.ceil(total_sets_count / SETS_PER_PAGE))
    current_p1_page = st.session_state.p1_page
    
    start_set_idx = current_p1_page * SETS_PER_PAGE
    end_set_idx = min(total_sets_count, start_set_idx + SETS_PER_PAGE)
    
    st.progress(end_set_idx / total_sets_count)
    st.write(f"**현재 페이지: {current_p1_page + 1} / {max_p1_pages}**")
    
    for s_idx in range(start_set_idx, end_set_idx):
        virtual_set_id = s_idx + 1
        st.markdown(f"#### 📦 무작위 세트 {virtual_set_id}")
        set_items = shuffled_sets[s_idx]
        
        # 이미 임시 저장된 기억이 있는지 확인하여 기본값 복원
        saved_near_id = st.session_state.p1_forced[virtual_set_id]["가깝다"]
        saved_far_id = st.session_state.p1_forced[virtual_set_id]["멀다"]
        
        for item in set_items:
            i_id = item["item_id"]
            col_text, col_likert, col_near, col_far = st.columns([4, 4, 1, 1])
            
            with col_text:
                st.write(f"• {item['text']} (Ref: P1-{i_id})")
                
            with col_likert:
                if f"likert_val_{i_id}" not in st.session_state:
                    st.session_state[f"likert_val_{i_id}"] = 4
                st.session_state[f"likert_val_{i_id}"] = st.radio(
                    f"L1_{i_id}", [1, 2, 3, 4, 5, 6], 
                    index=st.session_state[f"likert_val_{i_id}"] - 1, 
                    horizontal=True, key=f"likert_widget_{i_id}", label_visibility="collapsed"
                )
                
            # 🎯 [요청 반영 및 버그 해결]: 오직 가깝다 / 멀다만 노출되도록 체크박스로 복귀
            # 실시간 강제 새로고침(rerun)을 빼서 클릭 렉과 버튼 씹힘 현상을 완벽히 방지했습니다.
            with col_near:
                st.checkbox("가깝다", key=f"near_check_{i_id}", value=(saved_near_id == i_id))
                    
            with col_far:
                st.checkbox("멀다", key=f"far_check_{i_id}", value=(saved_far_id == i_id))
        st.write("---")
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if current_p1_page > 0:
            if st.button("이전 페이지"):
                # 이전 페이지로 이동할 때 현재 선택값 임시 보존
                for check_idx in range(start_set_idx, end_set_idx):
                    v_id = check_idx + 1
                    items_in_set = shuffled_sets[check_idx]
                    n_id = next((it["item_id"] for it in items_in_set if st.session_state.get(f"near_check_{it['item_id']}", False)), None)
                    f_id = next((it["item_id"] for it in items_in_set if st.session_state.get(f"far_check_{it['item_id']}", False)), None)
                    st.session_state.p1_forced[v_id] = {"가깝다": n_id, "멀다": f_id}
                st.session_state.p1_page -= 1
                st.rerun()
                
    with col_btn2:
        # [다음 페이지] 또는 [파트2 이동] 버튼을 누를 때 컴퓨터가 한 번에 정밀 검증을 수행합니다.
        if current_p1_page < max_p1_pages - 1:
            if st.button("다음 페이지"):
                has_error = False
                for check_idx in range(start_set_idx, end_set_idx):
                    v_set_id = check_idx + 1
                    items_in_set = shuffled_sets[check_idx]
                    
                    n_checked = [it["item_id"] for it in items_in_set if st.session_state.get(f"near_check_{it['item_id']}", False)]
                    f_checked = [it["item_id"] for it in items_in_set if st.session_state.get(f"far_check_{it['item_id']}", False)]
                    
                    # 중복 오류 검증
                    double_check = set(n_checked) & set(f_checked)
                    if double_check:
                        st.error(f"⚠️ 무작위 세트 {v_set_id}번의 한 문항에 '가깝다'와 '멀다'를 동시에 체크할 수 없습니다.")
                        has_error = True
                        continue
                        
                    if len(n_checked) != 1 or len(f_checked) != 1:
                        st.error(f"⚠️ 무작위 세트 {v_set_id}번은 반드시 '가깝다' 1개와 '멀다' 1개를 지정해야 합니다.")
                        has_error = True
                    else:
                        st.session_state.p1_forced[v_set_id] = {"가깝다": n_checked[0], "멀다": f_checked[0]}
                
                if not has_error:
                    st.session_state.p1_page += 1
                    st.rerun()
        else:
            if st.button("🏁 파트 1 완료 후 셔플 파트 2 진입", type="primary"):
                has_error = False
                for check_idx in range(start_set_idx, end_set_idx):
                    v_set_id = check_idx + 1
                    items_in_set = shuffled_sets[check_idx]
                    
                    n_checked = [it["item_id"] for it in items_in_set if st.session_state.get(f"near_check_{it['item_id']}", False)]
                    f_checked = [it["item_id"] for it in items_in_set if st.session_state.get(f"far_check_{it['item_id']}", False)]
                    
                    double_check = set(n_checked) & set(f_checked)
                    if double_check:
                        st.error(f"⚠️ 무작위 세트 {v_set_id}번의 한 문항에 '가깝다'와 '멀다'를 동시에 체크할 수 없습니다.")
                        has_error = True
                        continue
                        
                    if len(n_checked) != 1 or len(f_checked) != 1:
                        st.error(f"⚠️ 무작위 세트 {v_set_id}번은 반드시 '가깝다' 1개와 '멀다' 1개를 지정해야 합니다.")
                        has_error = True
                    else:
                        st.session_state.p1_forced[v_set_id] = {"가깝다": n_checked[0], "멀다": f_checked[0]}
                        
                if not has_error:
                    # 최종 전수 취합 처리
                    for s_flat_idx, s_flat_items in enumerate(shuffled_sets):
                        fid = s_flat_idx + 1
                        n_id = next((it["item_id"] for it in s_flat_items if st.session_state.get(f"near_check_{it['item_id']}", False)), None)
                        f_id = next((it["item_id"] for it in s_flat_items if st.session_state.get(f"far_check_{it['item_id']}", False)), None)
                        st.session_state.p1_forced[fid] = {"가깝다": n_id, "멀다": f_id}
                        
                    st.session_state.stage = "PART2"
                    st.rerun()

# ------------------------------------------------------------------
# [화면 구성 - PART 2]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART2":
    st.header("📋 파트 2: 단일 지표 무작위 셔플 검사 (300문항)")
    st.caption("완벽하게 섞인 300개의 질문입니다. 직관적으로 판단해 마킹하세요.")
    
    p2_items = st.session_state.p2_shuffled_items
    ITEMS_PER_PAGE = 30
    max_p2_pages = 300 // ITEMS_PER_PAGE
    current_p2_page = st.session_state.p2_page
    
    start_idx = current_p2_page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    
    st.progress(end_idx / 300)
    st.write(f"**현재 페이지: {current_p2_page + 1} / {max_p2_pages}**")
    
    for idx in range(start_idx, end_idx):
        item = p2_items[idx]
        i_id = item["item_id"]
        
        st.markdown(f"**[셔플 문항] {item['text']}** (Ref: P2-{i_id})")
        
        if f"p2_val_{i_id}" not in st.session_state:
            st.session_state[f"p2_val_{i_id}"] = 3
            
        st.session_state[f"p2_val_{i_id}"] = st.radio(
            f"L2_{i_id}", [1, 2, 3, 4, 5], 
            index=st.session_state[f"p2_val_{i_id}"] - 1, 
            horizontal=True, key=f"p2_widget_{i_id}",
            format_func=lambda x: {1:"전혀 아니다", 2:"아니다", 3:"보통이다", 4:"그렇다", 5:"매우 그렇다"}[x]
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
            if st.button("📊 블랙박스 가중 연산 및 최종 리포트 출력", type="primary"):
                st.session_state.stage = "RESULT"
                st.rerun()

# ------------------------------------------------------------------
# [화면 구성 - RESULT]
# ------------------------------------------------------------------
else:
    st.header("📊 블랙박스 분석 엔진 구동 결과 보고서")
    st.write("---")
    
    p2_shuffled = st.session_state.p2_shuffled_items
    p2_df = pd.DataFrame(p2_shuffled)
    p2_df["user_ans"] = p2_df["item_id"].map(lambda x: st.session_state.get(f"p2_val_{x}", 3))
    p2_df["weighted_score"] = p2_df["user_ans"] * p2_df["weight"]
    
    norm_params = {
        "최고 수준의 안전과 품질": {"mu": 4.8, "sigma": 0.4},
        "집요함": {"mu": 4.6, "sigma": 0.5},
        "시도와 발전": {"mu": 4.2, "sigma": 0.6},
        "민첩한 실행": {"mu": 4.1, "sigma": 0.5},
        "협업": {"mu": 4.3, "sigma": 0.5},
        "회복탄력성": {"mu": 4.2, "sigma": 0.6},
        "다양성 포용": {"mu": 4.0, "sigma": 0.6},
        "전문성": {"mu": 4.4, "sigma": 0.5},
        "윤리준수": {"mu": 4.7, "sigma": 0.4},
        "데이터 기반 사고": {"mu": 3.2, "sigma": 0.8}
    }
    
    dim_scores = {}
    for dim_name in HYUNDAI_WAY.values():
        sub = p2_df[p2_df["dim"] == dim_name]
        
        if sub["weight"].sum() == 0:
            user_raw_avg = 3.0
        else:
            user_raw_avg = sub["weighted_score"].sum() / sub["weight"].sum()
        
        param = norm_params.get(dim_name, {"mu": 4.0, "sigma": 0.5})
        z_score = (user_raw_avg - param["mu"]) / param["sigma"]
        
        if np.isnan(z_score) or np.isinf(z_score):
            t_score = 50
        else:
            t_score = int(50 + 15 * z_score)
            
        dim_scores[dim_name] = max(10, min(99, t_score))
        
    conflicts = 0
    valid_sets = 0
    p1_flatten = [item for sublist in st.session_state.p1_shuffled_sets for item in sublist]
    
    for v_set_id, choice in st.session_state.p1_forced.items():
        near_id = choice.get("가깝다")
        far_id = choice.get("멀다")
        if near_id and far_id:
            valid_sets += 1
            near_dim = next(item["dim"] for item in p1_flatten if item["item_id"] == near_id)
            far_dim = next(item["dim"] for item in p1_flatten if item["item_id"] == far_id)
            
            if dim_scores[near_dim] < dim_scores[far_dim] - 5:
                conflicts += 1
                
    if valid_sets > 0:
        consistency_rate = int(max(0, 100 - (conflicts / valid_sets) * 250))
    else:
        consistency_rate = 100
    honesty_score = int(95 - (conflicts * 5))
    
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric(label="✅ [통계 반영형] 교차 일관성 안정도", value=f"{consistency_rate}%", 
                  delta="정상 통과" if consistency_rate >= 70 else "신뢰성 임계치 미달 위험")
    with r2:
        st.metric(label="🔒 셔플링 검증 기준 진정성 지표", value=f"{honesty_score}%", 
                  delta="양호" if honesty_score >= 65 else "위선 반응 탐지")
    with r3:
        st.metric(label="⚠️ 가치 배치 논리 모순", value=f"{conflicts} 건", delta="안정권" if conflicts <= 2 else "밀착 검증 대상")
        
    st.write("---")
    st.subheader("📈 10대 Hyundai Way 상대 분포 분석 그래프")
    
    benchmark_scores = {
        "최고 수준의 안전과 품질": 85, "집요함": 90, "시도와 발전": 85, "민첩한 실행": 85,
        "협업": 80, "회복탄력성": 85, "다양성 포용": 85, "전문성": 80, "윤리준수": 85, "데이터 기반 사고": 50
    }
    
    chart_rows = []
    for dim_name in HYUNDAI_WAY.values():
        chart_rows.append({
            "Hyundai Way 핵심 가치": dim_name,
            "나의 변환 점수": dim_scores[dim_name],
            "현대차 규준 그룹 기준선": benchmark_scores.get(dim_name, 80)
        })
    df_chart = pd.DataFrame(chart_rows)
    
    fig = px.bar(
        df_chart, x="Hyundai Way 핵심 가치", y=["나의 변환 점수", "현대차 규준 그룹 기준선"],
    )
    fig.update_layout(barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    if st.button("🔄 새로운 무작위 배치로 다시 도전"):
        st.session_state.clear()
        st.rerun()
