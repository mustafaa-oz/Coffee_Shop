# main.py veya app.py
import streamlit as st
import runpy, os

st.set_page_config(
    page_title="Miuul Coffee Shop",
    page_icon="☕",
    layout="wide",
)

st.sidebar.title("📑 Sayfalar")
pages = {
    "Ana Sayfa": "HomePage.py",
    "Siparis": "Siparis.py",
    "Kâr Hesapla": "Kar_Hesapla.py",
    "Lokasyon": "Lokasyon.py",
    "Model Değerlendirme": "Model_degerlendirmesi.py",
}

# Kullanıcı seçimi
choice = st.sidebar.radio("Sayfa seç", list(pages.keys()))
script_path = pages[choice]

# Seçilen dosyayı çalıştır
if os.path.exists(script_path):
    runpy.run_path(script_path, run_name="__main__")
else:
    st.error(f"⚠️ {script_path} bulunamadı.")
