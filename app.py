import streamlit as st
import pandas as pd
import numpy as np

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Daftar Tanaman", layout="wide", page_icon="🌱")

# --- 2. KONEKSI GOOGLE SHEETS ---
GOOGLE_SHEET_ID = '1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro'
SHEET_NAME = 'Sheet1' 
url = f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(url)

st.title("🌱 Daftar Tanaman")
st.markdown("Sistem ini sekarang memberikan 3 opsi referensi untuk memudahkan pengambilan keputusan tender.")
st.markdown("---")

try:
    df = load_data()
    
    # Sidebar Input
    st.sidebar.header("🔍 Kriteria Target")
    daftar_tanaman = sorted(df['Nama Tanaman'].unique())
    nama_cari = st.sidebar.selectbox("Pilih Jenis Tanaman", daftar_tanaman)
    t_target = st.sidebar.number_input("Target Tinggi (m)", min_value=0.0, step=0.1, value=2.0)
    d_target = st.sidebar.number_input("Target Diameter (m)", min_value=0.0, step=0.1, value=0.5)

    if st.sidebar.button("Cari Referensi"):
        df_filter = df[df['Nama Tanaman'] == nama_cari].copy()
        
        if not df_filter.empty:
            # --- PERHITUNGAN 3 METODE ---
            
            # 1. Euclidean (Keseimbangan Tinggi & Diameter)
            df_filter['dist_euclidean'] = np.sqrt((df_filter['Tinggi (m)'] - t_target)**2 + (df_filter['Diameter (m)'] - d_target)**2)
            match_all = df_filter.loc[df_filter['dist_euclidean'].idxmin()]

            # 2. Nearest Height (Hanya Tinggi)
            df_filter['dist_height'] = abs(df_filter['Tinggi (m)'] - t_target)
            match_height = df_filter.loc[df_filter['dist_height'].idxmin()]

            # 3. Nearest Diameter (Hanya Diameter)
            df_filter['dist_diam'] = abs(df_filter['Diameter (m)'] - d_target)
            match_diam = df_filter.loc[df_filter['dist_diam'].idxmin()]

            # --- TAMPILAN HASIL ---
            st.subheader(f"Hasil Analisis Spesifikasi: {nama_cari}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("🎯 **Keseimbangan Terbaik** (Euclidean)")
                st.write(f"Tinggi: {match_all['Tinggi (m)']} m")
                st.write(f"Diam: {match_all['Diameter (m)']} m")
                st.metric("Harga", f"Rp {match_all['Harga']:,.0f}")
                st.caption("Paling mirip secara keseluruhan.")

            with col2:
                st.success("📏 **Tinggi Paling Pas**")
                st.write(f"Tinggi: {match_height['Tinggi (m)']} m")
                st.write(f"Diam: {match_height['Diameter (m)']} m")
                st.metric("Harga", f"Rp {match_height['Harga']:,.0f}")
                st.caption("Prioritas pada target tinggi.")

            with col3:
                st.warning("⭕ **Diameter Paling Pas**")
                st.write(f"Tinggi: {match_diam['Tinggi (m)']} m")
                st.write(f"Diam: {match_diam['Diameter (m)']} m")
                st.metric("Harga", f"Rp {match_diam['Harga']:,.0f}")
                st.caption("Prioritas pada target diameter.")
            
            st.markdown("---")
            st.write("### Perbandingan Data Lengkap")
            st.dataframe(df_filter[['Nama Tanaman', 'Tinggi (m)', 'Diameter (m)', 'Harga', 'Stok']], use_container_width=True)
            
        else:
            st.warning("Tanaman tidak ditemukan.")

except Exception as e:
    st.error(f"Error: {e}")

st.caption(f"Challenge Accepted | Boris Prilyan | Last Sync: {pd.Timestamp.now().strftime('%H:%M:%S')}")

