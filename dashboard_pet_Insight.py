import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="펫고객관리시스템",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 설정
st.sidebar.title("🐾펫고객관리시스템")
st.sidebar.markdown("---")

# 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["📊 대시보드", "🎯 개인 고객 분석", "📈 주기상향 추천", "💰 수익 예측"]
)

# 펫 크기 및 연령대 추정 함수
def estimate_pet_profile(pet_categories, pet_spend):
    """펫 카테고리와 지출액으로 반려동물 크기/연령 추정"""
    profiles = []
    
    categories = pet_categories.split(', ')
    for category in categories:
        if 'DOG-' in category:
            # 강아지 크기 추정 (지출액 기준)
            if pet_spend < 30:
                profiles.append("소형견")
            elif pet_spend < 80:
                profiles.append("중형견") 
            else:
                profiles.append("대형견")
        elif 'CAT-' in category:
            # 고양이 연령대 추정 (카테고리 기준)
            if '간식' in category or '장난감' in category:
                profiles.append(np.random.choice(["새끼고양이", "성묘"], p=[0.3, 0.7]))
            else:
                profiles.append("성묘")
    
    return list(set(profiles)) if profiles else ["미확인"]

def estimate_household_size(total_spend):
    """총 지출액으로 가구수 추정"""
    if total_spend < 2000:
        return "1인 가구"
    elif total_spend < 4000:
        return "2인 가구"
    elif total_spend < 6000:
        return "3인 가구"
    else:
        return "4인 이상 가구"

def get_pet_recommendations(pet_categories):
    """카테고리 기반 펫 제품 추천"""
    recommendations = []
    categories = pet_categories.split(', ')
    
    for category in categories:
        if 'DOG-사료/간식' in category:
            recommendations.extend([
                "프리미엄 건식사료 (대용량)",
                "기능성 간식 (관절/치아 건강)",
                "습식사료 (토핑용)",
                "수제 간식"
            ])
        elif 'CAT-사료/간식' in category:
            recommendations.extend([
                "연령별 맞춤 사료",
                "헤어볼 케어 간식",
                "동결건조 간식",
                "습식 파우치 (멀티팩)"
            ])
        elif 'CAT-모래/위생용품' in category:
            recommendations.extend([
                "응고형 벤토나이트 모래",
                "무향 두부모래",
                "자동급식기/급수기",
                "고양이 화장실 매트"
            ])
        elif 'DOG-건강관리/영양제' in category:
            recommendations.extend([
                "종합 영양제",
                "관절 건강 보조제",
                "피부/모질 개선제",
                "유산균 보조제"
            ])
    
    return list(set(recommendations))[:6]  # 중복 제거 후 상위 6개

def get_related_products(pet_categories, total_spend):
    """연관 일반 제품 추천"""
    base_products = [
        "키친타올 (대용량)",
        "물티슈 (무알코올)",
        "공기청정기 필터",
        "진공청소기 먼지봉투",
        "세탁세제 (저자극)",
        "바닥 청소용품"
    ]
    
    if total_spend > 5000:  # 고지출 고객
        base_products.extend([
            "프리미엄 공기청정기",
            "로봇청소기",
            "고급 세탁세제",
            "친환경 청소용품"
        ])
    
    if 'DOG-' in pet_categories:
        base_products.extend([
            "운동화 (산책용)",
            "아웃도어 재킷",
            "휴대용 물병",
            "차량용 시트커버"
        ])
    
    return base_products[:8]

