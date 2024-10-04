import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Memuat dataset
@st.cache_data
def load_data():
    main_data = pd.read_csv('./main_data.csv')
    main_data['order_purchase_timestamp'] = pd.to_datetime(main_data['order_purchase_timestamp'])
    return main_data

all_data = load_data()

st.title("Proyek Analisis Data: E-Commerce Public Dataset 🛒")

# Pemisah 
st.write("<hr style='margin-bottom: 20px;'>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("img/ecommerce.jpg", use_column_width=True)
st.sidebar.title("Halaman")
page = st.sidebar.radio("Pilih halaman:", ("Musim Pemesanan", "Kategori Produk Berdasarkan Musim"))

# Konten halaman awal
st.write("<h3 style='margin-bottom: 10px;'>Proyek ini memberikan pertanyaan bisnis terkait e-commerce</h3>", unsafe_allow_html=True)
st.write("<h4 style='margin-bottom: 5px;'>- Musim apakah pengguna sering melakukan pemesanan di e-commerce?</h4>", unsafe_allow_html=True)
st.write("<h4 style='margin-bottom: 5px;'>- Kategori produk apa yang sering dipesan pengguna e-commerce berdasarkan musim?</h4>", unsafe_allow_html=True)
st.caption("Untuk penjelasan lengkapnya terdapat pada bagian sidebar")

# Pemisah
st.write("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

# Konten Halaman
if page == "Musim Pemesanan":
    st.subheader("Musim apakah pengguna sering melakukan pemesanan di e-commerce?")
    st.write("<h5 style='margin-bottom: 5px;'>Untuk menjawab pertanyaan di atas, perhatikan diagram berikut</h5>", unsafe_allow_html=True)

    orders_df = all_data.copy()
    orders_df['order_month'] = orders_df['order_purchase_timestamp'].dt.month

    def get_season(month):
        if month in [3, 4, 5]:
            return 'Musim Semi'
        elif month in [6, 7, 8]:
            return 'Musim Panas'
        elif month in [9, 10, 11]:
            return 'Musim Gugur'
        elif month in [12, 1, 2]:
            return 'Musim Dingin'
        else:
            return 'Tidak Diketahui'

    orders_df['season'] = orders_df['order_month'].apply(get_season)

    season_counts = orders_df['season'].value_counts()

    # Visualisasi data
    plt.figure(figsize=(10, 6))
    plt.pie(season_counts, labels=season_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Persentase Pesanan Pengguna Berdasarkan Musim', fontsize=16)
    plt.axis('equal')
    st.pyplot(plt)

    st.write("<h6 style='margin-bottom: 5px;'>Berdasarkan waktu pembelian, Musim Panas menjadi periode paling produktif dengan kontribusi {30,8%} terhadap total pesanan, diikuti oleh Musim Semi dengan {30,1%}. Sebaliknya, Musim Dingin dan Musim Gugur menunjukkan volume pesanan yang lebih rendah, yakni {22,4%} dan {16,8%}. Data tersebut menunjukkan pentingnya fokus pada promosi produk rumah tangga selama musim panas dan semi untuk meningkatkan penjualan di e-commerce. </h6>", unsafe_allow_html=True)


elif page == "Kategori Produk Berdasarkan Musim":
    st.subheader("Kategori produk apa yang sering dipesan pengguna e-commerce berdasarkan musim?")
    st.write("<h5 style='margin-bottom: 5px;'>Untuk menjawab pertanyaan di atas, perhatikan beberapa diagram berikut</h5>", unsafe_allow_html=True)

    products_df = all_data.copy()
    season_product_category = products_df.groupby(by=["season", "product_category_name_english"]).order_id.nunique().reset_index()
    top_season_product_categories = season_product_category.sort_values(by=["season", "order_id"], ascending=[True, False])
    
    # Visualisasi data dengan bahasa
    plt.figure(figsize=(16, 12))
    unique_seasons = top_season_product_categories['season'].unique()

    for i, season in enumerate(unique_seasons):
        plt.subplot(2, 2, i + 1)
        season_data = top_season_product_categories[top_season_product_categories['season'] == season].head(5)
        sns.barplot(
            x='order_id',
            y='product_category_name_english',
            data=season_data,
            color='#1f77b4'
        )
        plt.title(f'5 Kategori Produk Teratas di Musim {season}', fontsize=14)
        plt.xlabel('Jumlah Pesanan', fontsize=12)
        plt.ylabel('Kategori Produk', fontsize=12)
        plt.xlim(0, season_data['order_id'].max() + 10)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    #visualisasi data
    plt.tight_layout()
    st.pyplot(plt)

    st.write("<h6 style='margin-bottom: 5px;'>Analisis menunjukkan bahwa kategori produk bed_bath_table, health_beauty, dan sports_leisure mendominasi penjualan di semua musim. Ini mengindikasikan bahwa konsumen secara konsisten tertarik pada produk-produk ini sepanjang tahun. Oleh karena itu, pengembangan strategi pemasaran yang berfokus pada kategori tersebut setiap musim dapat memberikan peluang besar untuk meningkatkan penjualan dalam e-commerce. </h6>", unsafe_allow_html=True)

# Pemisah 
st.write("<hr style='margin-bottom: 20px;'>", unsafe_allow_html=True)

st.caption('Copyright (c) Ariestio Dava Pratama')
