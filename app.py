import streamlit as st
import numpy as np
import pandas as pd
import joblib
import folium
from streamlit_folium import folium_static
from mlxtend.frequent_patterns import apriori, association_rules

# App configuration
st.set_page_config(page_title="Miuul Coffee Shop", page_icon="☕", layout="wide")

# Load models and data caches
@st.cache_resource
def load_models():
    revenue_model = joblib.load("kurlu_catboost_coffee_revenue_model.pkl")
    scaler = joblib.load("kurlu_robust_scaler_model.pkl")
    return revenue_model, scaler

@st.cache_data
def load_transaction_data():
    df = pd.read_csv("CoffeeShop2_updated.csv").drop(columns=["Unnamed: 0"], errors="ignore")
    return df

# Shared logo header
def render_logo_header(subtitle=None):
    col1, col2, col3 = st.columns(3)
    col2.image("miul_son - Kopya.png", width=550, use_container_width=False)
    if subtitle:
        col2.markdown(f"<h4 style='text-align: center;'>{subtitle}</h4>", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Sayfalar")
pages = ["Ana Sayfa", "Lokasyon (Admin)", "Günlük Kâr Hesapla", "Sipariş Ekranı", "Model Değerlendirmesi"]
choice = st.sidebar.radio("Sayfa seçin", pages)

# Main pages
if choice == "Ana Sayfa":
    render_logo_header()
    # Home page content
    st.markdown("<h2 style='text-align: center;'>Kahve İçmenin En Akıllı Hali...</h2>", unsafe_allow_html=True)
    # Side images
    col1, col2, col3 = st.columns([1,4,1])
    col1.image("serbest_cekirdek.png", width=400)
    col3.image("serbest_cekirdek.png", width=400)
    # Title and description
    st.markdown("<h1 style='text-align: center;'>Dünyanın ilk yapay zeka destekli kahve molası:</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='text-align: center;'>Sizleri sadece bir alışkanlığa değil, her yudumda optimum keyfi bulmak için bir yolculuğa davet ediyoruz. Burada her yudum, bir algoritmanın değil, bir anının parçası olur. Çünkü burada K-means ile değil, dost sohbetiyle kümeleniyoruz.</h5>",
        unsafe_allow_html=True
    )

elif choice == "Sipariş Ekranı":
    # Recommendation page
    st.title("☕ Coffee Shop Recommender")
    render_logo_header()
    df = load_transaction_data()
    # Build apriori rules
    basket = df.groupby(['order_id','item_name'])['item_name'].count().unstack().fillna(0) > 0
    frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    rules = rules[rules['lift'] > 1].sort_values('lift', ascending=False)
    price_table = { 'Brownie':190, 'Cappuccino':165, 'Caramel Macchiato':205, 'Cheesecake':210,
                    'Iced Latte':200, 'Iced Mocha':220, 'Cookie':140, 'Croissant':150,
                    'Espresso':125, 'Flat White':165, 'Herbal Tea':130, 'Hot Chocolate':150,
                    'Iced Tea':120, 'Latte':170, 'Lemonade':170, 'Mocha':215,
                    'Sandwich Salami&Mozzarella':250, 'Tea':90, 'Toast':200,
                    'White Mocha':215, 'Americano':200, 'Iced Americano':215 }
    # Session state
    if 'cart' not in st.session_state: st.session_state.cart = {}
    # Recommender function
    def arl_recommender(service, rec_count=1):
        input_cat = df[df['item_name']==service]['item_cat'].iloc[0]
        recs = []
        for _, row in rules.iterrows():
            if service in row['antecedents']:
                for itm in row['consequents']:
                    if itm != service and df[df['item_name']==itm]['item_cat'].iloc[0]!=input_cat:
                        recs.append(itm)
                        if len(recs)>=rec_count:
                            return recs
        return recs
    # UI
    all_items = sorted(df['item_name'].unique())
    selected = st.selectbox("Lütfen menüden bir seçim yapınız.", all_items)
    qty = st.number_input(f"{selected} için adet:", min_value=1, value=1)
    if st.button("➕ Sepete Ekle"):
        st.session_state.cart[selected] = st.session_state.cart.get(selected,0) + qty
        st.success(f"{selected} sepete eklendi.")
    # Recommendations
    recs = arl_recommender(selected,5)
    if recs:
        pick = st.selectbox("Ürününüze Özel Tavsiyeler:", ["Seçiniz"]+recs)
        if pick!="Seçiniz" and st.button(f"⭐️ {pick} önerisini sepete ekle"):
            st.session_state.cart[pick] = st.session_state.cart.get(pick,0) + 1
            st.success(f"{pick} öneri olarak sepete eklendi.")
    # Cart display & actions
    if st.session_state.cart:
        total=0
        st.markdown("### 🧺 Sepetiniz")
        for item, cnt in st.session_state.cart.items():
            price=price_table.get(item,0)
            st.write(f"- {item}: {cnt} adet — {price*cnt} TL")
            total+=price*cnt
        st.markdown(f"### 💰 Toplam Tutar: {total:.2f} TL")
        if st.button("🎉 Siparişi Tamamla"):
            st.success("Siparişiniz başarıyla oluşturuldu! ☕️ Afiyet olsun.")
            st.session_state.cart.clear()

elif choice == "Günlük Kâr Hesapla":
    # Revenue calculation
    st.title("💰 Günlük Kâr Hesaplama")
    render_logo_header(subtitle="Günlük Kâr Hesaplama")
    model, scaler = load_models()
    # Location presets
    locs = {
        'Mavişehir':(1500,300,210),
        'Bostanlı':(2500,400,250),
        'Karşıyaka':(3500,450,150)
    }
    loc = st.selectbox("Lokasyon seçin", list(locs.keys()))
    foot, cust, avg = locs[loc]
    st.session_state.foot_traffic = foot
    st.session_state.num_customers = cust
    st.session_state.avg_order_value = avg
    # User inputs
    st.session_state.num_customers = st.number_input("Günlük Müşteri Sayısı", value=st.session_state.num_customers)
    st.session_state.avg_order_value = st.number_input("Ortalama Sipariş Tutarı (₺)", value=st.session_state.avg_order_value)
    st.session_state.operating_hours = st.number_input("Günlük Çalışma Saati", value=8)
    st.session_state.num_employees = st.number_input("Çalışan Sayısı", value=2)
    st.session_state.marketing_spend = st.number_input("Günlük Pazarlama Harcaması (₺)", value=0)
    if st.button("📈 Tahmini Geliri Hesapla"):
        data = pd.DataFrame([{
            "Number_of_Customers_Per_Day":st.session_state.num_customers,
            "Average_Order_Value":st.session_state.avg_order_value,
            "Operating_Hours_Per_Day":st.session_state.operating_hours,
            "Number_of_Employees":st.session_state.num_employees,
            "Marketing_Spend_Per_Day":st.session_state.marketing_spend,
            "Location_Foot_Traffic":st.session_state.foot_traffic
        }])
        scaled = scaler.transform(data)
        preds = model.predict(pd.DataFrame(scaled, columns=data.columns))
        profit = (preds[0] - st.session_state.num_employees*1000)*(st.session_state.operating_hours/10)
        st.success(f"Tahmini Günlük Gelir: ₺{profit:,.2f}")

elif choice == "Lokasyon (Admin)":
    # Location map
    st.title("Optimal Lokasyon Seçenekleri")
    render_logo_header()
    st.markdown("<h4 style='text-align:center;'>K-Means modeli ile analiz edilen potansiyel noktalar</h4>", unsafe_allow_html=True)
    # Load and display saved HTML map
    with open("miuul coffee lokasyon.html","r",encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600)
    # Info sidebar
    st.markdown("**1. Mavişehir:** 300 müşteri, 210₺ ort. sipariş, 1500 yaya trafiği")
    st.markdown("**2. Bostanlı:** 400 müşteri, 250₺ ort. sipariş, 2500 yaya trafiği")
    st.markdown("**3. Karşıyaka:** 450 müşteri, 150₺ ort. sipariş, 3500 yaya trafiği")

elif choice == "Model Değerlendirmesi":
    # Model evaluation
    st.title("☕️ Maksimum Gelir Stratejisi")
    render_logo_header()
    st.markdown(
        "<h5 style='text-align:center;'>Modelleme sürecinde müşteri sayısı ve ortalama sipariş değeri en güçlü faktörlerdir.</h5>",
        unsafe_allow_html=True
    )
    # Images & explanations
    col1, col2 = st.columns(2)
    col1.image("Müşteri Sayısı Günlük Gelir.jpg", use_container_width=True)
    col1.image("Ortalama Sipariş Tutarı.jpg", use_container_width=True)
    col2.markdown("<h3 style='text-align:center;'>Günlük müşteri sayısı</h3>", unsafe_allow_html=True)
    col2.markdown("<h5 style='text-align:center;'>Operasyonel odak bu bölgelerde yoğunlaştırıldı.</h5>", unsafe_allow_html=True)
    col2.markdown("<h3 style='text-align:center;'>Tavsiye Sistemi</h3>", unsafe_allow_html=True)
    col2.markdown("<h5 style='text-align:center;'>Apriori tabanlı öneri sistemi entegre edildi.</h5>", unsafe_allow_html=True)
    # Final metrics
    col3, col4 = st.columns(2)
    col3.image("Tahmin grafiği.jpg", use_container_width=True)
    col4.markdown("**CatBoost R²: 0.9550**")
    col4.markdown("**CatBoost RMSE: 7085.73**")
    col4.markdown("Model yüksek doğrulukla tahmin yapmaktadır.")
