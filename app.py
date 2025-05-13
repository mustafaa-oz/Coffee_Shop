import streamlit as st
import pandas as pd
import joblib
import os

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

# Shared header with optional logo
def render_header(title=None, subtitle=None, logo_path=None):
    if logo_path and os.path.exists(logo_path):
        st.image(logo_path, use_column_width=True)
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
    render_header(
        title="Miuul Coffee Shop",
        subtitle="Dünyanın ilk yapay zeka destekli kahve molası",
        logo_path="assets/miul_son.png"
    )
    st.markdown("<h2 style='text-align:center;'>Kahve İçmenin En Akıllı Hali...</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,4,1])
    col1.image("assets/serbest_cekirdek.png", width=400)
    col3.image("assets/serbest_cekirdek.png", width=400)
    st.markdown(
        "<h5 style='text-align:center;'>Sizleri sadece bir alışkanlığa değil, her yudumda optimum keyfi bulmak için bir yolculuğa davet ediyoruz. Burada her yudum, bir algoritmanın değil, bir anının parçası olur.</h5>",
        unsafe_allow_html=True
    )

elif choice == "Sipariş Ekranı":
    render_header(
        title="☕ Coffee Shop Recommender",
        logo_path="assets/miul_son.png"
    )
    df = load_transaction_data()
    from mlxtend.frequent_patterns import apriori, association_rules
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
    if 'cart' not in st.session_state: st.session_state.cart = {}
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
    selected = st.selectbox("Menüden bir seçim yapın:", sorted(df['item_name'].unique()))
    qty = st.number_input(f"{selected} Adet:", min_value=1, value=1)
    if st.button("➕ Sepete Ekle"):
        st.session_state.cart[selected] = st.session_state.cart.get(selected,0) + qty
        st.success(f"{selected} sepete eklendi.")
    recs = arl_recommender(selected,5)
    if recs:
        pick = st.selectbox("Öneriler:", ["Seçiniz"]+recs)
        if pick!="Seçiniz" and st.button(f"⭐️ {pick} ekle"):
            st.session_state.cart[pick] = st.session_state.cart.get(pick,0) + 1
            st.success(f"{pick} öneri olarak sepete eklendi.")
    if st.session_state.cart:
        st.markdown("### 🧺 Sepetiniz")
        total=0
        for item,cnt in st.session_state.cart.items():
            price=price_table.get(item,0)
            st.write(f"- {item}: {cnt} adet — {price*cnt} TL")
            total+=price*cnt
        st.markdown(f"### 💰 Toplam: {total:.2f} TL")
        if st.button("🎉 Siparişi Tamamla"):
            st.success("Sipariş tamamlandı! ☕️")
            st.session_state.cart.clear()

elif choice == "Günlük Kâr Hesapla":
    render_header(
        title="💰 Günlük Kâr Hesaplama",
        logo_path="assets/miul_son.png"
    )
    model, scaler = load_models()
    locs = {'Mavişehir':(1500,300,210),'Bostanlı':(2500,400,250),'Karşıyaka':(3500,450,150)}
    loc = st.selectbox("Lokasyon:", list(locs.keys()))
    foot,cust,avg = locs[loc]
    num_cust = st.number_input("Müşteri Sayısı", value=cust)
    avg_order = st.number_input("Ortalama Sipariş (₺)", value=avg)
    hours = st.number_input("Çalışma Saati", value=8)
    employees = st.number_input("Çalışan Sayısı", value=2)
    marketing = st.number_input("Pazarlama Harcaması (₺)", value=0)
    if st.button("📈 Hesapla"):
        df_input = pd.DataFrame([{"Number_of_Customers_Per_Day":num_cust,
                                  "Average_Order_Value":avg_order,
                                  "Operating_Hours_Per_Day":hours,
                                  "Number_of_Employees":employees,
                                  "Marketing_Spend_Per_Day":marketing,
                                  "Location_Foot_Traffic":foot}])
        preds = model.predict(pd.DataFrame(scaler.transform(df_input),columns=df_input.columns))
        profit = (preds[0] - employees*1000)*(hours/10)
        st.success(f"Tahmini Gelir: ₺{profit:,.2f}")

elif choice == "Lokasyon (Admin)":
    render_header(
        title="Optimal Lokasyonlar",
        logo_path="assets/miul_son.png"
    )
    st.markdown("<h4 style='text-align:center;'>Potansiyel Noktalar</h4>",unsafe_allow_html=True)
    with open("miuul coffee lokasyon.html","r",encoding="utf-8") as f:
        html=f.read()
    st.components.v1.html(html,height=600)
    st.markdown("**1. Mavişehir:** 300 müşteri, 210₺ ort.")
    st.markdown("**2. Bostanlı:** 400 müşteri, 250₺ ort.")
    st.markdown("**3. Karşıyaka:** 450 müşteri, 150₺ ort.")

elif choice == "Model Değerlendirmesi":
    render_header(
        title="☕️ Model Değerlendirmesi",
        logo_path="assets/miul_son.png"
    )
    st.markdown("Modelde müşteri sayısı ve sipariş değeri en güçlü etkenler.")
    cols=st.columns(2)
    cols[0].markdown("**CatBoost R²:** 0.9550")
    cols[0].markdown("**CatBoost RMSE:** 7085.73")
    cols[1].markdown("Apriori tabanlı öneri sistemi entegre edildi.")
