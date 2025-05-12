import streamlit as st
import pandas as pd
import random
from mlxtend.frequent_patterns import apriori, association_rules



st.set_page_config(page_title="Coffee Shop Recommender", layout="wide")


#########################################
# LOGO VE SLOGAN:
#########################################

col1, col2, col3 = st.columns(3)
col2.image("miul_son - Kopya.png", width=550, use_container_width=False) #tüm ekran için true yap

#########################################
########################################
#🌰 Arka Plan Görseli - Kahve Teması
########################################
########################################

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-photo/coffee-beans-dark-background-top-view-coffee-concept-banner_1220-6300.jpg?t=st=1744490433~exp=1744494033~hmac=28bd86c9edbb495d2d08a9bce77aa22445d0eb545bc24d9db73e5afc533aa25e&w=1380");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Arka planı biraz karart */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.35);
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#################################################################################
#################################################################################

# 📦 Veriyi yükle
@st.cache_data
def load_data():
    df = pd.read_csv("CoffeeShop2_updated.csv")
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    return df

df = load_data()

# 🎯 Fiyat tablosu (TL)
price_table = {
    'Brownie': 190,
    'Cappuccino': 165,
    'Caramel Macchiato': 205,
    'Cheesecake': 210,
    'Iced Latte': 200,
    'Iced Mocha': 220,
    'Cookie': 140,
    'Croissant': 150,
    'Espresso': 125,
    'Flat White': 165,
    'Herbal Tea': 130,
    'Hot Chocolate': 150,
    'Iced Tea': 120,
    'Latte': 170,
    'Lemonade': 170,
    'Mocha': 215,
    'Sandwich Salami&Mozzarella': 250,
    'Tea': 90,
    'Toast': 200,
    'White Mocha': 215,
    'Americano' : 200,
    'Iced Americano' : 215
}

# ✅ Session başlat
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "order_summary" not in st.session_state:
    st.session_state.order_summary = ""

if "order_total" not in st.session_state:
    st.session_state.order_total = 0

# 💡 Ürün ve kategori bilgileri
all_items = sorted(df["item_name"].unique())
category_map = df[['item_name', 'item_cat']].drop_duplicates().set_index('item_name')['item_cat'].to_dict()

# 🔁 Apriori ile öneri kuralları
# 1. Pivot tablosunu oluştur (basket-service formatında)
service_df = df.groupby(['order_id', 'item_name'])['item_name'].count().unstack().fillna(0)

# 2. Sayıları 1/0’a dönüştür (var/yok bilgisi) - vektörleştirilmiş yaklaşım
service_df = service_df > 0
frequent_itemsets = apriori(service_df, min_support=0.01, use_colnames=True)
frequent_itemsets = frequent_itemsets.sort_values("support", ascending=False)
apr_rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
filtered_rules = apr_rules[apr_rules["lift"] > 1].sort_values("lift", ascending=False)
category_map = df[['item_name', 'item_cat']].drop_duplicates().set_index('item_name')['item_cat'].to_dict()


# 🔮 Öneri fonksiyonu
def arl_recommender(rules_df, service, rec_count=1, category_map=None):
    """
    Verilen ürünün (service) kategorisiyle aynı olmayan ürünleri,
    association rules üzerinden lift değerine göre tavsiye eder.
    """
    if category_map is None:
        raise ValueError("category_map gereklidir!")

    # Giriş ürününün kategorisini al
    input_category = category_map.get(service)
    if input_category is None:
        raise ValueError(f"{service} ürünü için kategori bilgisi bulunamadı!")

    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_set = set()

    for _, row in sorted_rules.iterrows():
        if service in row["antecedents"]:
            for item in row["consequents"]:
                # Aynı ürünü veya aynı kategorideki ürünleri eklemiyoruz
                if item != service and category_map.get(item) != input_category:
                    recommendation_set.add(item)
                    if len(recommendation_set) >= rec_count:
                        return list(recommendation_set)

    return list(recommendation_set)

# 🔹 Menüden ürün seç
col1, col2, col3 = st.columns(3)
col2.subheader(" ")
selected_item = col2.selectbox("Lütfen menüden bir seçim yapınız.", all_items)
quantity = col2.number_input(f"{selected_item} için adet:", min_value=1, max_value=10, value=1)

