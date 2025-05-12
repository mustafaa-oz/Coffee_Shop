import streamlit as st
import folium
from streamlit_folium import folium_static

#########################################
# LOGO VE SLOGAN:
#########################################

col1, col2, col3 = st.columns(3)
col2.image("miul_son - Kopya.png", width=550, use_container_width=False) #tüm ekran için true yap
col2.markdown("<h4 style='text-align: center;'>Kahve İçmenin En Akıllı Hali...</h4>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
#########################################
#########################################
# AÇIKLAMA ÖNCESİ GÖRSEL:
#########################################

col1, col2 = st.columns([16, 22])
col2.image("KAHVE KALP.png", width=180, use_container_width=False) #tüm ekran için true yap

#########################################
# AÇIKLAMANIN BAŞLIĞI:
#########################################

col1, col2, col3 = st.columns([8, 8, 7])

col2.title(":green[ Karşı]:red[yaka] 'nın Kalbi !")

#########################################
# AÇIKLAMA KISMI:
#########################################
col1, col2, col3 = st.columns([1, 8, 1])

col2.markdown("<h4 style='text-align: center;'>İzmir Karşıyaka’da açmayı planladığımız Miuul Coffee Shop için "
              "en uygun lokasyonu belirlemek amacıyla 60’tan fazla yoğun noktayı analiz ettik. "
              "Okullar, hastaneler, AVM’ler, pazar yerleri ve spor alanları gibi"
              " yaya trafiğinin yoğun olduğu bölgeleri işaretledik.</h4>", unsafe_allow_html=True)

col2.markdown("<h3 style='text-align: center;'>K-Means modeli ile müşteri potansiyeli en yüksek"
              " 3 ideal konumu belirledik. Aşağıdaki haritada, bu noktalarla birlikte"
              " analiz ettiğimiz tüm bölgeleri inceleyebilirsiniz.</h3>", unsafe_allow_html=True)

col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)


#########################################
# HARİTA BAŞLIĞI;
#########################################

st.title("Optimal Lokasyon Seçenekleri:")

#########################################
# HARİTANIN EKLENMESİ;
#########################################

col1, col2 = st.columns([8, 2])

# HTML dosyasını iframe olarak yükle
html_file = "miuul coffee lokasyon.html"  # Daha önce kaydettiğin dosyanın adı

with col1:
    st.components.v1.html(open(html_file, "r", encoding="utf-8").read(), height=600, width=1200)

#########################################
# HARİTANIN YANINDAKİ YAZILAR;
#########################################

with col2:
    st.markdown("<h4 style='text-align: center;'>1. Lokasyon: Mavişehir </h4>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Ortalama Sipariş Tutarı: 210₺</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: red;'>Ortalama Günlük Müşteri Sayısı: 300</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: red;'>Yaya Trafiği: 1500  </h6>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>2. Lokasyon: Bostanlı </h4>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Ortalama Sipariş Tutarı: 250₺ </h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Ortalama Günlük Müşteri Sayısı: 400</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Yaya Trafiği: 2500</h6>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>3. Lokasyon: Karşıyaka </h4>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: red;'>Ortalama Sipariş Tutarı: 150₺ </h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Ortalama Günlük Müşteri Sayısı: 450</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: green;'>Yaya Trafiği: 3500 </h6>", unsafe_allow_html=True)

#########################################