# 샘플 데이터 생성 (실제 사용 시에는 업로드된 파일에서 읽어옴)
@st.cache_data
def load_sample_data():
    # 펫 고객 데이터 샘플 (실제 분포에 맞춤)
    np.random.seed(42)
    
    # 실제 데이터 분포에 맞게 고객 생성 (초고빈도 포함)
    frequency_distribution = {
        '초고빈도': 297,      # 7+ transactions per month
        '주간구매': 266,    # 5-6 transactions per month
        '월간구매': 237,    # 1-2 transactions per month  
        '고빈도': 139,      # 4 transactions per month
        '저빈도': 98,       # 3 transactions per month
        '한달이상': 87,     # <1 transaction per month
    }
    
    customer_count = sum(frequency_distribution.values())  # 1124명
    
    # 각 빈도별로 고객 생성
    household_keys = []
    pet_transactions = []
    
    customer_id = 1000
    for freq_type, count in frequency_distribution.items():
        for _ in range(count):
            household_keys.append(customer_id)
            customer_id += 1
            
            # 빈도별 거래 횟수 할당
            if freq_type == '한달이상':
                pet_transactions.append(np.random.choice([0.5, 0.7, 0.9]))
            elif freq_type == '월간구매':
                pet_transactions.append(np.random.choice([1, 2]))
            elif freq_type == '저빈도':
                pet_transactions.append(3)
            elif freq_type == '고빈도':
                pet_transactions.append(4)
            elif freq_type == '주간구매':
                pet_transactions.append(np.random.choice([5, 6]))
            elif freq_type == '초고빈도':
                pet_transactions.append(np.random.choice([7, 8, 9, 10]))
    
    # 데이터를 섞어서 랜덤화
    combined_data = list(zip(household_keys, pet_transactions))
    np.random.shuffle(combined_data)
    household_keys, pet_transactions = zip(*combined_data)
    
    pet_spend = np.random.uniform(10, 200, customer_count).round(2)
    total_spend = np.random.uniform(500, 8000, customer_count).round(2)
    pet_ratio = (pet_spend / total_spend * 100).round(2)
    club_plus_member = np.random.choice([True, False], customer_count, p=[0.3, 0.7])
    
    # 펫 카테고리를 소분류까지 세분화
    pet_categories_detailed = [
        'DOG-사료/간식, CAT-모래/위생용품', 
        'DOG-장난감/액세서리, CAT-사료/간식',
        'DOG-사료/간식', 
        'CAT-사료/간식, OTHER-가금류용 사료 및 용품',
        'DOG-건강관리/영양제, CAT-장난감/액세서리',
        'CAT-모래/위생용품',
        'DOG-사료/간식, OTHER-물고기/어항용품',
        'DOG-장난감/액세서리',
        'CAT-사료/간식',
        'DOG-건강관리/영양제, CAT-건강관리/영양제, OTHER-햄스터/소동물용품',
        'DOG-사료/간식, CAT-사료/간식, OTHER-가금류용 사료 및 용품',
        'DOG-목줄/하네스/이동장',
        'CAT-모래/위생용품, OTHER-물고기/어항용품',
        'DOG-장난감/액세서리, CAT-모래/위생용품',
        'DOG-사료/간식, CAT-장난감/액세서리',
        'OTHER-파충류 용품',
        'DOG-건강관리/영양제',
        'CAT-건강관리/영양제',
        'DOG-목줄/하네스/이동장, CAT-사료/간식',
        'DOG-사료/간식, OTHER-가금류용 사료 및 용품'
    ]
    
    pet_categories = []
    household_sizes = []
    pet_profiles = []
    
    for i in range(customer_count):
        # 각 고객별로 1-3개의 카테고리를 랜덤 선택
        num_categories = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        selected_categories = np.random.choice(pet_categories_detailed, num_categories, replace=False)
        category_str = ', '.join(selected_categories)
        pet_categories.append(category_str)
        
        # 가구수 추정
        household_sizes.append(estimate_household_size(total_spend[i]))
        
        # 펫 프로필 추정
        pet_profiles.append(', '.join(estimate_pet_profile(category_str, pet_spend[i])))
    
    pet_customers = pd.DataFrame({
        'household_key': household_keys,
        'pet_transactions': pet_transactions,
        'pet_spend': pet_spend,
        'total_spend': total_spend,
        'pet_ratio': pet_ratio,
        'pet_categories': pet_categories,
        'household_size': household_sizes,
        'pet_profile': pet_profiles,
        'club_plus_member': club_plus_member,
        'last_purchase_days': np.random.randint(1, 90, customer_count),
        'phone_number': [f"010-{np.random.randint(1000,9999)}-{np.random.randint(1000,9999)}" for _ in range(customer_count)]
    })
    
    # 주기상향 변화 데이터 샘플
    frequency_changes = pd.DataFrame({
        'category': ['BEEF', 'SOFT DRINKS', 'FRZN MEAT/MEAT DINNERS', 'FROZEN PIZZA', 'CHEESE', 'FLUID MILK PRODUCTS', 'BAG SNACKS', 'BAKED BREAD/BUNS/ROLLS', 'PORK', 'CIGARETTES'],
        'current_sales': [184.72, 274.54, 196.84, 150.69, 199.55, 220.49, 153.78, 179.73, 86.68, 153.59],
        'target_sales': [1940.09, 1969.7, 1530.81, 1300.7, 1174.74, 1050.29, 936.82, 913.67, 806.5, 775.44],
        'sales_change': [1755.37, 1695.16, 1333.97, 1150.01, 975.19, 829.8, 783.04, 733.94, 719.82, 621.85],
        'percentage_change': [950.29, 617.45, 677.69, 763.16, 488.69, 376.34, 509.19, 408.36, 830.43, 404.88]
    })
    
    # 제품 데이터 샘플
    products = pd.DataFrame({
        'product_id': [25671, 26081, 26093, 26190, 26355, 26426, 26540, 26601, 26636, 26700],
        'major_category': ['GROCERY', 'MISC. TRANS.', 'PASTRY', 'GROCERY', 'GROCERY', 'GROCERY', 'GROCERY', 'DRUG GM', 'PASTRY', 'MEAT'],
        'middle_category': ['FRZN ICE', 'NO COMMODITY DESCRIPTION', 'BREAD', 'FRUIT - SHELF STABLE', 'COOKIES/CONES', 'SPICES & EXTRACTS', 'COOKIES/CONES', 'VITAMINS', 'BREAKFAST SWEETS', 'BEEF'],
        'small_category': ['ICE - CRUSHED/CUBED', 'NO SUBCOMMODITY DESCRIPTION', 'BREAD:ITALIAN/FRENCH', 'APPLE SAUCE', 'SPECIALTY COOKIES', 'SPICES & SEASONINGS', 'TRAY PACK/CHOC CHIP COOKIES', 'VITAMIN - MINERALS', 'SW GDS: SW ROLLS/DAN', 'SELECT BEEF'],
        'total_quantity': [6, 1, 1, 1, 2, 1, 3, 1, 1, 5],
        'total_revenue': [20.94, 0.99, 1.59, 1.54, 1.98, 2.29, 2.79, 7.59, 2.5, 45.67]
    })
    
    return pet_customers, frequency_changes, products

