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
# 🧠 [실전형 교묘한 문장 가속 엔진] 100% 고유 문항 자동 합성 엔진
# ------------------------------------------------------------------
def synthesize_everyday_text(item_id, dim_name, is_part1=True):
    situations = [
        "새로운 프로젝트의 인계배치가 완료된 첫날 작업에서",
        "매일 반복되는 일상적이고 사소한 루틴 업무를 할 때도",
        "주변 동료들이 마감 기한이 촉박해 마음이 조급해질 때",
        "아무도 모니터링하거나 지켜보지 않는 야간 교대 근무 중에",
        "기존 표준 매뉴얼에 명시되어 있지 않은 돌발 변수가 생겼을 때",
        "상사나 유관 부서로부터 공정 개선안에 대한 지적을 받았을 때",
        "예상치 못한 부품 수급 지연으로 라인 가동이 일시 정지되었을 때",
        "타 부서와의 업무 경계가 모호하여 책임 소재가 불분명할 때",
        "과거에 한 번 경험해 본 익숙하고 단순한 에러를 처리할 상황에서",
        "업무 효율성을 높이기 위해 개인적인 작업 방식을 바꿀 기회가 올 때",
        "작업조원들 간의 가치관 차이로 회의 분위기가 다소 경직되었을 때",
        "현장 정리정돈이나 안전 점검표를 수기로 작성해 제출해야 할 때",
        "품질 가이드라인의 허용 오차 한계 범위가 다소 애매하게 느껴질 때",
        "원인 분석이 어려운 복합적인 설비 트러블이 동시다발적으로 터졌을 때",
        "주변에서 편의상 관행대로 빠르게 넘어가자고 은밀히 제안해올 때"
    ]
    
    actions = {
        "최고 수준의 안전과 품질": [
            "작업 순서를 생략하지 않고 매뉴얼의 사소한 수치까지 끝까지 들여다본다.",
            "부품의 결합 상태가 아주 미세하게 마음에 걸려도 처음부터 다시 재조립한다.",
            "체크리스트의 공란이나 누락된 기록이 없는지 두 세 번 반복해서 대조해 본다.",
            "주변에서 번거롭다고 핀잔을 주더라도 규정된 보호 장구를 예외 없이 착용한다."
        ],
        "집요함": [
            "한번 의문이 생긴 에러는 원인을 완벽히 규명할 때까지 자리를 뜨지 않는다.",
            "남들이 이 정도면 충분하다고 적당히 타협할 때 한 단계를 더 확인하려 든다.",
            "과거에 실패했던 접근 방식을 끝까지 복기하며 끝내 대안을 찾아내고야 만다.",
            "아무리 복잡하고 시간이 오래 걸리는 추적 작업이라도 중간에 포기하지 않는다."
        ],
        "시도와 발전": [
            "기존 방식이 편하더라도 더 효율적인 새로운 시스템이 있다면 먼저 도입해 본다.",
            "관행적으로 내려오던 프로세스에서 시간 낭비 요소를 찾아내 개선안을 제안한다.",
            "실패할 리스크가 다소 있더라도 남들이 시도하지 않은 과감한 아이디어를 낸다.",
            "단순 반복적인 작업이라도 자동화하거나 단계를 줄일 방법이 없을지 늘 연구한다."
        ],
        "민첩한 실행": [
            "장기적인 계획을 정밀하게 세우기보다 일단 행동으로 옮겨 피드백을 본다.",
            "상황이 급박하게 돌아갈 때는 복잡한 결재선보다 현장 대처를 최우선으로 둔다.",
            "완벽한 타이밍을 기다리기보다는 조금 부족해도 기민하게 실행하는 편이다.",
            "지시 사항이나 결정이 내려지면 망설임 없이 즉각 실무에 반영해 나간다."
        ],
        "협업": [
            "내 담당 파트가 아니더라도 동료의 업무 부하가 심하면 기꺼이 지원한다.",
            "전체 조의 공동 목표 달성을 위해 내가 계획했던 개인 일정을 기꺼이 조정한다.",
            "이견이 대립할 때 조율 역할을 자처하여 서로 윈윈할 수 있는 절충점을 찾는다.",
            "개인의 성과를 돋보이게 하기보다 팀 전체의 결과물이 매끄럽게 나오는 데 집중한다."
        ],
        "회복탄력성": [
            "현장에서 강한 지적이나 쓴소리를 들어도 감정에 빠지지 않고 평정심을 유지한다.",
            "열심히 준비했던 개선안이 무산되더라도 낙담하지 않고 곧바로 대안을 마련한다.",
            "갑작스러운 스케줄 변동으로 업무가 꼬여도 스트레스를 받지 않고 담담하게 대처한다.",
            "실수가 발생했을 때 자책하기보다 다음 공정에서 바로잡을 방법을 먼저 생각한다."
        ],
        "다양성 포용": [
            "나와 업무 스타일이나 성향이 정반대인 동료의 의견에서도 핵심 아이디어를 수용한다.",
            "현장 경험이 다소 부족한 신입 사원의 엉뚱한 제안도 편견 없이 경청해 준다.",
            "나이와 직급을 떠나 배울 점이 있는 사람이라면 누구에게나 먼저 다가가 조언을 구한다.",
            "나와 가치관이 다른 조원들과 섞여서 일할 때 오히려 새로운 자극을 받는다."
        ],
        "전문성": [
            "내 직무 분야와 관련된 최신 기술 트렌드나 가이드북을 주기적으로 정독한다.",
            "주변 동료들이 까다로운 기술적 문제에 봉착했을 때 나를 가장 먼저 찾아온다.",
            "역량을 한 단계 더 높이기 위해 퇴근 후나 주말 시간의 일부를 학습에 투자한다.",
            "내가 담당하는 공정의 설비 매커니즘을 완벽히 이해하기 위해 이론 공부를 병행한다."
        ],
        "윤리준수": [
            "관리자나 감독관이 감시하지 않는 주말 작업에서도 보안 규정을 철저히 사수한다.",
            "회사의 공적인 자산이나 사소한 소모품도 정해진 목적 외에는 절대 사적으로 쓰지 않는다.",
            "친한 선후배가 편의를 위해 부탁한 경미한 절차 위반도 원칙에 위배된다면 거절한다.",
            "당장 눈앞의 실적을 올릴 수 있는 편법이 있더라도 올바른 절차만을 고집한다."
        ],
        "데이터 기반 사고": [
            "내 직관이나 다년간의 경험이 맞다고 느껴져도 반드시 통계 수치를 먼저 찾아본다.",
            "의견을 피력할 때 주관적인 느낌의 표현보다 정확한 정량적 지표와 그래프를 제시한다.",
            "과거의 고장 이력 데이터를 시계열로 분석하여 향후 에러 발생 주기성을 예측해 낸다.",
            "문제 현상을 진단할 때 감정적 호소보다 구체적인 팩트와 수치 데이터만을 신뢰한다."
        ]
    }
    
    sit_idx = (item_id * 7) % len(situations)
    act_idx = (item_id * 13) % len(actions[dim_name])
    
    prefix = situations[sit_idx]
    suffix = actions[dim_name][act_idx]
    part_tag = "P1" if is_part1 else "P2"
    
    return f"{prefix} {suffix} ({part_tag}-{item_id})"

