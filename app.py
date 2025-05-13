import streamlit as st
import os
import pandas as pd
import joblib

# App configuration
st.set_page_config(page_title="Miuul Coffee Shop", page_icon="☕", layout="wide")

# Global background via CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://yourcdn.com/background.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# End Global CSS

# Load models and data caches
@st.cache_resource
def load_models():
    try:
        model_path = os.path.join("models", "kurlu_catboost_coffee_revenue_model.pkl")
        scaler_path = os.path.join("models", "kurlu_robust_scaler_model.pkl")
        revenue_model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        st.error(f"Model yüklenemedi: {e}")
        st.stop()
    return revenue_model, scaler

@st.cache_data
def load_transaction_data():
    try:
        df = pd.read_csv("CoffeeShop2_updated.csv").drop(columns=["Unnamed: 0"], errors="ignore")
    except FileNotFoundError:
        return pd.DataFrame()
    return df

# Shared header without images
def render_header(title=None, subtitle=None):
    if title:
        st.markdown(f"<h1 style='text-align:center;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<h4 style='text-align:center;'>{subtitle}</h4>", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Sayfalar")
pages = ["Ana Sayfa", "Sipariş Ekranı", "Günlük Kâr Hesapla", "Lokasyon (Admin)", "Model Değerlendirmesi"]
choice = st.sidebar.radio("Sayfa seçin", pages)

# Main pages
if choice == "Ana Sayfa":
    render_header(title="Miuul Coffee Shop", subtitle="Dünyanın ilk yapay zeka destekli kahve molası")
    st.markdown("<h2 style='text-align:center;'>Kahve İçmenin En Akıllı Hali...</h2>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='text-align:center;'>Sizleri sadece bir alışkanlığa değil, her yudumda optimum keyfi bulmak için bir yolculuğa davet ediyoruz. Burada her yudum, bir algoritmanın değil, bir anının parçası olur.</h5>",
        unsafe_allow_html=True
    )
elif choice == "Sipariş Ekranı":
    render_header(title="☕ Coffee Shop Recommender")
    df = load_transaction_data()
    if df.empty:
        st.error("Sipariş verisi bulunamadı. Lütfen 'CoffeeShop2_updated.csv' dosyasını ekleyin.")
        st.stop()
    from mlxtend.frequent_patterns import apriori, association_rules
    basket = df.groupby(['order_id','item_name'])['item_name'].count().unstack().fillna(0) > 0
    rules = association_rules(apriori(basket, min_support=0.01, use_colnames=True), metric="support", min_threshold=0.01)
    rules = rules[rules['lift'] > 1].sort_values('lift', ascending=False)
    price_table = {'Brownie':190, 'Cappuccino':165}
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    def recommend(service, count=1):
        cat = df[df['item_name']==service]['item_cat'].iloc[0]
        recs = []
        for _, r in rules.iterrows():
            if service in r['antecedents']:
                for itm in r['consequents']:
                    if itm != service and df[df['item_name']==itm]['item_cat'].iloc[0] != cat:
                        recs.append(itm)
                        if len(recs) >= count:
                            return recs
        return recs
    sel = st.selectbox("Menü seçin:", sorted(df['item_name'].unique()))
    qty = st.number_input(f"{sel} Adet:", min_value=1, value=1)
    if st.button("Sepete Ekle"):
        st.session_state.cart[sel] = st.session_state.cart.get(sel, 0) + qty
        st.success(f"{sel} sepete eklendi.")
    recs = recommend(sel, 5)
    if recs:
        pick = st.selectbox("Öneriler:", ["Seçiniz"] + recs)
        if pick != "Seçiniz" and st.button("Ekle"):
            st.session_state.cart[pick] = st.session_state.cart.get(pick, 0) + 1
            st.success(f"{pick} sepete eklendi.")
    if st.session_state.cart:
        st.markdown("### 🧺 Sepetiniz")
        total = 0
        for it, cnt in st.session_state.cart.items():
            price = price_table.get(it, 100)
            st.write(f"- {it}: {cnt} x {price} = {price*cnt} TL")
            total += price * cnt
        st.markdown(f"### 💰 Toplam: {total} TL")
elif choice == "Günlük Kâr Hesapla":
    render_header(title="💰 Günlük Kâr Hesaplama")
    model, scaler = load_models()
    locs = {'Mavişehir': (1500, 300, 210), 'Bostanlı': (2500, 400, 250), 'Karşıyaka': (3500, 450, 150)}
    loc = st.selectbox("Lokasyon:", list(locs.keys()))
    foot, cust, avg = locs[loc]
    num = st.number_input("Müşteri Sayısı:", value=cust)
    avg_o = st.number_input("Ortalama Sipariş (₺):", value=avg)
    hrs = st.number_input("Çalışma Saati:", value=8)
    emp = st.number_input("Çalışan Sayısı:", value=2)
    mkt = st.number_input("Pazarlama Harcaması (₺):", value=0)
    if st.button("Hesapla"):
        inp = pd.DataFrame([{  
            "Number_of_Customers_Per_Day": num,
            "Average_Order_Value": avg_o,
            "Operating_Hours_Per_Day": hrs,
            "Number_of_Employees": emp,
            "Marketing_Spend_Per_Day": mkt,
            "Location_Foot_Traffic": foot
        }])
        # Derived features
        inp["Customers_Per_Employee"] = num / emp if emp else 0
        inp["Customer_Traffic_Ratio"] = num / foot if foot else 0
        inp["Total_Orders_Value"] = num * avg_o
        inp["Marketing_Per_Customer"] = mkt / num if num else 0
        inp["Marketing_Order_Interaction"] = mkt * avg_o
        # Align features
        expected = list(model.feature_names_)
        # Separate base features for scaler
        base_feats = scaler.feature_names_in_
        # Scale base features
        scaled = scaler.transform(inp[base_feats])
        scaled_df = pd.DataFrame(scaled, columns=base_feats)
        # Combine scaled base with derived
        final_df = pd.concat([scaled_df, inp[derived_feats].reset_index(drop=True)], axis=1)
        final_df = final_df[expected]
        try:
            preds = model.predict(final_df)
            profit = (preds[0] - emp * 1000) * (hrs / 10)
            st.success(f"Tahmini Gelir: ₺{profit:.2f}")
        except ValueError as e:
            st.error(f"Özellik uyuşmazlığı: {e}\nBeklenen özellikler: {expected}")
            st.stop()
elif choice == "Lokasyon" (Admin)":
    render_header(title="Optimal Lokasyonlar")
    try:
        html = open("miuul coffee lokasyon.html", "r", encoding="utf-8").read()
        st.components.v1.html(html, height=600)
        st.markdown("**1. Mavişehir:** 300 müşteri, 210₺ ort.")
        st.markdown("**2. Bostanlı:** 400 müşteri, 250₺ ort.")
        st.markdown("**3. Karşıyaka:** 450 müşteri, 150₺ ort.")
    except Exception as e:
        st.error(f"Harita yüklenemedi: {e}")
elif choice == "Model Değerlendirmesi":
    render_header(title="☕️ Model Değerlendirmesi")
    st.markdown("**CatBoost R²: 0.9550**")
    st.markdown("**CatBoost RMSE: 7085.73**")
