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
        try:
            with open("assets/serbest_cekirdek.png", 'rb') as f:
                img = f.read()
            c.image(img, width=400)
        except:
            c.write("Resim yüklenemedi.")
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
    price = { 'Brownie':190, 'Cappuccino':165, 'Caramel Macchiato':205, 'Cheesecake':210 }
    if 'cart' not in st.session_state: st.session_state.cart = {}
    def arl(service, n=1):
        cat = df[df['item_name']==service]['item_cat'].iloc[0]
        rec=[]
        for _,r in rules.iterrows():
            if service in r['antecedents']:
                for i in r['consequents']:
                    if i!=service and df[df['item_name']==i]['item_cat'].iloc[0]!=cat:
                        rec.append(i)
                        if len(rec)>=n: return rec
        return rec
    sel=st.selectbox("Menü seçin", sorted(df['item_name'].unique()))
    q=st.number_input(f"{sel} Adet",1,1)
    if st.button("Sepete Ekle"):
        st.session_state.cart[sel]=st.session_state.cart.get(sel,0)+q
        st.success(f"{sel} eklendi.")
    recs=arl(sel,5)
    if recs:
        p=st.selectbox("Öneriler",["Seçiniz"]+recs)
        if p!="Seçiniz" and st.button("Ekle"):
            st.session_state.cart[p]=st.session_state.cart.get(p,0)+1
            st.success(f"{p} eklendi.")
    if st.session_state.cart:
        st.write("Sepetiniz:")
        tot=0
        for it,c in st.session_state.cart.items():
            pr=price.get(it,100)
            st.write(it, c, pr*c)
            tot+=pr*c
        st.write("Toplam:", tot)

elif choice == "Günlük Kâr Hesapla":
    render_header(title="💰 Günlük Kâr", logo_path=logo)
    m,s=load_models()
    locs={'Mavişehir':(1500,300,210)}
    loc=st.selectbox("Lokasyon",locs.keys())
    f,n,a=locs[loc]
    n=st.number_input("Müşteri",value=n)
    a=st.number_input("Ortalama",value=a)
    h=st.number_input("Saat",value=8)
    e=st.number_input("Çalışan",value=2)
    pm=st.number_input("Pazarlama",value=0)
    if st.button("Hesapla"):
        df0=pd.DataFrame([{"Number_of_Customers_Per_Day":n,"Average_Order_Value":a,"Operating_Hours_Per_Day":h,"Number_of_Employees":e,"Marketing_Spend_Per_Day":pm,"Location_Foot_Traffic":f}])
        pr=m.predict(pd.DataFrame(s.transform(df0),columns=df0.columns))
        pf=(pr[0]-e*1000)*(h/10)
        st.write("Gelir: ₺",pf)

elif choice=="Lokasyon (Admin)":
    render_header(title="Lokasyonlar", logo_path=logo)
    try:
        with open("miuul coffee lokasyon.html","r",encoding="utf-8") as f: html=f.read()
        st.components.v1.html(html,height=600)
    except:
        st.write("Harita yüklenemedi.")

else:
    render_header(title="Model", logo_path=logo)
    st.write("Model metrikleri...")
