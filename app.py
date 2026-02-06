import streamlit as st
import pandas as pd
import numpy as np

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Canopy Landscape Directory", layout="wide", page_icon="🌱")

# --- 2. KONEKSI GOOGLE SHEETS (Membaca Data) ---
GOOGLE_SHEET_ID = '1bOJN0eShLtXvTFbnMhYYBzgBzKs03kblHDUOWw2bhro'
SHEET_NAME = 'Sheet1' 
url = f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

# --- 3. LINK GOOGLE FORM (Input Data) ---
# Link sudah saya ubah ke format 'viewform' agar bisa tampil di website
LINK_GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSca_MhXnFisX8_42Ea7Bf6Rz-zRIsU_Y7zF5rW-tO9R9-V87A/viewform?embedded=true"

@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(url)

st.title("🌱 Canopy: Intelligent Database")
st.markdown("---")

df = pd.DataFrame()

try:
    df = load_data()
    
    # --- TAB MENU ---
    tab1, tab2 = st.tabs(["🔍 Cari Tanaman", "➕ Input Data Baru"])

    with tab1:
        st.sidebar.header("🔍 Filter Spesifikasi")
        
        if not df.empty:
            # Dropdown Nama Tanaman
            daftar_tanaman = sorted(df['Nama Tanaman'].unique())
            nama_cari = st.sidebar.selectbox("Pilih Jenis Tanaman", daftar_tanaman)
            
            # Input kriteria
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
                    
                    st.info("Spesifikasi di atas adalah yang paling mendekati target Anda di database.")
                else:
                    st.warning("Data untuk tanaman ini belum tersedia.")
            
            st.markdown("---")
            st.write("### Database Aktif saat ini:")
            st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Input Data Tanaman Baru")
        st.write("Isi formulir di bawah ini. Data akan otomatis masuk ke Google Sheets dan terupdate di website ini dalam beberapa detik.")
        
        # Menampilkan Google Form secara rapi di dalam website
        st.components.v1.iframe(LINK_GOOGLE_FORM, height=800, scrolling=True)

except Exception as e:
    st.error(f"Gagal memuat data. Periksa koneksi atau ID Google Sheets.")
    st.write(f"Detail Error: {e}")

st.markdown("---")
st.caption(f"Update terakhir: {pd.Timestamp.now().strftime('%H:%M:%S')}")
