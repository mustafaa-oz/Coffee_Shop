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

# Shared header with optional logo (bytes)
def render_header(title=None, subtitle=None, logo_path=None):
    if logo_path and os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as f:
                img = f.read()
            st.image(img, use_column_width=True)
        except Exception as e:
            st.warning(f"Logo yüklenemedi: {e}")
    if title:
        st.markdown(f"<h1 style='text-align:center;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<h4 style='text-align:center;'>{subtitle}</h4>", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Sayfalar")
pages = ["Ana Sayfa", "Sipariş Ekranı", "Günlük Kâr Hesapla", "Lokasyon (Admin)", "Model Değerlendirmesi"]
choice = st.sidebar.radio("Sayfa seçin", pages)

# Main pages
logo = "assets/miul_son.png"

if choice == "Ana Sayfa":
    render_header(
        title="Miuul Coffee Shop",
        subtitle="Dünyanın ilk yapay zeka destekli kahve molası",
        logo_path=logo
    )
    st.markdown("<h2 style='text-align:center;'>Kahve İçmenin En Akıllı Hali...</h2>", unsafe_allow_html=True)
    cols = st.columns([1,4,1])
    for c in [cols[0], cols[2]]:
        path = "assets/serbest_cekirdek.png"
        if os.path.exists(path):
            with open(path,'rb') as f:
                c.image(f.read(), width=400)
        else:
            c.write("Resim bulunamadı")
    st.markdown(
        "<h5 style='text-align:center;'>Sizleri sadece bir alışkanlığa değil, her yudumda optimum keyfi bulmak için bir yolculuğa davet ediyoruz. Burada her yudum, bir algoritmanın değil, bir anının parçası olur.</h5>",
        unsafe_allow_html=True
    )

elif choice == "Sipariş Ekranı":
    render_header(title="☕ Coffee Shop Recommender", logo_path=logo)
    df = load_transaction_data()
    from mlxtend.frequent_patterns import apriori, association_rules
    basket = df.groupby(['order_id','item_name'])['item_name'].count().unstack().fillna(0) > 0
    rules = association_rules(apriori(basket, min_support=0.01, use_colnames=True), metric="support", min_threshold=0.01)
    rules = rules[rules['lift'] > 1].sort_values('lift', ascending=False)
    price_table = { 'Brownie':190, 'Cappuccino':165 }
    if 'cart' not in st.session_state: st.session_state.cart = {}
    def recommend(service, count=1):
        cat = df[df['item_name']==service]['item_cat'].iloc[0]
        recs=[]
        for _,r in rules.iterrows():
            if service in r['antecedents']:
                for itm in r['consequents']:
                    if itm!=service and df[df['item_name']==itm]['item_cat'].iloc[0]!=cat:
                        recs.append(itm)
                        if len(recs)>=count: return recs
        return recs
    sel = st.selectbox("Menü seçin", sorted(df['item_name'].unique()))
    qty = st.number_input(f"{sel} adet:",1,1)
    if st.button("Sepete Ekle"):
        st.session_state.cart[sel]=st.session_state.cart.get(sel,0)+qty
        st.success(f"{sel} sepete eklendi")
    recs = recommend(sel,5)
    if recs:
        pick = st.selectbox("Öneriler", ["Seçiniz"]+recs)
        if pick!="Seçiniz" and st.button("Ekle"):
            st.session_state.cart[pick]=st.session_state.cart.get(pick,0)+1
            st.success(f"{pick} sepete eklendi")
    if st.session_state.cart:
        st.write("Sepetiniz:")
        total=0
        for item,cnt in st.session_state.cart.items():
            price=price_table.get(item,100)
            st.write(f"{item}: {cnt} x {price} = {price*cnt}")
            total+=price*cnt
        st.write(f"Toplam: {total}")

elif choice == "Günlük Kâr Hesapla":
    render_header(title="💰 Günlük Kâr Hesaplama", logo_path=logo)
    model, scaler = load_models()
    locs = {'Mavişehir':(1500,300,210),'Bostanlı':(2500,400,250),'Karşıyaka':(3500,450,150)}
    loc = st.selectbox("Lokasyon", list(locs.keys()))
    foot, cust, avg = locs[loc]
    num = st.number_input("Müşteri Sayısı", value=cust)
    avg_o = st.number_input("Ortalama Sipariş", value=avg)
    hrs = st.number_input("Çalışma Saati", value=8)
    emp = st.number_input("Çalışan Sayısı", value=2)
    mkt = st.number_input("Pazarlama Harcaması", value=0)
    if st.button("Hesapla"):
        inp = pd.DataFrame([{"Number_of_Customers_Per_Day":num,"Average_Order_Value":avg_o,"Operating_Hours_Per_Day":hrs,"Number_of_Employees":emp,"Marketing_Spend_Per_Day":mkt,"Location_Foot_Traffic":foot}])
        pred = model.predict(pd.DataFrame(scaler.transform(inp),columns=inp.columns))
        profit = (pred[0] - emp*1000)*(hrs/10)
        st.write(f"Tahmini Gelir: ₺{profit}")

elif choice == "Lokasyon (Admin)":
    render_header(title="Optimal Lokasyonlar", logo_path=logo)
    try:
        html = open("miuul coffee lokasyon.html","r",encoding="utf-8").read()
        st.components.v1.html(html,height=600)
    except:
        st.write("Harita yüklenemedi.")

else:
    render_header(title="Model Değerlendirmesi", logo_path=logo)
    st.write("Model metrikleri..." )
