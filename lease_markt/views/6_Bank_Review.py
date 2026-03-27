"""
views/6_Bank_Review.py — Bank Listing Review & Approval Panel
Role-gated: bank admin only.
Shows pending queue, internal quality score, price reasonableness, and action buttons.
"""

import streamlit as st
from datetime import datetime



from data.state import init_state, get_listings, get_machine, get_seller, update_listing_status, get_review_actions
from data.models import ListingStatus
from components.styles import inject_global_css
from components.ui import (
    render_sidebar_nav, require_role, render_footer,
    status_chip_html, format_price, quality_score_html,
    price_reasonableness_html, page_title, trust_badge_html,
)

init_state()
inject_global_css()

if not require_role("bank", "Banka İnceleme ve Onay Paneli"):
    render_footer()
    st.stop()

page_title(
    "🏦 İç İnceleme Paneli",
    "İlan İnceleme Sırası",
    "Gönderilen ilanları yayınlanmadan önce inceleyin. İç kalite puanları yalnızca bu panelde görülebilir.",
)

# ── Review queue tabs ─────────────────────────────────────────────────────────
tab_pending, tab_revision, tab_live, tab_history = st.tabs([
    "⏳ Bekleyen İncelemeler",
    "🔄 Revizyon İstenenler",
    "✅ Onaylı / Yayında",
    "📋 Tüm İlanlar",
])


def render_review_card(listing, show_actions: bool = True, reviewer_name: str = "K. Arslan"):
    machine = get_machine(listing.machine_id)
    seller = get_seller(listing.seller_id)
    if not machine or not seller:
        return

    icon = "🏗️🌾⚙️🏭🖨️🥫⚡🚛".split()[0]  # fallback
    from components.ui import CATEGORY_ICONS
    icon = CATEGORY_ICONS.get(machine.category, "🔧")

    with st.expander(
        f"{icon}  {machine.brand} {machine.model}  ·  {format_price(listing.asking_price)}  ·  {status_chip_html(listing.status)}",
        expanded=False,
    ):
        detail_col, action_col = st.columns([3, 2], gap="large")

        with detail_col:
            # Machine snapshot
            st.html(f"""
<div style="background:#F8F9FC;border:1px solid #D6DCE8;border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.75rem;">
  <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.5rem;">Makine Detayları</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.35rem 1.5rem;font-size:0.85rem;">
    <div><span style="color:#8896A8;">Marka / Model:</span> <strong>{machine.brand} {machine.model}</strong></div>
    <div><span style="color:#8896A8;">Kategori:</span> {machine.category.value}</div>
    <div><span style="color:#8896A8;">Yıl:</span> {machine.production_year}</div>
    <div><span style="color:#8896A8;">Seri No:</span> {machine.serial_number}</div>
    <div><span style="color:#8896A8;">Saat:</span> {f"{machine.engine_hours:,}" if machine.engine_hours else "N/A"}</div>
    <div><span style="color:#8896A8;">Konum:</span> {listing.location_city}, {listing.location_region}</div>
    <div><span style="color:#8896A8;">İlan ID:</span> {listing.listing_id}</div>
  </div>
</div>
""")

            # Seller info (unmasked for bank)
            st.html(f"""
<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;padding:0.9rem 1.1rem;margin-bottom:0.75rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#B45309;margin-bottom:0.4rem;">
    🔒 Satıcı Bilgileri (Sadece Banka Kullanımı İçindir)
  </div>
  <div style="font-size:0.85rem;color:#92400E;">
    <strong>Gizlenen Ad:</strong> {seller.masked_name}<br>
    <strong>Şehir:</strong> {seller.city}<br>
    <strong>Leasing Müşterisi Başlangıcı:</strong> {seller.leasing_customer_since}<br>
    <strong>Doğrulanmış:</strong> {"✅ Evet" if seller.verified else "❌ Hayır"}
  </div>
</div>
""")

            # Machine description
            st.html(f"""
<div style="margin-bottom:0.75rem;">
  <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#8896A8;margin-bottom:0.3rem;">Açıklama</div>
  <div style="font-size:0.85rem;color:#4A5568;line-height:1.6;">{machine.description}</div>
</div>
""")

            if listing.condition_notes:
                st.html(f"""
<div style="margin-bottom:0.75rem;">
  <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#8896A8;margin-bottom:0.3rem;">Satıcı Durum Notları</div>
  <div style="font-size:0.85rem;color:#4A5568;">{listing.condition_notes}</div>
</div>
""")

            # Revision history
            if listing.revision_history:
                st.html('<div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#B45309;margin-bottom:0.3rem;">Revizyon Geçmişi</div>')
                for entry in listing.revision_history:
                    st.html(f'<div style="font-size:0.8rem;color:#92400E;background:#FFFBEB;border-radius:8px;padding:5px 10px;margin-bottom:4px;">↩ {entry}</div>')

        with action_col:
            # Internal quality score (bank-only)
            st.html(quality_score_html(machine.internal_quality_score))
            st.html("<br>")

            # Price reasonableness
            st.html(
                price_reasonableness_html(listing.asking_price, machine.market_reference_price)
            )
            st.html("<br>")

            # Submission timeline
            st.html(f"""
<div style="font-size:0.78rem;color:#8896A8;margin-bottom:0.75rem;">
  📅 Oluşturulma: {listing.created_at.strftime("%d %b %Y %H:%M")}<br>
  📤 Gönderilme: {listing.submitted_at.strftime("%d %b %Y %H:%M") if listing.submitted_at else "—"}
</div>
""")

            if show_actions and listing.status in (ListingStatus.SUBMITTED, ListingStatus.REVISION_REQUESTED):
                st.markdown("---")
                st.html('<div style="font-size:0.8rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;">İnceleme İşlemleri</div>')

                # Duration setting
                duration_choice = st.selectbox(
                    "Süre onayı",
                    options=[1, 2, 3, 4, 5, 6],
                    index=min(listing.duration_months, 6) - 1,
                    format_func=lambda x: f"{x} ay",
                    key=f"dur_{listing.listing_id}",
                )

                # Reviewer comment
                reviewer_comment = st.text_area(
                    "İnceleme Uzmanı Yorumu",
                    value=listing.reviewer_comment if listing.status == ListingStatus.REVISION_REQUESTED else "",
                    placeholder="Satıcı veya iç denetim kaydı için yorum ekleyin...",
                    height=90,
                    key=f"comment_{listing.listing_id}",
                )

                btn_cols = st.columns(3)
                with btn_cols[0]:
                    if st.button("✅ Onayla", key=f"approve_{listing.listing_id}", use_container_width=True, type="primary"):
                        comment = reviewer_comment or (
                            f"Kalite puanı: {machine.internal_quality_score} — {duration_choice} aylık ilan için onaylandı."
                        )
                        update_listing_status(
                            listing.listing_id,
                            ListingStatus.LIVE,
                            comment,
                            duration_choice,
                            reviewer_name,
                        )
                        st.success(f"✅ İlan onaylandı ve Yayına Alındı ({duration_choice} ay).")
                        st.rerun()
                with btn_cols[1]:
                    if st.button("🔄 Revizyon İste", key=f"revision_{listing.listing_id}", use_container_width=True):
                        if not reviewer_comment.strip():
                            st.error("Lütfen satıcı için bir revizyon yorumu girin.")
                        else:
                            update_listing_status(
                                listing.listing_id,
                                ListingStatus.REVISION_REQUESTED,
                                reviewer_comment,
                                reviewer_name=reviewer_name,
                            )
                            st.warning("🔄 Revizyon talep edildi. Satıcıya bilgi verildi.")
                            st.rerun()
                with btn_cols[2]:
                    if st.button("❌ Reddet", key=f"reject_{listing.listing_id}", use_container_width=True):
                        comment = reviewer_comment or "Reddedildi — platform kalite standartlarını karşılamıyor."
                        update_listing_status(
                            listing.listing_id,
                            ListingStatus.REJECTED,
                            comment,
                            reviewer_name=reviewer_name,
                        )
                        st.error("❌ İlan reddedildi.")
                        st.rerun()

            elif listing.status == ListingStatus.LIVE:
                approved_dur = listing.approved_duration_months or listing.duration_months
                st.html(f"""
<div class="alert-success">
  ✅ <strong>Onaylandı ve Yayında</strong><br>
  Süre: {approved_dur} ay<br>
  Bitiş: {listing.expires_at}
</div>
""")