pet_customers, frequency_changes, products = load_sample_data()

# 고객 구매 빈도 분류 함수
def classify_frequency(monthly_transactions):
    if monthly_transactions < 1:
        return "한달이상"
    elif monthly_transactions <= 2:
        return "월간구매"
    elif monthly_transactions == 3:
        return "저빈도"
    elif monthly_transactions == 4:
        return "고빈도"
    elif monthly_transactions <= 6:
        return "주간구매"
    else:
        return "초고빈도"

# 고객별 인사이트 생성 함수
def generate_customer_insights(customer_data, target_customers):
    insights = []
    marketing_tips = []
    
    # 펫 지출 비율 분석
    avg_pet_ratio = target_customers['pet_ratio'].mean()
    if customer_data['pet_ratio'] < avg_pet_ratio * 0.8:
        insights.append(f"고객 {customer_data['household_key']}는 **전체적으로 펫 관련 소비 비중이 낮은 편**입니다.")
        marketing_tips.append("🎯 **펫 관련 프로모션 타겟**: 현재는 관심은 있지만 지출이 낮은 고객 → 할인이나 번들 제안으로 지출 유도 가능.")
    elif customer_data['pet_ratio'] > avg_pet_ratio * 1.2:
        insights.append(f"고객 {customer_data['household_key']}는 **펫 관련 소비 비중이 매우 높은 편**입니다.")
        marketing_tips.append("🌟 **VIP 펫 고객 관리**: 고가치 펫 고객으로 프리미엄 서비스 및 신상품 우선 제안 가능.")
    
    # 구매 빈도 분석
    frequency = classify_frequency(customer_data['pet_transactions'])
    if frequency == "주간구매":
        insights.append("주간으로 꾸준히 구매를 하지만, **펫 관련 상품에는 비교적 적은 비용을 지출**합니다.")
        marketing_tips.append("⏱️ **빈도 기반 추천**: 주간 구매자이므로, 펫 관련 **정기배송 제안**이나 **구독형 서비스** 유도 가능.")
    elif frequency == "월간구매":
        insights.append("월간 단위로 구매하는 **안정적인 구매 패턴**을 보입니다.")
        marketing_tips.append("📅 **정기 구매 유도**: 월간 구매 패턴을 활용한 정기배송 할인 혜택 제안.")
    elif frequency == "고빈도":
        insights.append("**고빈도로 펫 제품을 구매**하는 충성도 높은 고객입니다.")
        marketing_tips.append("💎 **로열티 강화**: 고빈도 구매 고객으로 VIP 혜택 및 리워드 프로그램 제안.")
    elif frequency == "초고빈도":
        insights.append("**최고 빈도로 펫 제품을 구매**하는 VIP 고객입니다.")
        marketing_tips.append("👑 **VIP 고객 관리**: 초고빈도 고객으로 프리미엄 서비스, 얼리액세스, 개인 컨시어지 서비스 제공.")
    
    # 지출 패턴 분석
    avg_pet_spend = target_customers['pet_spend'].mean()
    if customer_data['pet_spend'] < avg_pet_spend * 0.7:
        insights.append("**단가가 낮거나 빈도가 적은 구매 패턴**으로 보입니다.")
        marketing_tips.append("💰 **단가 상승 전략**: 프리미엄 제품 체험 기회 제공 및 번들 상품 추천.")
    elif customer_data['pet_spend'] > avg_pet_spend * 1.3:
        insights.append("**높은 금액대의 펫 제품을 구매**하는 프리미엄 고객입니다.")
        marketing_tips.append("🏆 **프리미엄 서비스**: 고가 상품 선호 고객으로 신상품 런칭 시 우선 안내.")
    
    # 카테고리 다양성 분석
    categories = customer_data['pet_categories'].split(', ')
    unique_main_categories = set()
    for cat in categories:
        if '-' in cat:
            main_cat = cat.split('-')[0]
            unique_main_categories.add(main_cat)
    
    if len(unique_main_categories) >= 3:
        insights.append(f"다양한 펫 카테고리({', '.join(unique_main_categories)})에 관심이 있는 **종합적인 펫 케어** 고객입니다.")
        marketing_tips.append("🔍 **카테고리 맞춤 리타게팅**: 다양한 카테고리 구매로 고객 맞춤형 크로스셀링 기회 높음.")
    elif len(unique_main_categories) == 2:
        insights.append(f"주로 {', '.join(unique_main_categories)} 카테고리에 집중된 **특화된 관심사**를 보입니다.")
        marketing_tips.append("🎯 **전문화 전략**: 특정 카테고리 전문가로 해당 분야 신상품 및 전문 서비스 제안.")
    else:
        insights.append(f"{list(unique_main_categories)[0]} 카테고리에 **집중된 구매 패턴**을 보입니다.")
        marketing_tips.append("📈 **카테고리 확장**: 현재 관심 카테고리에서 연관 상품으로 구매 범위 확대 유도.")
    
    # Club+ 회원 여부 분석
    if customer_data['club_plus_member']:
        insights.append("**Club+ 회원**으로 브랜드 충성도가 높은 우수 고객입니다.")
        marketing_tips.append("🌟 **멤버십 혜택 활용**: Club+ 전용 이벤트 및 얼리버드 혜택으로 만족도 증대.")
    else:
        marketing_tips.append("💳 **Club+ 가입 유도**: 현재 구매 패턴 기반으로 멤버십 가입 혜택 어필.")
    
    # 최근 구매일 분석
    if customer_data['last_purchase_days'] > 30:
        insights.append(f"마지막 구매가 **{customer_data['last_purchase_days']}일 전**으로 재방문 유도가 필요합니다.")
        marketing_tips.append("🔔 **재방문 유도**: 개인화된 할인 쿠폰 및 리마인드 푸쉬로 재방문 촉진.")
    
    return insights, marketing_tips

