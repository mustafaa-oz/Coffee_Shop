import streamlit as st
import pandas as pd

#########################################
# LOGO VE SLOGAN:
#########################################

col1, col2, col3 = st.columns(3)
col2.image("miul_son - Kopya.png", width=550, use_container_width=False) #tüm ekran için true yap
col2.markdown("<h4 style='text-align: center;'>Kahve İçmenin En Akıllı Hali...</h4>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
#########################################
#########################################

st.markdown("<h1 style='text-align: center;'> ☕️ Maksimum Gelir Stratejisi</h1>", unsafe_allow_html=True)
st.markdown("""
<h4 style='text-align: center;'>
    Doğru Lokasyon + Doğru Öneri = <span style='color: #2ecc71;'>Maksimum Kazanç.</span>
</h4>
""", unsafe_allow_html=True)

st.markdown("""<h3 style='text-align: center;'>  </h3>""", unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center;'> Modelleme sürecinde yaptığımız analizler sonucunda, 
günlük müşteri sayısı, geliri etkileyen en güçlü faktör olarak öne çıkmıştır.</h5>""", unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center;'>Bununla birlikte, 
ortalama sipariş değeri de gelirin şekillenmesinde büyük rol oynayan ikinci önemli değişken olarak 
belirlenmiştir.</h5>""", unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center;'>Bu iki temel değişkenden yola çıkarak, 
maksimum gelir hedefiyle veri odaklı bir tavsiye sistemi geliştirdik.</h5>""", unsafe_allow_html=True)


#########################################
#########################################
#########################################
# 1. Günlük Müşteri Sayısı
#########################################

col1, col2 = st.columns(2)
col1.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col1.image("Müşteri Sayısı Günlük Gelir.jpg", width=740, use_container_width=True) #tüm ekran için true yap
col1.image("karsiyaka.webp", width=740, use_container_width=True) #tüm ekran için true yap


#########################################
#########################################

#########################################
# 1. GRAFİK AÇIKLAMASI
#########################################
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> 1. Günlük müşteri sayısı: </h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Model çıktılarından elde edilen bilgilere dayanarak, 
müşteri sayısının en yüksek olduğu lokasyonlar belirlenmiş ve operasyonel odak bu bölgelere yönlendirilmiştir. 
Bu sayede, yoğun müşteri trafiğinden maksimum gelir elde edilmesi amaçlanmıştır.</h5>""", unsafe_allow_html=True)


#########################################
#########################################
#########################################
# 1. GRAFİK AÇIKLAMASI
#########################################

col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> Lokasyon Analizi: </h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>
İzmir Karşıyaka’da hastane, okul, AVM, kütüphane ve pazar gibi yoğun yaya 
trafiğine sahip 56 farklı nokta belirlendi. Bu lokasyonların koordinatları 
çıkarılarak Folium kütüphanesi ile harita üzerinde görselleştirildi. Ardından 
K-Means kümeleme yöntemi kullanılarak yaya trafiğinin merkezinde bulunan 3 optimal 
kafe lokasyonu tespit edildi. Her bir nokta için günlük müşteri sayısı ve ortalama 
sipariş tutarları, benzer veri setlerinden faydalanarak tahmin edildi.</h5>""", unsafe_allow_html=True)

col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)


#########################################
#########################################

col1, col2, col3, col4, col5 = st.columns(5)

col3.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col3.image("serbest_cekirdek.png", width=250, use_container_width=False) #tüm ekran için true yap
col3.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)

#########################################
#########################################
# 1. GRAFİK AÇIKLAMASI
#########################################
col1, col2 = st.columns(2)
col1.image("Ortalama Sipariş Tutarı.jpg", width=740, use_container_width=True) #tüm ekran için true yap
col1.image("En çok satanlar.jpg", width=740, use_container_width=True) #tüm ekran için true yap


col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)

col2.markdown("<h3 style='text-align: center;'>  2. Ortalama sipariş değeri: </h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Menü mühendisliği, upsell/cross-sell teknikleri 
ve fiyatlama stratejileriyle ortalama harcama artırılabilir.</h5>""", unsafe_allow_html=True)

col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Tavsiye sistemi, günlük müşteri sayısı
 ve ortalama sipariş değeri gibi kritik değişkenleri dinamik olarak analiz ederek, 
 her müşteri etkileşimini daha kârlı hale 
 getirmeye yönelik öneriler sunar.</h5>""", unsafe_allow_html=True)

col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> Tavsiye Sistemi: </h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Ortalama sipariş değerini arttırmak amacıyla, dikkat çekici 
ve kullanıcı dostu 
bir menü arayüzü oluşturulmuştur.</h5>""", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Sipariş ekranına entegre edilen Apriori algoritması 
ve ARL yöntemine dayalı öneri sistemi, kullanıcının seçtiği ürünlere göre tamamlayıcı ürünler önererek 
çapraz satışları artırmayı hedefledik.</h5>""", unsafe_allow_html=True)

col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)

#########################################
#########################################
#########################################
# 3. MODEL SONUÇLARI KISMI
#########################################

col1, col2, col3, col4, col5 = st.columns(5)

col3.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col3.image("serbest_cekirdek.png", width=250, use_container_width=False) #tüm ekran için true yap



st.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)

#########################################
#########################################
# 4. R2 Model Sonuçları
#########################################


col1, col2 = st.columns(2)
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'>GÜNLÜK GELİR TAHMİN MODELİ SONUÇLARI</h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col1.image("Tahmin grafiği.jpg", width=740, use_container_width=True) #tüm ekran için true yap
col2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)

col2.markdown("<h3 style='text-align: center;'> <span style='color: #2ecc71;'>==================================================</span></h3>", unsafe_allow_html=True)
col2.markdown("<h5 style='text-align: center;'> CatBoost R²: 0.9550</h5>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> <span style='color: #2ecc71;'>==================================================</span></h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Günlük kâr tahmini için CatBoost modeli kullanılarak, 
en önemli etkenin günlük müşteri sayısı olduğu görüldü ve 
R² skoru %95.5 olarak elde edildi.</h5>""", unsafe_allow_html=True)



#########################################
# 4. R2 Model Sonuçları
#########################################

col1, col2 = st.columns(2)

col1.image("Hata Dağılım Grafiği.jpg", width=740, use_container_width=True) #tüm ekran için true yap

col2.markdown("<h1 style='text-align: center;'> </h1>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> <span style='color: #2ecc71;'>==================================================</span></h3>", unsafe_allow_html=True)
col2.markdown("<h5 style='text-align: center;'> CatBoost RMSE: 7085.7286</h5>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'> <span style='color: #2ecc71;'>==================================================</span></h3>", unsafe_allow_html=True)
col2.markdown("<h6 style='text-align: center;'> </h6>", unsafe_allow_html=True)
col2.markdown("""<h5 style='text-align: center;'>Modelin RMSE değeri, tahmin edilen günlük 
kâr ile gerçek kâr arasındaki ortalama sapmanın düşük olduğunu göstererek, modelin yüksek 
doğrulukla tahmin yaptığını ortaya koymaktadır.</h5>""", unsafe_allow_html=True)
