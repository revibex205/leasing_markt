import streamlit as st

st.set_page_config(
    page_title="LeaseMarkt — Bank-Approved Machinery",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

from data.state import init_state
from components.ui import render_sidebar_nav
from components.styles import inject_global_css

init_state()
inject_global_css()

# Render role switcher in sidebar above the navigation menu
render_sidebar_nav()

role = st.session_state.get("current_role", "public")

pages = {
    "Ziyaretçi Sayfaları": [
        st.Page("views/0_Home.py", title="Ana Sayfa", icon="🏠"),
        st.Page("views/1_Marketplace.py", title="Vitrin", icon="🔍"),
        st.Page("views/2_Machine_Detail.py", title="Makine Detayı", icon="📋"),
        st.Page("views/3_Lead_Form.py", title="Başvuru Formu", icon="📞"),
    ]
}

if role in ["seller", "bank"]:
    pages["Satıcı İşlemleri"] = [
        st.Page("views/4_Seller_Dashboard.py", title="Satıcı Paneli", icon="🗂️"),
        st.Page("views/5_Create_Listing.py", title="Yeni İlan Ekle", icon="➕"),
    ]

if role == "bank":
    pages["Banka Yönetimi"] = [
        st.Page("views/6_Bank_Review.py", title="İlan İnceleme", icon="⚖️"),
        st.Page("views/7_Admin_Dashboard.py", title="Admin Paneli", icon="📊"),
    ]

pg = st.navigation(pages)
pg.run()
