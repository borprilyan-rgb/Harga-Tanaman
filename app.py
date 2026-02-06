import streamlit as st
import pandas as pd
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Canopy Landscape Directory", layout="wide", page_icon="🌱")

# --- KONEKSI GOOGLE SHEETS ---
GOOGLE_SHEET_ID = '1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro'
SHEET_NAME = 'Sheet1' 
url = f'https://docs.google.com/spreadsheets/d/1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro/gviz/tq?tqx=out:csv&sheet=Sheet1'

# --- FUNGSI LOAD DATA (Diletakkan di luar agar bisa dipanggil semua Tab) ---
@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(url)

st.title("🌱 Canopy: Intelligent Database")
st.markdown("---")

# Inisialisasi df agar tidak NameError
df = pd.DataFrame()

try:
    df = load_data()
    
    # --- TAB MENU ---
    tab1, tab2 = st.tabs(["🔍 Cari Tanaman", "➕ Tambah / Edit Data"])

    with tab1:
        st.sidebar.header("🔍 Filter Spesifikasi")
        
        if not df.empty:
            daftar_tanaman = sorted(df['Nama Tanaman'].unique())
            nama_cari = st.sidebar.selectbox("Pilih Jenis Tanaman", daftar_tanaman)
            tinggi_cari = st.sidebar.number_input("Target Tinggi (m)", min_value=0.0, step=0.1, value=2.0)
            diam_cari = st.sidebar.number_input("Target Diameter (m)", min_value=0.0, step=0.1, value=0.5)

            if st.sidebar.button("Cari Data Terdekat"):
                df_filter = df[df['Nama Tanaman'] == nama_cari].copy()
                if not df_filter.empty:
                    # Logika Euclidean Distance
                    df_filter['selisih'] = np.sqrt((df_filter['Tinggi (m)'] - tinggi_cari)**2 + (df_filter['Diameter (m)'] - diam_cari)**2)
                    hasil = df_filter.loc[df_filter['selisih'].idxmin()]

                    st.subheader(f"Hasil Pencarian untuk: {nama_cari}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Tinggi", f"{hasil['Tinggi (m)']} m")
                    c2.metric("Diameter", f"{hasil['Diameter (m)']} m")
                    c3.metric("Harga", f"Rp {hasil['Harga']:,.0f}")
                else:
                    st.warning("Data spesifik tanaman ini tidak ditemukan.")
        else:
            st.error("Database kosong. Silakan isi data di Google Sheets.")

    with tab2:
        st.subheader("Manajemen Database Tanaman")
        st.info("Klik tombol di bawah untuk membuka Google Sheets. Data yang kamu tambah di sana akan muncul di sini dalam 10 detik.")
        
        # Tombol Langsung ke Google Sheets
        link_sheets = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/edit"
        st.link_button("Buka Google Sheets (Tambah Data)", link_sheets)
        
        st.markdown("---")
        st.write("### Preview Database Saat Ini:")
        # Sekarang df sudah pasti terdefinisi
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Periksa koneksi atau ID Google Sheets kamu.")
    st.write(f"Detail Error: {e}")

st.markdown("---")
st.caption(f"Update terakhir: {pd.Timestamp.now().strftime('%H:%M:%S')}")