# 전화번호 마스킹 함수
def mask_phone_number(phone_number):
    """전화번호 뒷자리 4자리를 ****로 마스킹"""
    if len(phone_number) >= 4:
        return phone_number[:-4] + "****"
    return phone_number

# 대시보드 페이지
if menu == "📊 대시보드":
    st.title("🐾Dashboard")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 펫 고객 수", f"{len(pet_customers):,}명")
    
    with col2:
        total_pet_spend = pet_customers['pet_spend'].sum()
        st.metric("펫 제품 총 매출", f"£{total_pet_spend:,.2f}")
    
    with col3:
        avg_pet_spend = pet_customers['pet_spend'].mean()
        st.metric("평균 펫 지출", f"£{avg_pet_spend:.2f}")
    
    with col4:
        upgrade_candidates = pet_customers[
            pet_customers['frequency_category'].isin(['저빈도', '월간구매', '한달이상'])
        ] if 'frequency_category' in pet_customers.columns else pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency).isin(['저빈도', '월간구매', '한달이상'])
        ]
        
        potential_total_revenue = upgrade_candidates['total_spend'].sum() * 0.15
        st.metric("상향이동 잠재 수익", f"£{potential_total_revenue:,.2f}")
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 고객 구매 빈도 분포")
        
        pet_customers['frequency_category'] = pet_customers['pet_transactions'].apply(classify_frequency)
        frequency_counts = pet_customers['frequency_category'].value_counts()
        
        frequency_order = ['초고빈도', '주간구매', '월간구매', '고빈도', '저빈도', '한달이상']
        
        chart_data = pd.DataFrame({
            '고객수': [frequency_counts.get(cat, 0) for cat in frequency_order]
        }, index=frequency_order)
        
        st.bar_chart(chart_data)
        
        frequency_descriptions = {
            '초고빈도': '0-4일 간격 (월 7회 이상)',
            '주간구매': '5-7일 간격 (월 4-6회)',
            '월간구매': '14-30일 간격 (월 1-2회)',
            '고빈도': '8-10일 간격 (월 3-4회)',
            '저빈도': '11-13일 간격 (월 2-3회)',
            '한달이상': '30일+ 간격 (월 1회 미만)'
        }
        
        for category in frequency_order:
            if category in frequency_counts:
                count = frequency_counts[category]
                percentage = count / len(pet_customers) * 100
                description = frequency_descriptions[category]
                st.write(f"• **{category}** ({description}): {count}명 ({percentage:.1f}%)")
    
    with col2:
        st.subheader("💰 펫고객별 총매출 순위")
        
        spend_analysis_sorted = pet_customers[['household_key', 'pet_spend', 'total_spend', 'frequency_category']].sort_values('total_spend', ascending=False) 
        st.dataframe(spend_analysis_sorted.head(10))
        
        top_customer = pet_customers.loc[pet_customers['total_spend'].idxmax()]
        avg_total_spend = pet_customers['total_spend'].mean()
        st.write(f"👑 **최고 매출 고객**: 고객 {top_customer['household_key']} (£{top_customer['total_spend']:,.2f})")
        st.write(f"📊 **평균 총 매출**: £{avg_total_spend:,.2f}")        
        
    # 주기상향 기회 분석
    st.subheader("🎯 주기상향 기회 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("카테고리별 상향 잠재력")
        
        top_categories = frequency_changes.head(8)
        chart_data = top_categories[['category', 'percentage_change']].set_index('category')
        st.bar_chart(chart_data)
        
        for _, row in top_categories.iterrows():
            st.write(f"• **{row['category']}**: {row['percentage_change']:.1f}% 증가 (£{row['sales_change']:.2f})")
    
    with col2:
        st.subheader("상향 대상 고객 식별")
        
        upgrade_candidates = pet_customers[
            pet_customers['frequency_category'].isin(['저빈도', '월간구매', '한달이상'])
        ]
        
        st.write(f"**상향 대상 고객**: {len(upgrade_candidates)}명")
        st.write(f"**평균 펫 지출**: £{upgrade_candidates['pet_spend'].mean():.2f}")
        st.write(f"**평균 총 지출**: £{upgrade_candidates['total_spend'].mean():.2f}")
        st.write(f"**Club+ 회원**: {upgrade_candidates['club_plus_member'].sum()}명")
        
        bins = [0, 25, 50, 100, 200]
        labels = ['£0-25', '£25-50', '£50-100', '£100+']
        upgrade_candidates['spend_range'] = pd.cut(upgrade_candidates['pet_spend'], bins=bins, labels=labels, include_lowest=True)
        spend_dist = upgrade_candidates['spend_range'].value_counts()
        
        for range_label, count in spend_dist.items():
            st.write(f"• **{range_label}**: {count}명")

# 개인 고객 분석 페이지
elif menu == "🎯 개인 고객 분석":
    st.title("🎯 개인 고객 분석")
    
    # 고객 선택
    selected_customer = st.selectbox(
        "분석할 고객을 선택하세요:",
        pet_customers['household_key'].tolist(),
        format_func=lambda x: f"고객 ID: {x}"
    )
    
    # 선택된 고객 정보
    customer_data = pet_customers[pet_customers['household_key'] == selected_customer].iloc[0]
    
    st.subheader(f"고객 {selected_customer} 상세 분석")
    
    # 기본 지표 (5개 컬럼으로 확장)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("펫 거래 횟수", f"{customer_data['pet_transactions']}회")
    
    with col2:
        st.metric("펫 지출 금액", f"£{customer_data['pet_spend']:.2f}")
    
    with col3:
        st.metric("총 지출 금액", f"£{customer_data['total_spend']:.2f}")
    
    with col4:
        st.metric("펫 지출 비율", f"{customer_data['pet_ratio']:.1f}%")
    
    with col5:
        club_status = "🌟 Club+" if customer_data['club_plus_member'] else "📱 일반"
        st.metric("회원 등급", club_status)
    
    # 추가 고객 정보 (3개 섹션으로 정리)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"🏠 **예상 가구수**: {customer_data['household_size']}")
        st.info(f"📱 **연락처**: {mask_phone_number(customer_data['phone_number'])}")
    
    with col2:
        st.info(f"🐾 **반려동물 유형**: {customer_data['pet_profile']}")
        st.info(f"🛒 **마지막 구매**: {customer_data['last_purchase_days']}일 전")
    
    with col3:
        current_frequency = classify_frequency(customer_data['pet_transactions'])
        st.info(f"⏰ **현재 구매 빈도**: {current_frequency}")
    
    # 구매 카테고리 (개선된 시각화)
    st.subheader("🛍️ 구매 펫 카테고리")
    categories = customer_data['pet_categories'].split(', ')
    
    category_cols = st.columns(min(len(categories), 3))
    for idx, category in enumerate(categories):
        col_idx = idx % 3
        with category_cols[col_idx]:
            if '-' in category:
                main_cat, sub_cat = category.split('-', 1)
                st.write(f"**{main_cat}**")
                st.write(f"└ {sub_cat}")
            else:
                st.write(f"**{category}**")
    
    # 동일 빈도 그룹 내 비교 (총매출 추가)
    st.subheader("📊 동일 빈도 그룹 내 비교")
    
    same_frequency_customers = pet_customers[
        pet_customers['pet_transactions'].apply(classify_frequency) == current_frequency
    ]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📈 펫 지출 분포**")
        pet_spend_stats = same_frequency_customers['pet_spend'].describe()
        for stat, value in pet_spend_stats.items():
            if stat in ['mean', 'std', 'min', 'max']:
                st.write(f"• {stat}: £{value:.2f}")
        
        current_rank = (same_frequency_customers['pet_spend'] < customer_data['pet_spend']).sum() + 1
        st.write(f"**현재 고객 순위**: {current_rank}/{len(same_frequency_customers)}위")
    
    with col2:
        st.write("**💰 총 지출 분포**")
        total_spend_stats = same_frequency_customers['total_spend'].describe()
        for stat, value in total_spend_stats.items():
            if stat in ['mean', 'std', 'min', 'max']:
                st.write(f"• {stat}: £{value:.2f}")
        
        total_rank = (same_frequency_customers['total_spend'] < customer_data['total_spend']).sum() + 1
        st.write(f"**현재 고객 순위**: {total_rank}/{len(same_frequency_customers)}위")
    
    with col3:
        st.write("**📊 펫 지출 비율 분포**")
        ratio_stats = same_frequency_customers['pet_ratio'].describe()
        for stat, value in ratio_stats.items():
            if stat in ['mean', 'std', 'min', 'max']:
                st.write(f"• {stat}: {value:.2f}%")
        
        ratio_rank = (same_frequency_customers['pet_ratio'] < customer_data['pet_ratio']).sum() + 1
        st.write(f"**현재 고객 순위**: {ratio_rank}/{len(same_frequency_customers)}위")
    
    # 추천 섹션
    st.markdown("---")
    st.subheader("💡 맞춤형 추천")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🐾 함께 구매 펫 추천")
        pet_recommendations = get_pet_recommendations(customer_data['pet_categories'])
        
        for i, recommendation in enumerate(pet_recommendations, 1):
            st.write(f"{i}. **{recommendation}**")
            if i <= 3:  # 상위 3개는 별표 추가
                st.write("   ⭐ 고객님께 특히 추천!")
        
        # 추천 이유
        with st.expander("💡 추천 이유"):
            if 'DOG-사료/간식' in customer_data['pet_categories']:
                st.write("• 기존 강아지 사료 구매 이력 기반 추천")
                st.write("• 프리미엄 라인업으로 업그레이드 제안")
            if 'CAT-' in customer_data['pet_categories']:
                st.write("• 고양이 전용 제품군 확대 추천")
                st.write("• 건강 관리 특화 제품 우선 추천")
    
    with col2:
        st.markdown("### 🛒 함께 구매 연관 제품")
        related_products = get_related_products(customer_data['pet_categories'], customer_data['total_spend'])
        
        for i, product in enumerate(related_products, 1):
            st.write(f"{i}. **{product}**")
            if customer_data['total_spend'] > 5000 and i <= 2:
                st.write("   💎 프리미엄 고객 맞춤 추천")
        
        # 연관성 설명
        with st.expander("🔗 연관성 분석"):
            st.write("• **청소용품**: 반려동물로 인한 청소 필요성 증가")
            st.write("• **위생용품**: 펫 케어와 연관된 생활용품")
            if customer_data['household_size'] != "1인 가구":
                st.write(f"• **가족용품**: {customer_data['household_size']} 맞춤 제품")
            if 'DOG-' in customer_data['pet_categories']:
                st.write("• **아웃도어 용품**: 강아지 산책 관련 제품")

# 주기상향 추천 페이지 (기존 코드 유지)
elif menu == "📈 주기상향 추천":
    st.title("📈 주기상향 추천")
    
    upgrade_path = st.selectbox(
        "상향 경로를 선택하세요:",
        [
            "주간구매 (5-7일) → 초고빈도 (0-4일)",
            "월간구매 (14-30일) → 저빈도 (11-13일)",
            "고빈도 (8-10일) → 주간구매 (5-7일)",
            "저빈도 (11-13일) → 고빈도 (8-10일)",
            "한달이상 (30일+) → 월간구매 (14-30일)",
            "초고빈도 유지 (0-4일) - VIP 관리"
        ]
    )
    
    st.subheader(f"🎯 {upgrade_path} 추천 전략")
    
    if "주간구매 (5-7일) → 초고빈도 (0-4일)" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "주간구매"
        ]
    elif "월간구매 (14-30일) → 저빈도 (11-13일)" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "월간구매"
        ]
    elif "고빈도 (8-10일) → 주간구매 (5-7일)" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "고빈도"
        ]
    elif "저빈도 (11-13일) → 고빈도 (8-10일)" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "저빈도"
        ]
    elif "한달이상 (30일+) → 월간구매 (14-30일)" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "한달이상"
        ]
    else:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "초고빈도"
        ]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 대상 고객 정보")
        st.metric("대상 고객 수", f"{len(target_customers)}명")
        if len(target_customers) > 0:
            st.metric("평균 펫 지출", f"£{target_customers['pet_spend'].mean():.2f}")
            st.metric("평균 총 지출", f"£{target_customers['total_spend'].mean():.2f}")
            club_plus_count = target_customers['club_plus_member'].sum()
            st.metric("Club+ 회원", f"{club_plus_count}명 ({club_plus_count/len(target_customers)*100:.1f}%)")
    
    with col2:
        st.subheader("🛒 추천 제품/카테고리")
        top_categories = frequency_changes.head(6)
        
        for idx, category in top_categories.iterrows():
            col_cat1, col_cat2, col_cat3 = st.columns([2, 1, 1])
            
            with col_cat1:
                st.write(f"**{category['category']}**")
            
            with col_cat2:
                st.metric("예상 매출 증가", f"£{category['sales_change']:.2f}")
            
            with col_cat3:
                st.metric("증가율", f"{category['percentage_change']:.1f}%")
            
            progress = min(category['percentage_change'] / 1000, 1.0)
            st.progress(progress)
            st.markdown("---")

