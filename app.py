import streamlit as st
import pandas as pd
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Canopy Landscape Directory", layout="wide", page_icon="🌱")

# --- KONEKSI GOOGLE SHEETS ---
# ID yang diambil dari link yang kamu berikan
GOOGLE_SHEET_ID = '1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro'
SHEET_NAME = 'Sheet1' 

# URL untuk export ke CSV agar bisa dibaca Pandas
url = f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

# --- FUNGSI LOAD DATA ---
@st.cache_data(ttl=60) # Data refresh otomatis setiap 60 detik
def load_data():
    return pd.read_csv(url)

st.title("🌱 Canopy: Intelligent Landscape Search")
st.markdown("Sistem pencarian spesifikasi tanaman terdekat berbasis database Cloud.")
st.markdown("---")

try:
    # Memuat data dari Google Sheets
    df = load_data()
    
    # Sidebar untuk Input Pencarian
    st.sidebar.header("🔍 Filter Spesifikasi")
    
    # Mengambil daftar unik nama tanaman untuk dropdown
    daftar_tanaman = sorted(df['Nama Tanaman'].unique())
    nama_cari = st.sidebar.selectbox("Pilih Jenis Tanaman", daftar_tanaman)
    
    # Input kriteria yang dicari
    tinggi_cari = st.sidebar.number_input("Target Tinggi (m)", min_value=0.0, step=0.1, value=2.0)
    diam_cari = st.sidebar.number_input("Target Diameter (m)", min_value=0.0, step=0.1, value=0.5)

    if st.sidebar.button("Cari Data Terdekat"):
        # Filter data berdasarkan tanaman yang dipilih
        df_filter = df[df['Nama Tanaman'] == nama_cari].copy()

        if not df_filter.empty:
            # Algoritma Euclidean Distance untuk mencari yang paling mirip
            # Menghitung selisih antara input user dengan data di database
            df_filter['selisih'] = np.sqrt(
                (df_filter['Tinggi (m)'] - tinggi_cari)**2 + 
                (df_filter['Diameter (m)'] - diam_cari)**2
            )
            
            # Mengambil baris dengan nilai selisih terkecil
            hasil = df_filter.loc[df_filter['selisih'].idxmin()]

            # Tampilan Dashboard Hasil
            st.subheader(f"Hasil Pencarian untuk: {nama_cari}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tinggi di Database", f"{hasil['Tinggi (m)']} m")
            with col2:
                st.metric("Diameter di Database", f"{hasil['Diameter (m)']} m")
            with col3:
                st.metric("Estimasi Harga", f"Rp {hasil['Harga']:,.0f}")
            
            st.info(f"Sistem menampilkan data yang paling mendekati target (T:{tinggi_cari}m, D:{diam_cari}m).")
            
            # Tabel Riwayat/Alternatif (Menampilkan 5 yang terdekat)
            with st.expander("Lihat 5 Opsi Terdekat Lainnya"):
                tabel_tampil = df_filter.sort_values(by='selisih').head(5)
                st.table(tabel_tampil[['Nama Tanaman', 'Tinggi (m)', 'Diameter (m)', 'Harga']])
        else:
            st.warning(f"Tanaman '{nama_cari}' belum tersedia di database.")

    # Footer
    st.markdown("---")
    st.caption(f"Status: Terhubung ke Google Sheets | Update terakhir: {pd.Timestamp.now().strftime('%H:%M:%S')}")

except Exception as e:
    st.error("Koneksi gagal atau format kolom Google Sheets tidak sesuai.")
    st.write("Pastikan kolom di Google Sheets berjudul: **Nama Tanaman**, **Tinggi (m)**, **Diameter (m)**, dan **Harga**.")
    st.write(f"Detail Error: {e}")
