"""
views/4_Seller_Dashboard.py — Seller Listing Management Portal
Role-gated: seller context only. Tabs for all listing statuses.
"""

import streamlit as st
from datetime import date



from data.state import init_state, get_listings, get_machine
from data.models import ListingStatus
from components.styles import inject_global_css
from components.ui import (
    render_sidebar_nav, require_role, render_footer,
    status_chip_html, format_price, days_remaining, page_title, trust_badge_html,
)

init_state()
inject_global_css()

if not require_role("seller", "Satıcı Portalı — DemoBank LeaseMarkt"):
    render_footer()
    st.stop()

seller_id = st.session_state.get("current_seller_id", "S001")

page_title(
    "İlan Portalınız",
    "Satıcı Paneli",
    "Makine ilanlarınızı yönetin. Tüm ilanlar yayınlanmadan önce DemoBank incelemesine tabidir."
)

# ── Summary KPI row ───────────────────────────────────────────────────────────
all_seller_listings = get_listings(seller_id=seller_id)

kpi_cols = st.columns(7)
kpi_defs = [
    ("Toplam", len(all_seller_listings), "📋"),
    ("Taslak", len([l for l in all_seller_listings if l.status == ListingStatus.DRAFT]), "✏️"),
    ("Gönderildi", len([l for l in all_seller_listings if l.status == ListingStatus.SUBMITTED]), "📤"),
    ("Revizyon Bekleyen", len([l for l in all_seller_listings if l.status == ListingStatus.REVISION_REQUESTED]), "🔄"),
    ("Yayında", len([l for l in all_seller_listings if l.status == ListingStatus.LIVE]), "✅"),
    ("Süresi Dolmuş", len([l for l in all_seller_listings if l.status == ListingStatus.EXPIRED]), "⏱️"),
    ("Reddedildi", len([l for l in all_seller_listings if l.status == ListingStatus.REJECTED]), "❌"),
]
for i, (label, val, icon) in enumerate(kpi_defs):
    with kpi_cols[i]:
        st.html(f"""
<div class="kpi-card" style="padding:0.9rem;text-align:center;">
  <div class="kpi-icon" style="font-size:1.2rem;margin-bottom:0.25rem;">{icon}</div>
  <div class="kpi-value" style="font-size:1.6rem;">{val}</div>
  <div class="kpi-sub">{label}</div>
</div>
""")

st.html("""
<div class="alert-info" style="margin-top:0.5rem;font-size:0.8rem;">
  ⏱️ <strong>İlan Süresi Hakkında Not:</strong> Makine ilanları, banka onay tarihinden itibaren en fazla <strong>6 ay</strong> süreyle yayınlanabilir. 
  Süresi dolan ilanların incelenmek üzere yeniden oluşturulması gerekir.
</div>
""")

st.html("<br>")

# ── Eligible machines (from leasing history) ──────────────────────────────────
st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">⚙️ Leasing Geçmişinizden Listelenebilecek Makineler</div>')

from data.seed_data import MACHINE_MAP, SELLER_MAP
eligible_machines = [m for m in MACHINE_MAP.values() if m.seller_id == seller_id]
already_listed_machine_ids = {l.machine_id for l in all_seller_listings}

if eligible_machines:
    for machine in eligible_machines:
        listed = machine.machine_id in already_listed_machine_ids
        badge = '<span style="font-size:0.72rem;background:#F0FDF4;color:#166534;border:1px solid #BBF7D0;padding:2px 8px;border-radius:999px;font-weight:700;">Listelendi</span>' if listed else '<span style="font-size:0.72rem;background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;padding:2px 8px;border-radius:999px;font-weight:700;">Listelenebilir</span>'
        days_to_end = (machine.leasing_contract_end_date - date.today()).days
        days_str = f"Sözleşme {days_to_end} gün içinde bitiyor" if days_to_end > 0 else "Sözleşme bitti"

        elg_cols = st.columns([3, 2, 1, 1])
        with elg_cols[0]:
            st.html(f"""
<div style="font-size:0.9rem;font-weight:700;color:#0A1628;">{machine.brand} {machine.model}</div>
<div style="font-size:0.78rem;color:#8896A8;">{machine.category.value} · {machine.production_year}</div>
""")
        with elg_cols[1]:
            st.html(f'<div style="font-size:0.8rem;color:#4A5568;padding-top:0.3rem;">{days_str}</div>')
        with elg_cols[2]:
            st.html(f'<div style="padding-top:0.25rem;">{badge}</div>')
        with elg_cols[3]:
            if not listed:
                if st.button("+ Makine Listele", key=f"list_{machine.machine_id}", use_container_width=True):
                    st.session_state["create_listing_machine_id"] = machine.machine_id
                    st.session_state["create_listing_step"] = 1
                    st.switch_page("views/5_Create_Listing.py")

        st.html('<hr style="border:none;border-top:1px solid #EEF1F7;margin:0.4rem 0;">')