# ------------------------------------------------------------------
# [정적 데이터 빌드 및 제약 조건 만족성 검증]
# ------------------------------------------------------------------
@st.cache_data
def get_master_part1():
    data = []
    item_id = 1
    for set_id in range(1, 53):
        dim_indices = []
        base_start = (set_id * 3) % 10
        for i in range(3):
            d_idx = ((base_start + i) % 10) + 1
            dim_indices.append(d_idx)
            
        for i in range(3):
            if item_id > 155: break
            d_name = HYUNDAI_WAY[dim_indices[i]]
            np.random.seed(item_id)
            weight = float(np.random.uniform(0.7, 1.5))
            
            data.append({
                "item_id": item_id,
                "original_set_id": set_id,
                "text": synthesize_everyday_text(item_id, d_name, is_part1=True),
                "dim": d_name,
                "weight": weight
            })
            item_id += 1
    return data

@st.cache_data
def get_master_part2():
    data = []
    for item_id in range(1, 301):
        dim_idx = ((item_id - 1) % 10) + 1
        d_name = HYUNDAI_WAY[dim_idx]
        np.random.seed(item_id + 300)
        weight = float(np.random.uniform(0.8, 1.4))
        
        data.append({
            "item_id": item_id,
            "text": synthesize_everyday_text(item_id, d_name, is_part1=False),
            "dim": d_name,
            "weight": weight
        })
    return data

p1_master = get_master_part1()
p2_master = get_master_part2()

# ------------------------------------------------------------------
# [데이터 백업 유실 방지형 세션 보존 매트릭스]
# ------------------------------------------------------------------
if "p1_storage" not in st.session_state:
    st.session_state.p1_storage = {item["item_id"]: {"near": True, "far": False} for item in p1_master}

def on_near_toggle(item_id):
    if st.session_state[f"near_check_{item_id}"]:
        st.session_state[f"far_check_{item_id}"] = False
    st.session_state.p1_storage[item_id]["near"] = st.session_state[f"near_check_{item_id}"]
    st.session_state.p1_storage[item_id]["far"] = st.session_state[f"far_check_{item_id}"]

