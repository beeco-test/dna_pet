import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="펫 고객 주기상향 추천서비스",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 설정
st.sidebar.title("🐾 펫 고객 주기상향 추천서비스")
st.sidebar.markdown("---")

# 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["📊 대시보드", "🎯 개인 고객 분석", "📈 주기상향 추천", "💰 수익 예측"]
)

# 샘플 데이터 생성 (실제 사용 시에는 업로드된 파일에서 읽어옴)
@st.cache_data
def load_sample_data():
    # 펫 고객 데이터 샘플 (더 많은 고객 데이터)
    np.random.seed(42)
    customer_count = 50
    
    household_keys = np.random.randint(1000, 9999, customer_count)
    pet_transactions = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], customer_count)
    pet_spend = np.random.uniform(10, 200, customer_count).round(2)
    total_spend = np.random.uniform(500, 8000, customer_count).round(2)
    pet_ratio = (pet_spend / total_spend * 100).round(2)
    # 펫 카테고리를 소분류까지 세분화
    pet_categories_detailed = [
        'DOG-사료/간식, CAT-모래/위생용품', 
        'DOG-장난감/액세서리, CAT-사료/간식',
        'DOG-사료/간식', 
        'CAT-사료/간식, OTHER-새/조류용품',
        'DOG-건강관리/영양제, CAT-장난감/액세서리',
        'CAT-모래/위생용품',
        'DOG-사료/간식, OTHER-물고기/어항용품',
        'DOG-장난감/액세서리',
        'CAT-사료/간식',
        'DOG-건강관리/영양제, CAT-건강관리/영양제, OTHER-햄스터/소동물용품',
        'DOG-사료/간식, CAT-사료/간식, OTHER-새/조류용품',
        'DOG-목줄/하네스/이동장',
        'CAT-모래/위생용품, OTHER-물고기/어항용품',
        'DOG-장난감/액세서리, CAT-모래/위생용품',
        'DOG-사료/간식, CAT-장난감/액세서리',
        'OTHER-햄스터/소동물용품',
        'DOG-건강관리/영양제',
        'CAT-건강관리/영양제',
        'DOG-목줄/하네스/이동장, CAT-사료/간식',
        'DOG-사료/간식, OTHER-새/조류용품'
    ]
    
    pet_categories = []
    for _ in range(customer_count):
        # 각 고객별로 1-3개의 카테고리를 랜덤 선택
        num_categories = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        selected_categories = np.random.choice(pet_categories_detailed, num_categories, replace=False)
        pet_categories.append(', '.join(selected_categories))
    club_plus_member = np.random.choice([True, False], customer_count, p=[0.3, 0.7])  # 30% club+ 회원
    
    pet_customers = pd.DataFrame({
        'household_key': household_keys,
        'pet_transactions': pet_transactions,
        'pet_spend': pet_spend,
        'total_spend': total_spend,
        'pet_ratio': pet_ratio,
        'pet_categories': pet_categories,
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
def classify_frequency(transactions):
    if transactions <= 2:
        return "저빈도"
    elif transactions <= 8:
        return "월간"
    elif transactions <= 15:
        return "고빈도"
    elif transactions <= 25:
        return "주간"
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
    if frequency == "주간":
        insights.append("주간으로 꾸준히 구매를 하지만, **펫 관련 상품에는 비교적 적은 비용을 지출**합니다.")
        marketing_tips.append("⏱️ **빈도 기반 추천**: 주간 구매자이므로, 펫 관련 **정기배송 제안**이나 **구독형 서비스** 유도 가능.")
    elif frequency == "월간":
        insights.append("월간 단위로 구매하는 **안정적인 구매 패턴**을 보입니다.")
        marketing_tips.append("📅 **정기 구매 유도**: 월간 구매 패턴을 활용한 정기배송 할인 혜택 제안.")
    elif frequency == "고빈도":
        insights.append("**고빈도로 펫 제품을 구매**하는 충성도 높은 고객입니다.")
        marketing_tips.append("💎 **로열티 강화**: 고빈도 구매 고객으로 VIP 혜택 및 리워드 프로그램 제안.")
    
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

# 대시보드 페이지
if menu == "📊 대시보드":
    st.title("🐾 펫 고객 주기상향 추천서비스 대시보드")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 펫 고객 수", f"{len(pet_customers):,}명")
    
    with col2:
        total_pet_spend = pet_customers['pet_spend'].sum()
        st.metric("펫 제품 총 매출", f"${total_pet_spend:,.2f}")
    
    with col3:
        avg_pet_spend = pet_customers['pet_spend'].mean()
        st.metric("평균 펫 지출", f"${avg_pet_spend:.2f}")
    
    with col4:
        potential_revenue = frequency_changes['sales_change'].sum()
        st.metric("상향이동 잠재 수익", f"${potential_revenue:,.2f}")
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 고객 구매 빈도 분포")
        
        # 구매 빈도 분류
        pet_customers['frequency_category'] = pet_customers['pet_transactions'].apply(classify_frequency)
        frequency_counts = pet_customers['frequency_category'].value_counts()
        
        fig_pie = px.pie(
            values=frequency_counts.values,
            names=frequency_counts.index,
            title="구매 빈도별 고객 분포",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("💰 펫 지출 vs 총 지출 관계")
        
        fig_scatter = px.scatter(
            pet_customers,
            x='total_spend',
            y='pet_spend',
            size='pet_transactions',
            color='frequency_category',
            hover_data=['household_key'],
            title="총 지출 대비 펫 지출 분포",
            labels={'total_spend': '총 지출 ($)', 'pet_spend': '펫 지출 ($)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 주기상향 기회 분석
    st.subheader("🎯 주기상향 기회 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("카테고리별 상향 잠재력")
        
        fig_bar = px.bar(
            frequency_changes.head(8),
            x='category',
            y='percentage_change',
            title="주기상향 시 매출 증가율 (%)",
            labels={'percentage_change': '증가율 (%)', 'category': '카테고리'},
            color='percentage_change',
            color_continuous_scale='Viridis'
        )
        # 올바른 방법으로 x축 각도 조정
        fig_bar.update_layout(xaxis={'tickangle': 45})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("상향 대상 고객 식별")
        
        # 상향 가능 고객 (저빈도, 월간 고객)
        upgrade_candidates = pet_customers[
            pet_customers['frequency_category'].isin(['저빈도', '월간'])
        ]
        
        fig_hist = px.histogram(
            upgrade_candidates,
            x='pet_spend',
            color='frequency_category',
            title="상향 대상 고객의 펫 지출 분포",
            labels={'pet_spend': '펫 지출 ($)', 'count': '고객 수'},
            nbins=10
        )
        st.plotly_chart(fig_hist, use_container_width=True)

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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("펫 거래 횟수", f"{customer_data['pet_transactions']}회")
    
    with col2:
        st.metric("펫 지출 금액", f"${customer_data['pet_spend']:.2f}")
    
    with col3:
        st.metric("총 지출 금액", f"${customer_data['total_spend']:.2f}")
    
    with col4:
        st.metric("펫 지출 비율", f"{customer_data['pet_ratio']:.1f}%")
    
    # 현재 구매 빈도
    current_frequency = classify_frequency(customer_data['pet_transactions'])
    st.info(f"**현재 구매 빈도**: {current_frequency}")
    
    # 구매 카테고리
    st.subheader("구매 펫 카테고리")
    categories = customer_data['pet_categories'].split(', ')
    cols = st.columns(len(categories))
    for i, category in enumerate(categories):
        with cols[i]:
            st.markdown(f"**{category}**")
    
    # 비교 분석
    st.subheader("동일 빈도 그룹 내 비교")
    
    same_frequency_customers = pet_customers[
        pet_customers['pet_transactions'].apply(classify_frequency) == current_frequency
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 펫 지출 비교
        fig_box = px.box(
            same_frequency_customers,
            y='pet_spend',
            title=f"{current_frequency} 그룹 펫 지출 분포"
        )
        fig_box.add_hline(
            y=customer_data['pet_spend'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"현재 고객: ${customer_data['pet_spend']:.2f}"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # 펫 지출 비율 비교
        fig_box2 = px.box(
            same_frequency_customers,
            y='pet_ratio',
            title=f"{current_frequency} 그룹 펫 지출 비율 분포"
        )
        fig_box2.add_hline(
            y=customer_data['pet_ratio'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"현재 고객: {customer_data['pet_ratio']:.1f}%"
        )
        st.plotly_chart(fig_box2, use_container_width=True)

# 주기상향 추천 페이지
elif menu == "📈 주기상향 추천":
    st.title("📈 주기상향 추천")
    
    # 상향 단계 선택
    upgrade_path = st.selectbox(
        "상향 경로를 선택하세요:",
        [
            "저빈도 → 월간 구매",
            "월간 구매 → 고빈도",
            "고빈도 → 주간 구매",
            "주간 구매 → 초고빈도"
        ]
    )
    
    st.subheader(f"🎯 {upgrade_path} 추천 전략")
    
    # 상향 대상 고객 식별
    if "저빈도 → 월간" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "저빈도"
        ]
    elif "월간 → 고빈도" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "월간"
        ]
    elif "고빈도 → 주간" in upgrade_path:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "고빈도"
        ]
    else:
        target_customers = pet_customers[
            pet_customers['pet_transactions'].apply(classify_frequency) == "주간"
        ]
    
    # 세션 스테이트 초기화
    if 'selected_customer_detail' not in st.session_state:
        st.session_state.selected_customer_detail = None
    if 'show_customer_list' not in st.session_state:
        st.session_state.show_customer_list = True
    
    # 대상 고객 목록 보기 vs 개별 고객 상세 보기
    if st.session_state.show_customer_list:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📊 대상 고객 정보")
            st.metric("대상 고객 수", f"{len(target_customers)}명")
            if len(target_customers) > 0:
                st.metric("평균 펫 지출", f"${target_customers['pet_spend'].mean():.2f}")
                st.metric("평균 총 지출", f"${target_customers['total_spend'].mean():.2f}")
                club_plus_count = target_customers['club_plus_member'].sum()
                st.metric("Club+ 회원", f"{club_plus_count}명 ({club_plus_count/len(target_customers)*100:.1f}%)")
            
            # 대상 고객 목록 - 리스트 형태로 표시
            st.subheader("🎯 대상 고객 목록")
            
            if len(target_customers) > 0:
                # 정렬 옵션
                sort_option = st.selectbox(
                    "정렬 기준:",
                    ["펫 지출 높은순", "펫 지출 낮은순", "총 지출 높은순", "최근 구매일순"]
                )
                
                if sort_option == "펫 지출 높은순":
                    target_customers_sorted = target_customers.sort_values('pet_spend', ascending=False)
                elif sort_option == "펫 지출 낮은순":
                    target_customers_sorted = target_customers.sort_values('pet_spend', ascending=True)
                elif sort_option == "총 지출 높은순":
                    target_customers_sorted = target_customers.sort_values('total_spend', ascending=False)
                else:
                    target_customers_sorted = target_customers.sort_values('last_purchase_days', ascending=True)
                
                # 고객 목록을 카드 형태로 표시
                for idx, customer in target_customers_sorted.iterrows():
                    with st.container():
                        col_info1, col_info2, col_btn = st.columns([2, 2, 1])
                        
                        with col_info1:
                            club_badge = "🌟 Club+" if customer['club_plus_member'] else "📱 일반"
                            st.write(f"**고객 {customer['household_key']}** {club_badge}")
                            st.write(f"📱 {customer['phone_number']}")
                        
                        with col_info2:
                            st.write(f"💰 펫 지출: ${customer['pet_spend']:.2f}")
                            st.write(f"🛒 총 지출: ${customer['total_spend']:.2f}")
                        
                        with col_btn:
                            if st.button(f"상세보기", key=f"detail_{customer['household_key']}"):
                                st.session_state.selected_customer_detail = customer['household_key']
                                st.session_state.show_customer_list = False
                                st.rerun()
                        
                        st.markdown("---")
                
                # 전체 선택 앱푸쉬 기능
                st.subheader("📱 앱푸쉬 발송")
                
                push_message = st.text_area(
                    "푸쉬 메시지 내용:",
                    value="🐾 반려동물을 위한 특별한 혜택이 준비되어 있어요! 지금 확인해보세요 💝",
                    height=100
                )
                
                col_push1, col_push2, col_push3 = st.columns(3)
                
                with col_push1:
                    if st.button("🌟 Club+ 회원만 발송", type="primary"):
                        club_plus_customers = target_customers[target_customers['club_plus_member'] == True]
                        st.success(f"Club+ 회원 {len(club_plus_customers)}명에게 푸쉬 발송 완료!")
                        with st.expander("발송 대상 확인"):
                            for _, customer in club_plus_customers.iterrows():
                                st.write(f"📱 {customer['phone_number']} (고객 {customer['household_key']})")
                
                with col_push2:
                    if st.button("📱 전체 고객 발송"):
                        st.success(f"전체 대상 고객 {len(target_customers)}명에게 푸쉬 발송 완료!")
                        with st.expander("발송 대상 확인"):
                            for _, customer in target_customers.iterrows():
                                club_status = "🌟 Club+" if customer['club_plus_member'] else "📱 일반"
                                st.write(f"📱 {customer['phone_number']} (고객 {customer['household_key']}) {club_status}")
                
                with col_push3:
                    if st.button("📋 고객 데이터 다운로드"):
                        csv = target_customers.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="CSV 다운로드",
                            data=csv,
                            file_name=f'{upgrade_path.replace(" → ", "_")}_고객목록.csv',
                            mime='text/csv'
                        )
            else:
                st.info("해당 상향 경로에 대상 고객이 없습니다.")
        
        with col2:
            st.subheader("🛒 추천 제품/카테고리")
            
            # 상위 추천 카테고리
            top_categories = frequency_changes.head(6)
            
            for idx, category in top_categories.iterrows():
                with st.container():
                    col_cat1, col_cat2, col_cat3 = st.columns([2, 1, 1])
                    
                    with col_cat1:
                        st.write(f"**{category['category']}**")
                    
                    with col_cat2:
                        st.metric("예상 매출 증가", f"${category['sales_change']:.2f}")
                    
                    with col_cat3:
                        st.metric("증가율", f"{category['percentage_change']:.1f}%")
                    
                    # 프로그레스 바
                    progress = min(category['percentage_change'] / 1000, 1.0)
                    st.progress(progress)
                    
                    st.markdown("---")
            
            # 맞춤형 추천 전략
            st.subheader("💡 맞춤형 추천 전략")
            
            strategy_options = [
                "🥩 **단백질 중심 전략**: BEEF, PORK 등 육류 제품 중심 추천",
                "🥤 **편의성 전략**: SOFT DRINKS, FROZEN PIZZA 등 간편 제품 추천",
                "🧀 **프리미엄 전략**: CHEESE, 고급 식재료 중심 추천",
                "🍞 **일상 필수품 전략**: FLUID MILK, BREAD 등 기본 식품 추천"
            ]
            
            for strategy in strategy_options:
                st.write(strategy)
    
    else:
        # 개별 고객 상세 보기
        selected_customer_id = st.session_state.selected_customer_detail
        customer_detail = target_customers[target_customers['household_key'] == selected_customer_id].iloc[0]
        
        # 뒤로가기 버튼
        if st.button("← 고객 목록으로 돌아가기"):
            st.session_state.show_customer_list = True
            st.session_state.selected_customer_detail = None
            st.rerun()
        
        st.subheader(f"🎯 고객 {selected_customer_id} 상세 현황")
        
        # 고객 기본 정보
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("펫 거래 횟수", f"{customer_detail['pet_transactions']}회")
        
        with col2:
            st.metric("펫 지출 금액", f"${customer_detail['pet_spend']:.2f}")
        
        with col3:
            st.metric("총 지출 금액", f"${customer_detail['total_spend']:.2f}")
        
        with col4:
            st.metric("펫 지출 비율", f"{customer_detail['pet_ratio']:.1f}%")
        
        with col5:
            club_status = "🌟 Club+ 회원" if customer_detail['club_plus_member'] else "📱 일반 회원"
            st.metric("회원 등급", club_status)
        
        # 추가 정보
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"📱 연락처: {customer_detail['phone_number']}")
        
        with col2:
            st.info(f"🛒 마지막 구매: {customer_detail['last_purchase_days']}일 전")
        
        with col3:
            st.info(f"🐾 펫 카테고리: {customer_detail['pet_categories']}")
        
        # 개인별 맞춤 추천
        st.subheader("🎯 개인 맞춤 추천 전략")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 구매 패턴 분석")
            
            # 현재 구매 빈도
            current_frequency = classify_frequency(customer_detail['pet_transactions'])
            st.write(f"**현재 구매 빈도**: {current_frequency}")
            
            # 펫 카테고리 소분류 표시
            st.markdown("### 🐾 구매 펫 카테고리 (소분류)")
            categories = customer_detail['pet_categories'].split(', ')
            for category in categories:
                if '-' in category:
                    main_cat, sub_cat = category.split('-', 1)
                    st.write(f"• **{main_cat}**: {sub_cat}")
                else:
                    st.write(f"• **{category}**")
            
            # 추천 전략
            if customer_detail['pet_ratio'] < 2.0:
                strategy = "💡 **펫 제품 비중 증가 전략**\n- 현재 펫 지출 비율이 낮아 증가 여지가 큽니다\n- 펫 전용 상품 추천으로 비중 확대"
            elif customer_detail['last_purchase_days'] > 30:
                strategy = "⏰ **재방문 유도 전략**\n- 마지막 구매가 30일 이상 경과\n- 할인 쿠폰 및 이벤트로 재방문 유도"
            elif customer_detail['club_plus_member']:
                strategy = "🌟 **Club+ 프리미엄 전략**\n- Club+ 회원 전용 혜택 활용\n- 고급 펫 제품 및 서비스 추천"
            else:
                strategy = "📈 **Club+ 가입 유도 전략**\n- Club+ 가입 혜택 안내\n- 멤버십 전환으로 로열티 증대"
            
            st.markdown(strategy)
        
        with col2:
            st.markdown("### 📱 개인별 푸쉬 발송")
            
            # 개인 맞춤 푸쉬 메시지 템플릿
            if customer_detail['club_plus_member']:
                default_message = f"🌟 {selected_customer_id}님, Club+ 회원 전용 펫 용품 특가 이벤트가 시작되었어요! 지금 확인해보세요 🐾"
            else:
                default_message = f"🐾 {selected_customer_id}님, 반려동물을 위한 새로운 상품이 입고되었어요! 특별 할인도 놓치지 마세요 💝"
            
            personal_message = st.text_area(
                "개인 맞춤 푸쉬 메시지:",
                value=default_message,
                height=100
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("📱 푸쉬 발송", type="primary"):
                    st.success(f"고객 {selected_customer_id}님에게 푸쉬 발송 완료!")
                    st.info(f"발송 번호: {customer_detail['phone_number']}")
            
            with col_btn2:
                if st.button("📧 이메일 발송"):
                    st.success(f"고객 {selected_customer_id}님에게 이메일 발송 완료!")
            
            # 발송 이력
            st.markdown("### 📋 최근 발송 이력")
            st.text("• 2025.08.01 - 신상품 안내 푸쉬")
            st.text("• 2025.07.28 - 할인 쿠폰 이메일")
            st.text("• 2025.07.25 - Club+ 혜택 안내 푸쉬")
        
        # 고객 인사이트 섹션 추가
        st.markdown("---")
        st.subheader("💡 고객 인사이트 분석")
        
        # 인사이트 생성
        insights, marketing_tips = generate_customer_insights(customer_detail, target_customers)
        
        # 요약 인사이트
        st.markdown("### 📊 **요약 인사이트**")
        for insight in insights:
            st.write(f"* {insight}")
        
        # 마케팅 시사점
        st.markdown("### 💡 **마케팅 시사점**")
        for tip in marketing_tips:
            st.write(f"* {tip}")
        
        # 추가 데이터 시각화
        col1, col2 = st.columns(2)
        
        with col1:
            # 동일 빈도 그룹과의 비교
            st.markdown("### 📈 **동일 빈도 그룹 대비 위치**")
            same_frequency_customers = target_customers[
                target_customers['pet_transactions'].apply(classify_frequency) == current_frequency
            ]
            
            if len(same_frequency_customers) > 1:
                # 펫 지출 순위
                pet_spend_rank = (same_frequency_customers['pet_spend'] < customer_detail['pet_spend']).sum() + 1
                total_in_group = len(same_frequency_customers)
                pet_spend_percentile = (1 - (pet_spend_rank - 1) / total_in_group) * 100
                
                st.metric(
                    f"{current_frequency} 그룹 내 펫 지출 순위",
                    f"{pet_spend_rank}/{total_in_group}위",
                    f"상위 {pet_spend_percentile:.1f}%"
                )
                
                # 총 지출 순위
                total_spend_rank = (same_frequency_customers['total_spend'] < customer_detail['total_spend']).sum() + 1
                total_spend_percentile = (1 - (total_spend_rank - 1) / total_in_group) * 100
                
                st.metric(
                    f"{current_frequency} 그룹 내 총 지출 순위",
                    f"{total_spend_rank}/{total_in_group}위",
                    f"상위 {total_spend_percentile:.1f}%"
                )
        
        with col2:
            # 상향 가능성 점수
            st.markdown("### 🎯 **상향 가능성 분석**")
            
            # 상향 점수 계산 (0-100점)
            upgrade_score = 0
            
            # 펫 지출 비율이 낮으면 상향 가능성 높음
            if customer_detail['pet_ratio'] < target_customers['pet_ratio'].mean():
                upgrade_score += 25
            
            # 총 지출이 높으면 상향 가능성 높음  
            if customer_detail['total_spend'] > target_customers['total_spend'].mean():
                upgrade_score += 25
            
            # Club+ 회원이면 상향 가능성 높음
            if customer_detail['club_plus_member']:
                upgrade_score += 20
            
            # 최근 구매일이 짧으면 상향 가능성 높음
            if customer_detail['last_purchase_days'] < 30:
                upgrade_score += 20
            
            # 카테고리 다양성
            categories = customer_detail['pet_categories'].split(', ')
            if len(categories) >= 2:
                upgrade_score += 10
            
            # 점수에 따른 등급
            if upgrade_score >= 80:
                grade = "🌟 매우 높음"
                color = "green"
            elif upgrade_score >= 60:
                grade = "📈 높음"  
                color = "blue"
            elif upgrade_score >= 40:
                grade = "📊 보통"
                color = "orange"
            else:
                grade = "📉 낮음"
                color = "red"
            
            st.metric("상향 가능성 점수", f"{upgrade_score}/100점", grade)
            
            # 점수 세부 내역
            with st.expander("점수 세부 내역 보기"):
                st.write("**점수 산정 기준:**")
                st.write(f"• 펫 지출 개선 여지: {'✅ +25점' if customer_detail['pet_ratio'] < target_customers['pet_ratio'].mean() else '❌ 0점'}")
                st.write(f"• 총 지출 규모: {'✅ +25점' if customer_detail['total_spend'] > target_customers['total_spend'].mean() else '❌ 0점'}")
                st.write(f"• Club+ 회원: {'✅ +20점' if customer_detail['club_plus_member'] else '❌ 0점'}")
                st.write(f"• 구매 활성도: {'✅ +20점' if customer_detail['last_purchase_days'] < 30 else '❌ 0점'}")
                st.write(f"• 카테고리 다양성: {'✅ +10점' if len(categories) >= 2 else '❌ 0점'}")

# 수익 예측 페이지
elif menu == "💰 수익 예측":
    st.title("💰 수익 예측 분석")
    
    st.subheader("📈 주기상향 시나리오별 수익 예측")
    
    # 시나리오 설정
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
    
    # 각 상향 단계별 예측
    scenarios = [
        {
            'name': '저빈도 → 월간',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "저빈도"]),
            'avg_increase': frequency_changes['sales_change'].mean()
        },
        {
            'name': '월간 → 고빈도',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "월간"]),
            'avg_increase': frequency_changes['sales_change'].mean() * 1.2
        },
        {
            'name': '고빈도 → 주간',
            'target_count': len(pet_customers[pet_customers['pet_transactions'].apply(classify_frequency) == "고빈도"]),
            'avg_increase': frequency_changes['sales_change'].mean() * 1.5
        }
    ]
    
    # 수익 예측 계산
    total_projected_revenue = 0
    scenario_results = []
    
    for scenario in scenarios:
        converted_customers = scenario['target_count'] * (conversion_rate / 100)
        monthly_increase = converted_customers * scenario['avg_increase']
        total_increase = monthly_increase * target_months
        total_projected_revenue += total_increase
        
        scenario_results.append({
            'scenario': scenario['name'],
            'target_customers': scenario['target_count'],
            'converted_customers': int(converted_customers),
            'monthly_revenue_increase': monthly_increase,
            'total_revenue_increase': total_increase
        })
    
    # 결과 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 예상 수익 증가", f"${total_projected_revenue:,.2f}")
    
    with col2:
        total_converted = sum([r['converted_customers'] for r in scenario_results])
        st.metric("총 전환 예상 고객", f"{total_converted}명")
    
    with col3:
        monthly_avg = total_projected_revenue / target_months
        st.metric("월평균 수익 증가", f"${monthly_avg:,.2f}")
    
    # 시나리오별 상세 결과
    st.subheader("📋 시나리오별 상세 예측")
    
    results_df = pd.DataFrame(scenario_results)
    
    # 차트 생성
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("시나리오별 총 수익 증가", "시나리오별 전환 고객 수"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 수익 증가 차트
    fig.add_trace(
        go.Bar(
            x=results_df['scenario'],
            y=results_df['total_revenue_increase'],
            name="총 수익 증가",
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # 전환 고객 수 차트
    fig.add_trace(
        go.Bar(
            x=results_df['scenario'],
            y=results_df['converted_customers'],
            name="전환 고객 수",
            marker_color='lightgreen'
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 상세 테이블
    st.subheader("📊 상세 수익 예측 테이블")
    
    display_df = results_df.copy()
    display_df['monthly_revenue_increase'] = display_df['monthly_revenue_increase'].apply(lambda x: f"${x:,.2f}")
    display_df['total_revenue_increase'] = display_df['total_revenue_increase'].apply(lambda x: f"${x:,.2f}")
    
    display_df.columns = [
        '상향 시나리오',
        '대상 고객 수',
        '예상 전환 고객',
        '월별 수익 증가',
        f'{target_months}개월 총 수익 증가'
    ]
    
    st.dataframe(display_df, use_container_width=True)
    
    # 추가 인사이트
    st.subheader("💡 추가 인사이트")
    
    insights = [
        f"📊 **최고 수익 시나리오**: {scenario_results[0]['scenario']} - ${scenario_results[0]['total_revenue_increase']:,.2f}",
        f"🎯 **전환율 1% 증가 시**: 추가 ${(total_projected_revenue * 0.01 / (conversion_rate / 100)):,.2f} 수익 기대",
        f"⏰ **목표 기간 연장 시**: 12개월 기준 ${(total_projected_revenue * 12 / target_months):,.2f} 수익 가능",
        f"🔄 **지속적 상향 시**: 고객 생애가치 기준 ${total_projected_revenue * 2:,.2f} 장기 수익 예상"
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
    
    **📈 주기상향 추천**: 구매 빈도 상향을 위한 맞춤 추천을 제공합니다.
    
    **💰 수익 예측**: 주기상향 시나리오별 예상 수익을 계산합니다.
    """)

# 푸터
st.sidebar.markdown("---")
st.sidebar.markdown("🐾 **펫 고객 주기상향 추천서비스**")
st.sidebar.markdown("*Powered by Streamlit*")