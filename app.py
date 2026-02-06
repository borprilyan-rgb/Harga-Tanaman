import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Tampilan Website
st.set_page_config(page_title="Canopy Landscape Directory", layout="wide")

st.title("🌱 Canopy: Intelligent Specimen Search")
st.write("Sistem pencarian cerdas untuk kebutuhan landscape dan tender.")

# 1. Load Data dari Excel
@st.cache_data
def load_data():
    # Pastikan nama file sesuai dengan file Excel kamu
    df = pd.read_excel("database_tanaman.xlsx") 
    return df

try:
    df = load_data()

    # 2. Sidebar untuk Input Pencarian
    st.sidebar.header("Kriteria Pencarian")
    nama_cari = st.sidebar.selectbox("Pilih Nama Tanaman", df['Nama Tanaman'].unique())
    tinggi_cari = st.sidebar.number_input("Target Tinggi (m)", min_value=0.0, step=0.1)
    diam_cari = st.sidebar.number_input("Target Diameter (m)", min_value=0.0, step=0.1)

    if st.sidebar.button("Cari Match Terdekat"):
        # Filter berdasarkan nama tanaman
        df_filter = df[df['Nama Tanaman'] == nama_cari].copy()

        if not df_filter.empty:
            # RUMUS: Menghitung jarak terdekat (Euclidean Distance)
            df_filter['selisih'] = np.sqrt(
                (df_filter['Tinggi (m)'] - tinggi_cari)**2 + 
                (df_filter['Diameter (m)'] - diam_cari)**2
            )
            
            # Ambil baris dengan selisih paling kecil
            hasil = df_filter.loc[df_filter['selisih'].idxmin()]

            # 3. Tampilkan Hasil
            st.subheader(f"Hasil Pencarian Terdekat: {nama_cari}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tinggi di Database", f"{hasil['Tinggi (m)']} m")
            with col2:
                st.metric("Diameter di Database", f"{hasil['Diameter (m)']} m")
            with col3:
                st.metric("Harga Estimasi", f"Rp {hasil['Harga']:,.0f}")
            
            st.info(f"Catatan: Tidak ditemukan t:{tinggi_cari} d:{diam_cari}. Menampilkan spesifikasi terdekat yang tersedia.")
        else:
            st.warning("Tanaman tidak ditemukan dalam database.")

except Exception as e:
    st.error(f"Gagal membaca database. Pastikan file 'database_tanaman.xlsx' ada di folder yang sama. Error: {e}")