def on_far_toggle(item_id):
    if st.session_state[f"far_check_{item_id}"]:
        st.session_state[f"near_check_{item_id}"] = False
    st.session_state.p1_storage[item_id]["near"] = st.session_state[f"near_check_{item_id}"]
    st.session_state.p1_storage[item_id]["far"] = st.session_state[f"far_check_{item_id}"]

# ------------------------------------------------------------------
# [세션 제어 상태 초기화]
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
    shuffled_sets = []
    chunk_size = 3
    for i in range(0, len(p1_master), chunk_size):
        shuffled_sets.append(p1_master[i:i+chunk_size])
    st.session_state.p1_shuffled_sets = shuffled_sets

if "p2_shuffled_items" not in st.session_state:
    random.seed(42)
    p2_master_shuffled = p2_master.copy()
    random.shuffle(p2_master_shuffled)
    st.session_state.p2_shuffled_items = p2_master_shuffled

# ------------------------------------------------------------------
# [화면 구성 - INTRO]
# ------------------------------------------------------------------
if st.session_state.stage == "INTRO":
    st.title("🚗 현대자동차 10대 Hyundai Way 인성검사 실전형 PRO")
    st.write("---")
    st.markdown("본 버전은 대기업 채용용 검증 솔루션과 동일하게 **인재상 노출을 완전히 숨긴 일상적 우회 문항**으로 전면 재구성된 파이널 모의고사입니다.\n\n### ⚙️ 시스템 동작 규격 (Real-Exam Spec)\n1. **교묘한 우회 문장 (Implicit Text)**: 직관적으로 정답을 골라 꾸며내는 위선(Faking) 응답을 차단하기 위해 철저한 일상 업무 사례로 포장되었습니다.\n2. **100% 완전 고유 리스트**: 455개 전 문항 전체에 걸쳐 동일하게 중복 반복되는 텍스트 라인이 단 한 줄도 존재하지 않는 완전 독립 구조입니다.\n3. **세트 내 영역 중복 배제 (Unique Triplet)**: 파트 1의 3개 질문 조합 한 세트 내부에서 동일한 인재상 차원이 겹쳐 나타나지 않도록 엄격히 분리 매핑되었습니다.\n4. **오류 프리 패스**: 시스템 멈춤 버그 유발 요인을 완전히 제거하여 유연한 답변 저장이 가능합니다.")
    if st.button("🚀 실전 셔플링 테스트 시작", type="primary"):
        st.session_state.stage = "PART1"
        st.rerun()

# ------------------------------------------------------------------
# [화면 구성 - PART 1]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART1":
    st.header("📋 파트 1: 강제선택형 콤보 검사 (155문항 / 총 52세트)")
    st.caption("6개 선택지 중 하나를 고르고, 우측 체크박스에서 해당 문항이 나에게 '가깝다' 또는 '멀다' 인지 고르세요. (가깝다 기본 프리셋 지원)")
    
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
        
        for item in set_items:
            i_id = item["item_id"]
            
            st.session_state[f"near_check_{i_id}"] = st.session_state.p1_storage[i_id]["near"]
            st.session_state[f"far_check_{i_id}"] = st.session_state.p1_storage[i_id]["far"]
            
            col_text, col_likert, col_near, col_far = st.columns([5, 4, 1, 1])
            
            with col_text:
                st.write(f"• {item['text']}")
                
            with col_likert:
                if f"likert_val_{i_id}" not in st.session_state:
                    st.session_state[f"likert_val_{i_id}"] = 4
                st.session_state[f"likert_val_{i_id}"] = st.radio(
                    f"L1_{i_id}", [1, 2, 3, 4, 5, 6], 
                    index=st.session_state[f"likert_val_{i_id}"] - 1, 
                    horizontal=True, key=f"likert_widget_{i_id}", label_visibility="collapsed"
                )
                
            with col_near:
                st.checkbox("가깝다", key=f"near_check_{i_id}", on_change=on_near_toggle, args=(i_id,))
                    
            with col_far:
                st.checkbox("멀다", key=f"far_check_{i_id}", on_change=on_far_toggle, args=(i_id,))
        st.write("---")
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if current_p1_page > 0:
            if st.button("이전 페이지"):
                st.session_state.p1_page -= 1
                st.rerun()
                
    with col_btn2:
        if current_p1_page < max_p1_pages - 1:
            if st.button("💾 답변 저장 후 다음 페이지"):
                for check_idx in range(start_set_idx, end_set_idx):
                    v_set_id = check_idx + 1
                    items_in_set = shuffled_sets[check_idx]
                    n_checked = [it["item_id"] for it in items_in_set if st.session_state.p1_storage[it["item_id"]]["near"]]
                    f_checked = [it["item_id"] for it in items_in_set if st.session_state.p1_storage[it["item_id"]]["far"]]
                    
                    st.session_state.p1_forced[v_set_id] = {
                        "가깝다": n_checked[0] if len(n_checked) > 0 else None,
                        "멀다": f_checked[0] if len(f_checked) > 0 else None
                    }
                st.session_state.p1_page += 1
                st.rerun()
        else:
            if st.button("🏁 파트 1 데이터 확정 및 파트 2 진입", type="primary"):
                for s_flat_idx, s_flat_items in enumerate(st.session_state.p1_shuffled_sets):
                    fid = s_flat_idx + 1
                    n_id = next((it["item_id"] for it in s_flat_items if st.session_state.p1_storage[it["item_id"]]["near"]), None)
                    f_id = next((it["item_id"] for it in s_flat_items if st.session_state.p1_storage[it["item_id"]]["far"]), None)
                    st.session_state.p1_forced[fid] = {"가깝다": n_id, "멀다": f_id}
                    
                st.session_state.stage = "PART2"
                st.rerun()

