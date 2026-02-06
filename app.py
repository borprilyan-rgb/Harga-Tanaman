import streamlit as st
import pandas as pd
import numpy as np

st.title("🌱 Canopy: Real-time Database")

# 1. Masukkan Link Google Sheets kamu di sini
# Ganti 'ID_PANJANG_DI_SINI' dengan ID dari link Google Sheets kamu
SHEET_ID = 'ID_PANJANG_DI_SINI'
SHEET_NAME = 'Sheet1' # Sesuaikan dengan nama sheet kamu
url = f'https://docs.google.com/spreadsheets/d/1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro/edit?gid=0#gid=0'

@st.cache_data(ttl=60) # Data akan otomatis refresh setiap 60 detik
def load_data():
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
    st.success("Tersambung ke Google Sheets!")
    
    # --- Lanjutkan dengan logika pencarian seperti sebelumnya ---
    # (Copy paste kode pencarian Euclidean Distance kamu di sini)
    
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan link Google Sheets benar. Error: {e}")
