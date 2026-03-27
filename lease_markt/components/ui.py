"""
components/ui.py
Shared UI rendering functions for LeaseMarkt.
Uses st.html() for raw HTML injection and st.markdown() only for pure markdown.
"""

import streamlit as st
from datetime import date
from typing import Optional

from data.models import Listing, ListingStatus, Machine, SellerProfile, MachineCategory
from data.state import get_machine, get_seller


# ─── Role Navigation ──────────────────────────────────────────────────────────

ROLE_OPTIONS = {
    "🌐 Herkese Açık Görüntüleyen": "public",
    "🏭 Satıcı (Leasing Müşterisi)": "seller",
    "🏦 Banka Yöneticisi / İncelemeci": "bank",
}
ROLE_LABELS = {v: k for k, v in ROLE_OPTIONS.items()}


def render_sidebar_nav():
    """Render brand header, role switcher, and navigation links in the sidebar."""
    with st.sidebar:
        st.html("""
<div style="padding:1.2rem 0.5rem 0.8rem;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:1rem;">
  <div style="font-size:1.2rem;font-weight:800;color:white;letter-spacing:-0.01em;">
    Lease<span style="color:#F5B942;">Markt</span>
  </div>
  <div style="font-size:0.65rem;color:rgba(255,255,255,0.4);margin-top:3px;text-transform:uppercase;letter-spacing:0.09em;">
    Banka Onaylı Makine Platformu
  </div>
</div>
""")
        selected_label = st.selectbox(
            "GÖRÜNÜM",
            options=list(ROLE_OPTIONS.keys()),
            index=list(ROLE_OPTIONS.values()).index(
                st.session_state.get("current_role", "public")
            ),
            key="role_selector",
        )
        new_role = ROLE_OPTIONS[selected_label]
        if st.session_state.get("current_role") != new_role:
            st.session_state["current_role"] = new_role

        st.divider()

        role = st.session_state.get("current_role", "public")
        role_colors = {"public": "#3B82F6", "seller": "#2A63F6", "bank": "#F5B942"}
        role_name = ROLE_LABELS.get(role, "Unknown")
        st.html(f"""
<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:0.6rem 0.8rem;
     font-size:0.78rem;color:rgba(255,255,255,0.5);">
  <span style="color:{role_colors.get(role,'#fff')};font-weight:700;">● </span>
  Demo modu: {role_name}
</div>
""")


# ─── Trust Badges ─────────────────────────────────────────────────────────────

def trust_badge_html(level: str = "bank") -> str:
    configs = {
        "bank":     ("trust-badge-bank",     "🏦 DemoBank Onaylı"),
        "verified": ("trust-badge-verified",  "✅ Banka Onaylı Satıcı"),
        "gold":     ("trust-badge-gold",      "⭐ Banka Denetimli"),
    }
    css_class, label = configs.get(level, configs["bank"])
    return f'<span class="trust-badge {css_class}">{label}</span>'


def render_trust_badge(level: str = "bank"):
    st.html(trust_badge_html(level))


# ─── Status Chip ──────────────────────────────────────────────────────────────

STATUS_CSS = {
    ListingStatus.DRAFT:              "sc-draft",
    ListingStatus.SUBMITTED:          "sc-submitted",
    ListingStatus.REVISION_REQUESTED: "sc-revision",
    ListingStatus.APPROVED:           "sc-approved",
    ListingStatus.LIVE:               "sc-live",
    ListingStatus.REJECTED:           "sc-rejected",
    ListingStatus.EXPIRED:            "sc-expired",
    ListingStatus.CLOSED:             "sc-closed",
}


def status_chip_html(status: ListingStatus) -> str:
    css = STATUS_CSS.get(status, "sc-draft")
    return (
        f'<span class="status-chip {css}">'
        f'<span class="sc-dot"></span>{status.value}</span>'
    )


def render_status_chip(status: ListingStatus):
    st.html(status_chip_html(status))


# ─── Machine Category Icons ───────────────────────────────────────────────────

