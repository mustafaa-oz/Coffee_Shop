import streamlit as st
import numpy as np
import pandas as pd
import joblib

# 🌰 Arka Plan Görseli - Kahve Teması
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

# Model ve scaler'ı yükleyelim
model = joblib.load("kurlu_catboost_coffee_revenue_model.pkl")
scaler = joblib.load("kurlu_robust_scaler_model.pkl")

# Session state başlangıç değerleri
if "foot_traffic" not in st.session_state:
    st.session_state.foot_traffic = 0
if "num_customers" not in st.session_state:
    st.session_state.num_customers = 0
if "avg_order_value" not in st.session_state:
    st.session_state.avg_order_value = 0
if "operating_hours" not in st.session_state:
    st.session_state.operating_hours = 0
if "num_employees" not in st.session_state:
    st.session_state.num_employees = 0
if "marketing_spend" not in st.session_state:
    st.session_state.marketing_spend = 0

# LOGO VE SLOGAN:
col1, col2, col3 = st.columns(3)
col2.image("miul_son - Kopya.png", width=550, use_container_width=False)

st.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Günlük Kâr Hesaplama </h1>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center;'> </h5>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>İşletme Lokasyonunuzu Seçiniz: </h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'> </h5>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
if col2.button("Lokasyon 1 : Mavişehir"):
    col2.markdown("<h6 style='text-align: left;'>Konum Yaya Trafiği: 1500</h6>", unsafe_allow_html=True)
    col2.markdown("<h6 style='text-align: left;'>Ortalama Günlük Müşteri Sayısı: 300</h6>", unsafe_allow_html=True)
    col2.markdown("<h6 style='text-align: left;'>Ortalama Sipariş Tutarı: 210</h6>", unsafe_allow_html=True)
    st.session_state.foot_traffic = 1500
    st.session_state.num_customers = 300
    st.session_state.avg_order_value = 210

if col3.button("Lokasyon 2 : Bostanlı"):
    col3.markdown("<h6 style='text-align: left;'>Konum Yaya Trafiği: 2500</h6>", unsafe_allow_html=True)
    col3.markdown("<h6 style='text-align: left;'>Ortalama Günlük Müşteri Sayısı: 400</h6>", unsafe_allow_html=True)
    col3.markdown("<h6 style='text-align: left;'>Ortalama Sipariş Tutarı: 250</h6>", unsafe_allow_html=True)
    st.session_state.foot_traffic = 2500
    st.session_state.num_customers = 400
    st.session_state.avg_order_value = 250

if col4.button("Lokasyon 3 : Karşıyaka"):
    col4.markdown("<h6 style='text-align: left;'>Konum Yaya Trafiği: 3500</h6>", unsafe_allow_html=True)
    col4.markdown("<h6 style='text-align: left;'>Ortalama Günlük Müşteri Sayısı: 450</h6>", unsafe_allow_html=True)
    col4.markdown("<h6 style='text-align: left;'>Ortalama Sipariş Tutarı: 150</h6>", unsafe_allow_html=True)
    st.session_state.foot_traffic = 3500
    st.session_state.num_customers = 450
    st.session_state.avg_order_value = 150

col1, col2, col3 = st.columns(3)
col2.subheader(" ")
col2.markdown("<h3 style='text-align: center;'>İşletmenize Ait Günlük Verileri Giriniz: </h3>", unsafe_allow_html=True)
st.session_state.foot_traffic = col2.number_input("Konum Yaya Trafiği", min_value=0, value=st.session_state.foot_traffic, disabled=True)
st.session_state.num_customers = col2.number_input("Günlük Müşteri Sayısı", min_value=0, value=st.session_state.num_customers)
st.session_state.avg_order_value = col2.number_input("Ortalama Sipariş Tutarı (₺)", min_value=0, value=st.session_state.avg_order_value)
st.session_state.operating_hours = col2.number_input("Günlük Çalışma Saati", min_value=0, value=st.session_state.operating_hours)
st.session_state.num_employees = col2.number_input("Çalışan Sayısı", min_value=0, value=st.session_state.num_employees)
st.session_state.marketing_spend = col2.number_input("Günlük Pazarlama Harcaması (₺)", min_value=0, value=st.session_state.marketing_spend)

# Güvenli bölme fonksiyonu
def safe_divide(a, b, fill_value=0):
    result = np.zeros_like(a, dtype=float)
    mask = b != 0
    result[mask] = a[mask] / b[mask]
    result[~mask] = fill_value
    return result

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
if col4.button("💰 Tahmini Geliri Hesapla"):
    input_data = pd.DataFrame([{
        "Number_of_Customers_Per_Day": st.session_state.num_customers,
        "Average_Order_Value": st.session_state.avg_order_value,
        "Operating_Hours_Per_Day": st.session_state.operating_hours,
        "Number_of_Employees": st.session_state.num_employees,
        "Marketing_Spend_Per_Day": st.session_state.marketing_spend,
        "Location_Foot_Traffic": st.session_state.foot_traffic
    }])

    scaled_cols = [
        "Number_of_Customers_Per_Day",
        "Average_Order_Value",
        "Operating_Hours_Per_Day",
        "Number_of_Employees",
        "Marketing_Spend_Per_Day",
        "Location_Foot_Traffic"
    ]

    input_data_scaled = input_data.copy()
    input_data_scaled[scaled_cols] = scaler.transform(input_data[scaled_cols])

    input_data_scaled["Customers_Per_Employee"] = safe_divide(
        input_data_scaled["Number_of_Customers_Per_Day"],
        input_data_scaled["Number_of_Employees"],
        fill_value=input_data_scaled["Number_of_Customers_Per_Day"].mean()
    )

    input_data_scaled["Marketing_Per_Customer"] = safe_divide(
        input_data_scaled["Marketing_Spend_Per_Day"],
        input_data_scaled["Number_of_Customers_Per_Day"]
    )

    input_data_scaled["Customer_Traffic_Ratio"] = safe_divide(
        input_data_scaled["Number_of_Customers_Per_Day"],
        input_data_scaled["Location_Foot_Traffic"]
    )

    input_data_scaled["Total_Orders_Value"] = (
        input_data_scaled["Number_of_Customers_Per_Day"] * input_data_scaled["Average_Order_Value"]
    )

    input_data_scaled["Marketing_Order_Interaction"] = (
        input_data_scaled["Marketing_Spend_Per_Day"] * input_data_scaled["Average_Order_Value"]
    )

    predicted_revenue = model.predict(input_data_scaled)
    col1, col2, col3 = st.columns(3)
    col2.success(f"📈 Tahmini Günlük Gelir: ₺{(predicted_revenue[0] - (st.session_state.num_employees * 1000)) * (st.session_state.operating_hours / 10):,.2f}")