if col2.button("➕ Sepete Ekle"):
    if selected_item in st.session_state.cart:
        item_info = st.session_state.cart[selected_item]
        if isinstance(item_info, dict):
            item_info["adet"] += quantity
        else:
            st.session_state.cart[selected_item] = {"adet": item_info + quantity, "onerilen": False}
    else:
        st.session_state.cart[selected_item] = {"adet": quantity, "onerilen": False}
    col2.success(f"{selected_item} sepete eklendi.")

# 🔹 Tavsiye önerileri sepete ekleme
col2.markdown("---")
recs = arl_recommender(apr_rules, selected_item, 5, category_map)
recommended_item = None
if recs:
    recommended_item = col2.selectbox("Ürününüze Özel Tavsiyeler:", ["Seçiniz"] + recs)
    if recommended_item and recommended_item != "Seçiniz":
        if col2.button(f"⭐️ {recommended_item} önerisini sepete ekle"):
            if recommended_item in st.session_state.cart:
                item_info = st.session_state.cart[recommended_item]
                if isinstance(item_info, dict):
                    item_info["adet"] += 1
                else:
                    st.session_state.cart[recommended_item] = {"adet": item_info + 1, "onerilen": True}
            else:
                st.session_state.cart[recommended_item] = {"adet": 1, "onerilen": True}
            col2.success(f"{recommended_item} öneri olarak sepete eklendi.")
else:
    col2.info("Bu ürün için öneri bulunamadı.")


# 🛍️ Sepet
col1, col2, col3 = st.columns(3)
if st.session_state.cart:
    col2.markdown("---")
    st.markdown("<h5 style='text-align: center;'>🧺 Sepetiniz</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
    toplam = 0
    siparis_ozeti = []

    for item, info in list(st.session_state.cart.items()):
        adet = info["adet"]
        öneri = info.get("onerilen", False)
        price = price_table.get(item, 0)
        toplam += price * adet
        siparis_ozeti.append(f"- {item} ({adet} adet) = {price * adet} TL")

        #col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])

        col1, col2, col3, col4, col5, col6= st.columns([3, 1, 1, 1, 1, 3])
        with col2:
            etiket = " ⭐️" if öneri else ""
            st.markdown(f"**{item}{etiket}**")
        with col3:
            st.markdown(f"**{adet} adet — {price * adet} TL**")
        with col4:
            if st.button("➖", key=f"dec_{item}"):
                if st.session_state.cart[item]["adet"] > 1:
                    st.session_state.cart[item]["adet"] -= 1
                else:
                    del st.session_state.cart[item]
                st.rerun()
        with col5:
            if st.button("➕", key=f"inc_{item}"):
                st.session_state.cart[item]["adet"] += 1
                st.rerun()
        with col6:
            if st.button("❌", key=f"remove_{item}"):
                del st.session_state.cart[item]
                st.rerun()
    col1, col2, col3 = st.columns(3)
    col2.markdown("----")
    col1, col2, col3, col4, col5 = st.columns(5)
    st.markdown("<h7 style='text-align: center;'> </h7>", unsafe_allow_html=True)
    col3.markdown(f"##### 💰   Toplam Tutar: {toplam:.2f} TL")
    st.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6= st.columns([2, 1, 1, 1, 1, 2])

    col_finish, col_clear = col2.columns(2)
    with col_finish:
        if col3.button("🎉 Siparişi Tamamla"):
            st.session_state.order_summary = "\n".join(siparis_ozeti)
            st.session_state.order_total = toplam
            col2.success("Siparişiniz başarıyla oluşturuldu! ☕️ Afiyet olsun.")
            st.session_state.cart.clear()
            st.rerun()
    with col_clear:
        if col4.button("🗑️ Sepeti Temizle"):
            st.session_state.cart.clear()
            st.rerun()

col1, col2, col3 = st.columns(3)
# ✅ Sipariş özeti ve toplamı
if st.session_state.order_summary:
    col2.markdown("### 🧾 Sipariş Özeti")
    col2.code(st.session_state.order_summary, language="markdown")
    col2.markdown(f"### 💰 Toplam Tutar: {st.session_state.order_total:.2f} TL")

    if col2.button("🆕 Yeni Sipariş Ver"):
        st.session_state.order_summary = ""
        st.session_state.order_total = 0
        st.session_state.cart = {}
        st.rerun()