# ── Pending tab ───────────────────────────────────────────────────────────────
with tab_pending:
    pending = get_listings(status=[ListingStatus.SUBMITTED])
    if not pending:
        st.html('<div style="color:#8896A8;padding:1rem 0;">İncelenecek ilan bulunmuyor. ✅</div>')
    else:
        st.html(f'<div style="font-size:0.875rem;color:#4A5568;margin-bottom:0.75rem;"><strong>{len(pending)}</strong> ilan inceleme bekliyor</div>')
        for l in sorted(pending, key=lambda x: x.submitted_at or x.created_at):
            render_review_card(l, show_actions=True)

# ── Revision tab ──────────────────────────────────────────────────────────────
with tab_revision:
    revision = get_listings(status=[ListingStatus.REVISION_REQUESTED])
    if not revision:
        st.html('<div style="color:#8896A8;padding:1rem 0;">Revizyon bekleyen ilan bulunmuyor.</div>')
    else:
        for l in revision:
            render_review_card(l, show_actions=True)

# ── Live tab ──────────────────────────────────────────────────────────────────
with tab_live:
    live = get_listings(status=[ListingStatus.LIVE])
    if not live:
        st.html('<div style="color:#8896A8;padding:1rem 0;">Yayında olan ilan bulunmuyor.</div>')
    else:
        for l in live:
            render_review_card(l, show_actions=False)

# ── All listings tab ──────────────────────────────────────────────────────────
with tab_history:
    all_listings = get_listings()
    st.dataframe(
        data={
            "İlan ID": [l.listing_id for l in all_listings],
            "Makine": [
                f"{get_machine(l.machine_id).brand} {get_machine(l.machine_id).model}"
                if get_machine(l.machine_id) else "?"
                for l in all_listings
            ],
            "Asking Price (₺)": [f"₺{l.asking_price:,.0f}" for l in all_listings],
            "Status": [l.status.value for l in all_listings],
            "Submitted": [l.submitted_at.strftime("%d %b %Y") if l.submitted_at else "—" for l in all_listings],
            "City": [l.location_city for l in all_listings],
            "Duration (mo)": [l.duration_months for l in all_listings],
        },
        use_container_width=True,
        hide_index=True,
    )

render_footer()