# 수익 예측 페이지 (기존 코드 유지)
elif menu == "💰 수익 예측":
    st.title("💰 수익 예측 분석")
    
    st.subheader("📈 주기상향 시나리오별 수익 예측")
    
    col1, col2 = st.columns(2)
    
    with col1:
        conversion_rate = st.slider(
            "전환율 (%)",
            min_value=1,
            max_value=50,
            value=15,
            help="선택된 고객 중 실제 상향되는 비율"
        )
    
    with col2:
        target_months = st.slider(
            "목표 기간 (월)",
            min_value=1,
            max_value=12,
            value=6,
            help="상향 효과를 측정할 기간"
        )
    
    scenarios = [
        {
            'name': '주간구매 → 초고빈도',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "주간구매"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "주간구매"]['total_spend'].mean(),
            'increase_multiplier': 1.5
        },
        {
            'name': '월간구매 → 저빈도',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "월간구매"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "월간구매"]['total_spend'].mean(),
            'increase_multiplier': 1.1
        },
        {
            'name': '고빈도 → 주간구매',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "고빈도"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "고빈도"]['total_spend'].mean(),
            'increase_multiplier': 1.3
        },
        {
            'name': '저빈도 → 고빈도',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "저빈도"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "저빈도"]['total_spend'].mean(),
            'increase_multiplier': 1.2
        },
        {
            'name': '한달이상 → 월간구매',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "한달이상"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "한달이상"]['total_spend'].mean(),
            'increase_multiplier': 1.0
        },
        {
            'name': '초고빈도 VIP 유지',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "초고빈도"]),
            'avg_total_spend': pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "초고빈도"]['total_spend'].mean(),
            'increase_multiplier': 2.0
        }
    ]
    
    total_projected_revenue = 0
    scenario_results = []
    
    for scenario in scenarios:
        converted_customers = scenario['target_count'] * (conversion_rate / 100)
        monthly_increase_per_customer = scenario['avg_total_spend'] * (scenario['increase_multiplier'] - 1) / 12
        monthly_increase = converted_customers * monthly_increase_per_customer
        total_increase = monthly_increase * target_months
        total_projected_revenue += total_increase
        
        scenario_results.append({
            'scenario': scenario['name'],
            'target_customers': scenario['target_count'],
            'converted_customers': int(converted_customers),
            'avg_total_spend': scenario['avg_total_spend'],
            'monthly_revenue_increase': monthly_increase,
            'total_revenue_increase': total_increase
        })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 예상 수익 증가", f"£{total_projected_revenue:,.2f}")
    
    with col2:
        total_converted = sum([r['converted_customers'] for r in scenario_results])
        st.metric("총 전환 예상 고객", f"{total_converted}명")
    
    with col3:
        monthly_avg = total_projected_revenue / target_months
        st.metric("월평균 수익 증가", f"£{monthly_avg:,.2f}")
    
    st.subheader("📋 시나리오별 상세 예측")
    
    results_df = pd.DataFrame(scenario_results)
    st.dataframe(results_df)
    
    best_scenario = max(scenario_results, key=lambda x: x['total_revenue_increase'])
    
    insights = [
        f"📊 **최고 수익 시나리오**: {best_scenario['scenario']} - £{best_scenario['total_revenue_increase']:,.2f}",
        f"🎯 **전환율 1% 증가 시**: 추가 £{(total_projected_revenue * 0.01 / (conversion_rate / 100)):,.2f} 수익 기대",
        f"⏰ **목표 기간 연장 시**: 12개월 기준 £{(total_projected_revenue * 12 / target_months):,.2f} 수익 가능",
        f"🔄 **지속적 상향 시**: 고객 생애가치 기준 £{total_projected_revenue * 2:,.2f} 장기 수익 예상"
    ]
    
    for insight in insights:
        st.info(insight)