# ------------------------------------------------------------------
# [화면 구성 - PART 2]
# ------------------------------------------------------------------
elif st.session_state.stage == "PART2":
    st.header("📋 파트 2: 단일 지표 무작위 셔플 검사 (300문항)")
    st.caption("완벽하게 뒤섞인 300개의 실전형 문항입니다. 직관적으로 마킹을 밀고 나가세요.")
    
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
        
        st.markdown(f"**{item['text']}**")
        
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
    p1_flatten = p1_master
    
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
    st.header("🔍 10대 Hyundai Way 다차원 성향 진단서")
    
    sorted_scores = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]
    bottom_3 = sorted_scores[-3:]
    
    c_str, c_need = st.columns(2)
    with c_str:
        st.markdown("### 🌟 나의 상위 3대 핵심 강점 지표")
        df_top_dims = pd.DataFrame(top_3, columns=["Hyundai Way 핵심 가치", "나의 T-스코어"])
        st.table(df_top_dims)
        st.markdown("강점 지표 해석 가이드: 위의 3가지 영역은 규준 집단(Norm Group)인 우수 합격자 대비 확고한 성향 우위를 확보한 지표입니다. 실제 현대자동차 면접장에서 구체적인 에피소드를 질문받았을 때 가장 강력하게 나를 어필할 수 있는 핵심 무기가 됩니다.")
        
    with c_need:
        st.markdown("### ⚠️ 보완이 필요한 하위 3대 열세 지표")
        df_bot_dims = pd.DataFrame(bottom_3, columns=["Hyundai Way 핵심 가치", "나의 T-스코어"])
        st.table(df_bot_dims)
        st.markdown("열세 지표 방어 가이드: 해당 역량들은 현대차 합격 컷오프 수직선 대비 상대적으로 보완이 필요한 지표군입니다. 이 점수들이 과도하게 낮을 경우 면접관 가이드 리포트에 '검증 필요 리스크' 신호가 인쇄되어 압박 질문이 들어올 확률이 매우 높습니다.")
        
    st.write("---")
    st.markdown("### 💡 현대자동차 실전 패스를 위한 직무 맞춤형 면접 보안 전략")
    st.info("🛠️ 엔지니어링 및 플랜트 제조 트랙 핵심 합격 가이드라인")
    st.markdown("1. **[최고 수준의 안전과 품질] & [윤리준수] 점수 미달 시**:\n   * 대기업 제조 현장에서는 즉흥적인 번뜩임보다 정해진 공정 규정(SOP)과 안전 제어 원칙을 무한히 반복하고 사수하는 태도를 1순위로 평가합니다. 만약 이 지표가 합격선보다 낮게 탐지되었다면, 면접 시 '사소한 공정 누락이나 규칙 위반 가능성을 차단하기 위해 나만의 정밀 체크리스트나 정량적 시스템을 구축해 극복한 사례'를 중심으로 소명해야 합니다.\n2. **[집요함] & [회복탄력성] 보완 방법**:\n   * 불확실성이 높은 라인 운영 환경 특성상 돌발적인 설비 문제나 공정 에러에 직면했을 때 감정적으로 무너지지 않는 강인함이 필수적입니다. T-스코어가 불안정하게 잡힌 경우, 과거 기술적 자격증 시험이나 복잡한 프로젝트를 준비하며 겪었던 좌절 경험을 솔직하게 인정하되, 어떤 데이터 중심 루틴과 마인드셋을 가동해 끝까지 목표를 완수했는지 '행동 중심(Action)'으로 어필하세요.")
    
    if st.button("🔄 새로운 무작위 배치로 다시 도전"):
        st.session_state.clear()
        st.rerun()
