"""
views/1_Marketplace.py — Public Machine Catalogue
Search, filter, and browse all bank-approved live listings.
"""

import streamlit as st



from data.state import init_state, get_public_listings, get_machine
from data.models import MachineCategory
from components.styles import inject_global_css
from components.ui import (
    render_sidebar_nav, render_machine_card, trust_badge_html,
    render_footer, format_price, CATEGORY_ICONS, page_title,
)

init_state()
inject_global_css()

# ── Page header ──────────────────────────────────────────────────────────────
page_title("Herkese Açık Pazaryeri", "Onaylı Makineleri İnceleyin", "Tüm ilanlar yayınlanmadan önce DemoBank tarafından incelenip onaylanmıştır.")

# ── Load data ────────────────────────────────────────────────────────────────
all_live = get_public_listings()
all_machines = [get_machine(l.machine_id) for l in all_live]

# ── Filter sidebar ────────────────────────────────────────────────────────────
filter_col, results_col = st.columns([1, 3], gap="large")

with filter_col:
    st.html("""
<div style="background:white;border:1px solid #D6DCE8;border-radius:14px;padding:1.2rem;margin-bottom:1rem;">
  <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#8896A8;margin-bottom:1rem;">
    🔽 İlanları Filtrele
  </div>
""")

    # Search
    search = st.text_input(
        "Ara",
        value=st.session_state.get("marketplace_search", ""),
        placeholder="Marka, model, kelime...",
    )
    st.session_state["marketplace_search"] = search

    # Category filter
    categories = ["Tüm Kategoriler"] + [c.value for c in MachineCategory]
    preselect_cat = st.session_state.get("marketplace_category", "Tüm Kategoriler")
    if preselect_cat not in categories:
        preselect_cat = "Tüm Kategoriler"
    st.session_state["marketplace_category"] = ""  # clear after use

    category = st.selectbox("Kategori", categories, index=categories.index(preselect_cat))

    # Year range
    all_years = sorted({m.production_year for m in all_machines if m})
    if all_years:
        year_min, year_max = st.select_slider(
            "Üretim Yılı",
            options=all_years,
            value=(min(all_years), max(all_years)),
        )
    else:
        year_min, year_max = 2015, 2025

    # Price range
    all_prices = [l.asking_price for l in all_live]
    if all_prices:
        price_min = int(min(all_prices))
        price_max = int(max(all_prices))
        price_range = st.slider(
            "Talep Edilen Fiyat (₺)",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=50_000,
            format="₺%d",
        )
    else:
        price_range = (0, 10_000_000)

    # Location
    all_cities = sorted({l.location_city for l in all_live})
    location = st.selectbox("Konum", ["Tüm Şehirler"] + all_cities)

    st.html("</div>")

    # Sort
    sort_by = st.selectbox(
        "Sıralama Ölçütü",
        ["En Yeniler", "Fiyat: Düşük → Yüksek", "Fiyat: Yüksek → Düşük", "Yıl: En Yeniler"],
    )

    # Clear filters
    if st.button("↺ Filtreleri Sıfırla", use_container_width=True):
        st.session_state["marketplace_search"] = ""
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = []
for listing in all_live:
    machine = get_machine(listing.machine_id)
    if not machine:
        continue

    # Text search
    if search:
        search_lc = search.lower()
        searchable = f"{machine.brand} {machine.model} {machine.description} {machine.category.value}".lower()
        if search_lc not in searchable:
            continue

    # Category
    if category != "Tüm Kategoriler" and machine.category.value != category:
        continue

    # Year
    if not (year_min <= machine.production_year <= year_max):
        continue

    # Price
    if not (price_range[0] <= listing.asking_price <= price_range[1]):
        continue

    # Location
    if location != "Tüm Şehirler" and listing.location_city != location:
        continue

    filtered.append((listing, machine))

# ── Sort ──────────────────────────────────────────────────────────────────────
if sort_by == "Fiyat: Düşük → Yüksek":
    filtered.sort(key=lambda x: x[0].asking_price)
elif sort_by == "Fiyat: Yüksek → Düşük":
    filtered.sort(key=lambda x: x[0].asking_price, reverse=True)
elif sort_by == "Yıl: En Yeniler":
    filtered.sort(key=lambda x: x[1].production_year, reverse=True)
else:  # Newest First (by created_at)
    filtered.sort(key=lambda x: x[0].created_at, reverse=True)

# ── Results ───────────────────────────────────────────────────────────────────
with results_col:
    result_count = len(filtered)
    st.html(
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">'
        f'<div style="font-size:0.9rem;font-weight:600;color:#4A5568;">'
        f'<strong style="color:#0A1628;">{result_count}</strong> ilan bulundu'
        f'<span style="margin-left:0.5rem;">{trust_badge_html("bank")}</span></div>'
        f'</div>'
    )

    if not filtered:
        st.html("""
<div style="background:white;border:1px solid #D6DCE8;border-radius:14px;padding:3rem;text-align:center;color:#8896A8;">
  <div style="font-size:2rem;margin-bottom:0.5rem;">🔍</div>
  <div style="font-weight:700;font-size:1rem;color:#4A5568;margin-bottom:0.25rem;">Filtrelerinizle eşleşen ilan bulunamadı</div>
  <div style="font-size:0.85rem;">Filtreleri veya arama terimini değiştirmeyi deneyin.</div>
</div>
""")
    else:
        # Display 3 cards per row
        for row_start in range(0, len(filtered), 3):
            row_items = filtered[row_start: row_start + 3]
            cols = st.columns(3)
            for i, (listing, machine) in enumerate(row_items):
                with cols[i]:
                    render_machine_card(listing, show_select_btn=True)

render_footer()