CATEGORY_ICONS = {
    MachineCategory.CONSTRUCTION:      "🏗️",
    MachineCategory.AGRICULTURAL:      "🌾",
    MachineCategory.MANUFACTURING:     "⚙️",
    MachineCategory.MATERIAL_HANDLING: "🏭",
    MachineCategory.PRINTING:          "🖨️",
    MachineCategory.FOOD_PROCESSING:   "🥫",
    MachineCategory.ENERGY:            "⚡",
    MachineCategory.TRANSPORT:         "🚛",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def format_price(price: float, currency: str = "TRY") -> str:
    symbol = "₺" if currency == "TRY" else currency
    return f"{symbol}{price:,.0f}"


def days_remaining(expires_at: Optional[date]) -> str:
    if not expires_at:
        return "—"
    delta = (expires_at - date.today()).days
    if delta < 0:
        return "Süresi Doldu"
    if delta == 0:
        return "Bugün Doluyor"
    return f"{delta} gün kaldı"


# ─── Machine Card ─────────────────────────────────────────────────────────────

def render_machine_card(listing: Listing, show_select_btn: bool = True, rerun_on_click: bool = False):
    """Render a public-safe machine discovery card."""
    machine = get_machine(listing.machine_id)
    seller  = get_seller(listing.seller_id)
    if not machine or not seller:
        return

    icon      = CATEGORY_ICONS.get(machine.category, "🔧")
    price_str = format_price(listing.asking_price, listing.currency)
    days_left = days_remaining(listing.expires_at)

    with st.container(border=True):
        st.html(f"""
<div class="card-img-bleed">{icon}</div>
<div class="machine-card-category">{machine.category.value}</div>
<div class="machine-card-title">{machine.brand} {machine.model}</div>
<div class="machine-card-meta">
  <span>📅 {machine.production_year}</span>
  <span>📍 {listing.location_city}</span>
  {"<span>⏱️ " + f"{machine.engine_hours:,} saat</span>" if machine.engine_hours else ""}
</div>
<div class="machine-card-price">{price_str}</div>
<div class="machine-card-footer">
  <span>{trust_badge_html("bank")}</span>
  <span>{days_left}</span>
</div>
""")

        if show_select_btn:
            if st.button(
                "Detayları Gör →",
                key=f"card_btn_{listing.listing_id}",
                use_container_width=True,
            ):
                st.session_state["selected_listing_id"]  = listing.listing_id
                st.session_state["selected_machine_id"]  = listing.machine_id
                if rerun_on_click:
                    st.rerun()
                else:
                    st.switch_page("views/2_Machine_Detail.py")


# ─── Quality Score Ring ───────────────────────────────────────────────────────

def quality_score_html(score: int) -> str:
    if score >= 85:
        ring_class, label = "score-ring-high", "Mükemmel"
    elif score >= 65:
        ring_class, label = "score-ring-mid",  "İyi"
    else:
        ring_class, label = "score-ring-low",  "Ortalama Altı"
    return (
        f'<div style="display:flex;align-items:center;gap:0.75rem;">'
        f'<div class="score-ring {ring_class}">{score}</div>'
        f'<div><div style="font-size:0.78rem;font-weight:700;color:#4A5568;">Kalite Puanı</div>'
        f'<div style="font-size:0.95rem;font-weight:800;color:#0A1628;">{label}</div></div></div>'
    )


# ─── Price Reasonableness Indicator ──────────────────────────────────────────

def price_reasonableness_html(asking: float, reference: float) -> str:
    diff_pct = ((asking - reference) / reference) * 100
    if diff_pct > 15:
        color, label, icon = "#DC2626", f"Piyasanın %{diff_pct:.0f} üzerinde", "⚠️"
    elif diff_pct < -10:
        color, label, icon = "#16A34A", f"Piyasanın %{abs(diff_pct):.0f} altında", "✅"
    else:
        color, label, icon = "#D97706", f"Piyasa aralığında (%{diff_pct:+.0f})", "ℹ️"
    return (
        f'<div style="background:#F8F9FC;border:1px solid #D6DCE8;border-radius:10px;padding:0.75rem 1rem;">'
        f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#8896A8;margin-bottom:0.25rem;">Fiyat Uygunluğu</div>'
        f'<div style="font-size:0.9rem;font-weight:700;color:{color};">{icon} {label}</div>'
        f'<div style="font-size:0.76rem;color:#8896A8;margin-top:0.2rem;">Piyasa ref: ₺{reference:,.0f} · İstek: ₺{asking:,.0f}</div>'
        f'</div>'
    )


# ─── Role Gate ────────────────────────────────────────────────────────────────

def require_role(required_role: str, label: str = "") -> bool:
    role = st.session_state.get("current_role", "public")
    if role == required_role:
        if required_role == "seller":
            banner_class = "role-banner-seller"
            icon = "🏭"
            lbl  = label or "Satıcı Portalı"
            subtext = "Bu sayfayı doğrulanmış DemoBank Leasing Müşterisi olarak görüntülüyorsunuz."
        else:
            banner_class = "role-banner-bank"
            icon = "🏦"
            lbl  = label or "Banka Yönetim Paneli"
            subtext = "İÇ GÖRÜNÜM — Gizli Banka Verileri Gösterilmektedir"
            
        st.html(f'''
<div class="role-banner {banner_class}">
  <div><span style="font-size:1.5rem;margin-right:0.5rem;">{icon}</span></div>
  <div>
    <div style="font-size:0.95rem;font-weight:800;">{lbl}</div>
    <div style="font-size:0.75rem;opacity:0.85;margin-top:2px;">{subtext}</div>
  </div>
</div>
''')
        return True

    role_name = "Satıcı" if required_role == "seller" else "Banka Yöneticisi"
    st.html(
        f'<div class="alert-warning">🔒 <strong>Erişim Engellendi:</strong> Bu sayfaya yalnızca <strong>{role_name}</strong> yetkisine sahip kullanıcılar erişebilir. '
        f'Test işlemine devam etmek için lütfen sol menüden rolünüzü değiştirin.</div>'
    )
    return False


# ─── Page Title ───────────────────────────────────────────────────────────────

def page_title(eyebrow: str, title: str, subtitle: str = ""):
    sub_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    st.html(f"""
<div style="margin-bottom:1.5rem;">
  <div class="section-eyebrow">{eyebrow}</div>
  <div class="section-title">{title}</div>
  {sub_html}
</div>
""")


# ─── Footer ───────────────────────────────────────────────────────────────────

def render_footer():
    st.html("""
<div class="lm-footer">
  <strong>LeaseMarkt</strong> — Bir <strong>DemoBank A.Ş.</strong> hizmetidir.<br>
  Tüm ilanlar yayınlanmadan önce banka tarafından incelenir ve onaylanır.
  Bu platform doğrudan çevrimiçi satın alma, ödeme veya bağlayıcı finansal taahhütler sağlamaz.
  Leasing şartları ve kampanya oranları yalnızca gösterge niteliğindedir ve banka değerlendirmesine tabidir.
  Satıcı bilgileri veri gizliliği politikası uyarınca gizlenmiştir.<br>
  <span style="font-size:0.7rem;opacity:0.45;">
    © 2026 DemoBank A.Ş. · BDDK Lisanslı · Prototip Demo — Yalnızca Sentetik Veri
  </span>
</div>
""")
