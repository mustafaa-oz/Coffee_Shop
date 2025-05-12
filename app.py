# app.py
import streamlit as st
import runpy
import os

# Uygulamanın genel ayarları
st.set_page_config(
    page_title="Miuul Coffee Shop",
    page_icon="☕",
    layout="wide"
)

# Sağ kenar çubuğunda gezinme menüsü
st.sidebar.title("🚀 Sayfalar")
pages = {
    "Anasayfa": "HomePage.py",
    "Sipariş": "Siparis.py",
    "Kâr Hesapla": "Kar_Hesapla.py",
    "Lokasyon": "Lokasyon.py",
    "Model Değerlendirme": "Model_degerlendirmesi.py"
}

choice = st.sidebar.radio("Menüden seçin", list(pages.keys()))

# Seçilen sayfanın dosyasını çalıştır
script_path = pages[choice]
if os.path.exists(script_path):
    runpy.run_path(script_path, run_name="__main__")
else:
    st.error(f"⚠️ {script_path} dosyası bulunamadı.")
