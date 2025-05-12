import streamlit as st
import runpy
import os

# Uygulama yapılandırması
st.set_page_config(
    page_title="Miuul Coffee Shop",
    page_icon="☕",
    layout="wide"
)

# Başlık ve açıklama
st.title("☕ Miuul Coffee Shop")
st.write("Sol taraftan istediğiniz sayfayı seçin.")

# Sidebar ile sayfa navigasyonu
st.sidebar.title("🚀 Sayfalar")
pages = {
    "Ana Sayfa": "HomePage.py",
    "Sipariş Ekranı": "Siparis.py",
    "Günlük Kâr Hesapla": "Kar_Hesapla.py",
    "Lokasyon (Admin)": "Lokasyon.py",
    "Model Değerlendirmesi": "Model_degerlendirmesi.py"
}

choice = st.sidebar.radio("Sayfa seçin", list(pages.keys()))
script_path = pages[choice]

if os.path.exists(script_path):
    runpy.run_path(script_path, run_name="__main__")
else:
    st.error(f"⚠️ {script_path} dosyası bulunamadı.")