else:
    st.html('<div class="alert-info">Leasing geçmişinizde uygun makine bulunamadı.</div>')

st.html("<br>")

# ── Tabs for listing statuses ─────────────────────────────────────────────────
st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">📋 İlanlarınız</div>')

tab_labels = ["Tümü", "Taslak", "Gönderildi", "Revizyon İstenen", "Yayında", "Süresi Dolmuş", "Reddedildi"]
tabs = st.tabs(tab_labels)

status_filter_map = {
    "Taslak": [ListingStatus.DRAFT],
    "Gönderildi": [ListingStatus.SUBMITTED],
    "Revizyon İstenen": [ListingStatus.REVISION_REQUESTED],
    "Yayında": [ListingStatus.LIVE],
    "Süresi Dolmuş": [ListingStatus.EXPIRED],
    "Reddedildi": [ListingStatus.REJECTED],
}


def render_listing_row(listing, tab_index: int):
    machine = get_machine(listing.machine_id)
    if not machine:
        return

    days_left = days_remaining(listing.expires_at) if listing.status == ListingStatus.LIVE else ""
    price_str = format_price(listing.asking_price, listing.currency)
    approved_since = listing.approved_at.strftime("%d %b %Y") if listing.approved_at else "—"

    with st.container():
        st.html(f"""
<div style="background:white;border:1px solid #D6DCE8;border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem;">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
    <div>
      <div style="font-size:0.95rem;font-weight:700;color:#0A1628;">{machine.brand} {machine.model}</div>
      <div style="font-size:0.78rem;color:#8896A8;margin-top:2px;">
        {machine.production_year} · {listing.location_city} · {price_str}
        {"· <span style='color:#B45309;font-weight:700;background:#FFFBEB;padding:2px 6px;border-radius:4px;'>⏱️ " + days_left + "</span>" if days_left else ""}
      </div>
    </div>
    <div>{status_chip_html(listing.status)}</div>
  </div>
""")

        if listing.status == ListingStatus.REVISION_REQUESTED and listing.reviewer_comment:
            st.html(f"""
<div class="revision-box" style="margin-top:0.75rem;">
  <div class="rb-title">🔄 Banka Revizyon Talebi</div>
  <div class="rb-text">{listing.reviewer_comment}</div>
</div>
""")

        st.html("</div>")

        action_cols = st.columns(4)
        with action_cols[0]:
            if st.button("📋 Görüntüle", key=f"view_{listing.listing_id}_{tab_index}", use_container_width=True):
                st.session_state["selected_listing_id"] = listing.listing_id
                st.switch_page("views/2_Machine_Detail.py")
        with action_cols[1]:
            if listing.status in (ListingStatus.DRAFT, ListingStatus.REVISION_REQUESTED):
                if st.button("✏️ Düzenle ve Gönder", key=f"edit_{listing.listing_id}_{tab_index}", use_container_width=True):
                    st.session_state["edit_listing_id"] = listing.listing_id
                    st.session_state["create_listing_machine_id"] = listing.machine_id
                    st.switch_page("views/5_Create_Listing.py")


for tab_i, tab_label in enumerate(tab_labels):
    with tabs[tab_i]:
        if tab_label == "Tümü":
            filtered_listings = all_seller_listings
        else:
            filtered_listings = get_listings(status=status_filter_map[tab_label], seller_id=seller_id)

        if not filtered_listings:
            st.html(f'<div style="color:#8896A8;font-size:0.875rem;padding:1rem 0;">Bu kategoride ilan bulunamadı.</div>')
        else:
            for listing in sorted(filtered_listings, key=lambda x: x.created_at, reverse=True):
                render_listing_row(listing, tab_i)

st.html("<br>")
if st.button("➕ Yeni İlan Oluştur", type="primary"):
    st.session_state["create_listing_step"] = 1
    st.switch_page("views/5_Create_Listing.py")

render_footer()
