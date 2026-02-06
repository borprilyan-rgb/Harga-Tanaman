import streamlit as st
import pandas as pd
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Canopy Landscape Directory", layout="wide")

# --- BAGIAN YANG HARUS KAMU UBAH ---
# Ganti kode di bawah ini dengan ID Google Sheets kamu
GOOGLE_SHEET_ID = '1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro'
SHEET_NAME = 'Sheet1'  # Pastikan nama sheet di bawah (tab) adalah Sheet1

# URL untuk mengambil data sebagai CSV
url = f'https://docs.google.com/spreadsheets/d/1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro/edit?gid=0#gid=0'

# --- FUNGSI LOAD DATA ---
@st.cache_data(ttl=60) # Refresh data tiap 60 detik
def load_data():
    return pd.read_csv(url)

st.title("🌱 Canopy: Intelligent Landscape Search")
st.markdown("---")

try:
    # Memuat data
    df = load_data()
    
    # Sidebar untuk Input
    st.sidebar.header("🔍 Input Spesifikasi")
    
    # Dropdown Nama Tanaman (Otomatis ambil dari Google Sheets)
    daftar_tanaman = df['Nama Tanaman'].unique()
    nama_cari = st.sidebar.selectbox("Pilih Jenis Tanaman", daftar_tanaman)
    
    # Input Tinggi dan Diameter
    tinggi_cari = st.sidebar.number_input("Target Tinggi (m)", min_value=0.0, step=0.1, value=1.0)
    diam_cari = st.sidebar.number_input("Target Diameter (m)", min_value=0.0, step=0.1, value=0.5)

    if st.sidebar.button("Cari Match Terdekat"):
        # Filter data berdasarkan nama yang dipilih
        df_filter = df[df['Nama Tanaman'] == nama_cari].copy()

        if not df_filter.empty:
            # RUMUS: Euclidean Distance (Mencari jarak terpendek/paling mirip)
            df_filter['selisih'] = np.sqrt(
                (df_filter['Tinggi (m)'] - tinggi_cari)**2 + 
                (df_filter['Diameter (m)'] - diam_cari)**2
            )
            
            # Ambil baris dengan selisih terkecil
            hasil = df_filter.loc[df_filter['selisih'].idxmin()]

            # Menampilkan Hasil ke Dashboard
            st.subheader(f"Hasil Terbaik untuk: {nama_cari}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tinggi di Database", f"{hasil['Tinggi (m)']} m")
            with col2:
                st.metric("Diameter di Database", f"{hasil['Diameter (m)']} m")
            with col3:
                st.metric("Estimasi Harga", f"Rp {hasil['Harga']:,.0f}")
            
            st.success(f"Ditemukan spesifikasi yang paling mendekati di database.")
            
            # Menampilkan Tabel Pembanding (Opsional)
            with st.expander("Lihat perbandingan data lainnya"):
                st.dataframe(df_filter.sort_values(by='selisih').head(5))
        else:
            st.error("Data tanaman tersebut tidak ditemukan.")

    # Bagian Footer/Informasi Database
    st.markdown("---")
    st.caption(f"Status: Terkoneksi ke Google Sheets. Terakhir diupdate: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

except Exception as e:
    st.error("Gagal terhubung ke Google Sheets.")
    st.info("Pastikan ID Google Sheets benar dan aksesnya sudah 'Anyone with the link can view'.")
    st.write(f"Error Detail: {e}")