# 파일 업로드 기능
st.sidebar.markdown("---")
st.sidebar.subheader("📂 데이터 업로드")

uploaded_files = st.sidebar.file_uploader(
    "Excel 파일을 업로드하세요",
    type=['xlsx', 'xls'],
    accept_multiple_files=True,
    help="펫고객 데이터, 제품 데이터, 주기상향 변화 데이터를 업로드할 수 있습니다."
)

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)}개 파일이 업로드되었습니다!")
    for file in uploaded_files:
        st.sidebar.write(f"📄 {file.name}")

# 사용법 안내
with st.sidebar.expander("❓ 사용법 안내"):
    st.write("""
    **📊 대시보드**: 전체 펫 고객 현황과 주요 지표를 확인할 수 있습니다.
    
    **🎯 개인 고객 분석**: 특정 고객의 상세한 구매 패턴을 분석합니다.
    - 🏠 예상 가구수
    - 🐾 반려동물 유형 (소형견/중형견/대형견, 새끼고양이/성묘)
    - 📊 동일 빈도 그룹 내 비교 (펫지출, 총지출, 펫지출비율)
    - 🐾 함께 구매 펫 추천
    - 🛒 함께 구매 연관 제품
    
    **📈 주기상향 추천**: 구매 빈도 상향을 위한 맞춤 추천을 제공합니다.
    
    **💰 수익 예측**: 주기상향 시나리오별 예상 수익을 계산합니다.
    """)

# 푸터
st.sidebar.markdown("---")
st.sidebar.markdown("🐾펫고객관리시스템")
st.sidebar.markdown("*Powered by Streamlit*")
