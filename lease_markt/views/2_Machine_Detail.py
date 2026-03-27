"""
views/2_Machine_Detail.py — Machine Detail View
Full specifications, masked seller, trust badge, leasing placeholder, CTA.
"""

import streamlit as st



from data.state import init_state, get_public_listings, get_machine, get_seller
from components.styles import inject_global_css
from components.ui import (
    trust_badge_html, render_footer, render_machine_card,
    format_price, days_remaining, CATEGORY_ICONS, page_title,
)

init_state()
inject_global_css()

# ── Resolve listing ───────────────────────────────────────────────────────────
all_live = get_public_listings()
listing_id = st.session_state.get("selected_listing_id")
selected_listing = None

if listing_id:
    for l in all_live:
        if l.listing_id == listing_id:
            selected_listing = l
            break

# If no listing selected yet, allow manual selection
if not selected_listing:
    st.html("""
<div class="section-eyebrow">Makine Detayı</div>
<div class="section-title">Bir İlan Seçin</div>
""")

    options = {
        f"{get_machine(l.machine_id).brand} {get_machine(l.machine_id).model} — ₺{l.asking_price:,.0f}": l
        for l in all_live
        if get_machine(l.machine_id)
    }
    chosen_label = st.selectbox("İncelemek için bir ilan seçin:", list(options.keys()))
    if chosen_label:
        selected_listing = options[chosen_label]
        st.session_state["selected_listing_id"] = selected_listing.listing_id

if not selected_listing:
    st.info("İlan seçilmedi. Lütfen önce pazaryerini inceleyin.")
    if st.button("← Pazaryerine Dön"):
        st.switch_page("views/1_Marketplace.py")
    st.stop()

machine = get_machine(selected_listing.machine_id)
seller = get_seller(selected_listing.seller_id)
if not machine or not seller:
    st.error("Makine verisi bulunamadı.")
    st.stop()

icon = CATEGORY_ICONS.get(machine.category, "🔧")

# ── Breadcrumb ───────────────────────────────────────────────────────────────
st.html(f"""
<div style="font-size:0.82rem;color:#8896A8;margin-bottom:1.25rem;">
  <a href="#" style="color:#1147CC;">Pazaryeri</a> › {machine.brand} {machine.model}
</div>
""")

# ── Main layout ───────────────────────────────────────────────────────────────
main_col, side_col = st.columns([3, 2], gap="large")

with main_col:
    # "Gallery" — icon placeholder
    st.html(f"""
<div style="background:linear-gradient(135deg,#EEF1F7,#D6DCE8);border-radius:16px;
     aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;
     font-size:7rem;margin-bottom:1rem;">
  {icon}
</div>
""")

    # Trust + Status strip
    st.html(f"""
<div style="display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;margin-bottom:1rem;">
  {trust_badge_html("bank")}
  {trust_badge_html("verified")}
  {trust_badge_html("gold")}
  <span style="font-size:0.78rem;color:#8896A8;margin-left:0.5rem;">
    ✅ Bu ilan yayınlanmadan önce DemoBank tarafından incelenip onaylanmıştır.
  </span>
</div>
""")

    # Title block
    st.html(f"""
<div style="margin-bottom:1.25rem;">
  <div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#1147CC;margin-bottom:4px;">
    {machine.category.value}
  </div>
  <div style="font-size:2rem;font-weight:800;color:#0A1628;line-height:1.15;margin-bottom:0.3rem;">
    {machine.brand} {machine.model}
  </div>
  <div style="font-size:0.9rem;color:#4A5568;">
    {machine.production_year} · {selected_listing.location_city}, {selected_listing.location_region}
  </div>
</div>
""")

    # Specifications Table
    st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.6rem;">Makine Özellikleri</div>')

    specs = [
        ("Marka", machine.brand),
        ("Model", machine.model),
        ("Kategori", machine.category.value),
        ("Üretim Yılı", str(machine.production_year)),
        ("Seri Numarası", machine.serial_number + " (gizlenmiş)"),
        ("Ağırlık", f"{machine.weight_kg:,} kg" if machine.weight_kg else "N/A"),
        ("Motor / Çalışma Saati", f"{machine.engine_hours:,} saat" if machine.engine_hours else "N/A"),
        ("İlan Konumu", f"{selected_listing.location_city}, {selected_listing.location_region}"),
        ("İlan Geçerlilik Tarihi", str(selected_listing.expires_at) if selected_listing.expires_at else "N/A"),
    ]

    spec_rows = "".join([
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in specs
    ])
    st.html(f'<table class="spec-table">{spec_rows}</table>')

    st.html("<br>")

    # Description
    st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;">Açıklama</div>')
    st.html(f'<div style="font-size:0.9rem;color:#4A5568;line-height:1.7;">{machine.description}</div>')

    if selected_listing.additional_notes:
        st.html("<br>")
        st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.3rem;">Ek Notlar</div>')
        st.html(f'<div style="font-size:0.875rem;color:#4A5568;">{selected_listing.additional_notes}</div>')

    st.html("<br>")

    # ── Leasing Module Placeholder ──
    st.html("""
<div style="background:linear-gradient(135deg,#F8F9FC,#E8EEF8);border:1px solid #D6DCE8;border-radius:14px;padding:1.5rem;position:relative;overflow:hidden;">
  <!-- "Coming Soon" Overlay -->
  <div style="position:absolute;top:0;left:0;right:0;bottom:0;background:rgba(255,255,255,0.85);z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;backdrop-filter:blur(2px);">
    <div style="background:var(--cobalt);color:white;padding:0.4rem 1.2rem;border-radius:999px;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;box-shadow:0 4px 12px rgba(17,71,204,0.3);">Yakında Eklenecek</div>
    <div style="font-size:1.1rem;font-weight:800;color:var(--navy);">İnteraktif Leasing Hesaplayıcı</div>
    <div style="font-size:0.85rem;color:var(--text-sec);max-width:300px;text-align:center;margin-top:0.4rem;">Gösterge niteliğindeki kampanya oranlarını ve ödeme planlarını doğrudan platform üzerinden hesaplayın.</div>
  </div>

  <!-- Mock Calculator UI (Behind overlay) -->
  <div style="opacity:0.4;pointer-events:none;">
    <div style="display:flex;align-items:center;gap:0.5rem;font-size:0.9rem;font-weight:700;color:var(--navy);margin-bottom:1rem;">
      <span>💳</span> Örnek Finansman Seçenekleri
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div>
        <div style="font-size:0.75rem;color:var(--text-sec);margin-bottom:0.3rem;">Peşinat %</div>
        <div style="background:white;border:1px solid var(--border);border-radius:8px;padding:0.6rem;font-size:0.85rem;color:var(--navy);font-weight:600;">20% (₺0.00)</div>
      </div>
      <div>
        <div style="font-size:0.75rem;color:var(--text-sec);margin-bottom:0.3rem;">Vade (Ay)</div>
        <div style="background:white;border:1px solid var(--border);border-radius:8px;padding:0.6rem;font-size:0.85rem;color:var(--navy);font-weight:600;">36 Ay ▼</div>
      </div>
    </div>
    <div style="background:white;border:1px solid var(--border);border-radius:8px;padding:1rem;display:flex;justify-content:space-between;align-items:center;">
      <div>
        <div style="font-size:0.75rem;color:var(--text-sec);">Tahmini Aylık Taksit</div>
        <div style="font-size:1.4rem;font-weight:800;color:var(--navy);">₺ --,---</div>
      </div>
      <div style="background:var(--cobalt-dim);color:var(--cobalt);padding:0.4rem 0.8rem;border-radius:6px;font-size:0.75rem;font-weight:700;">Hesaplamayı Güncelle</div>
    </div>
  </div>
</div>
""")

    st.html("<br>")

    # Bank reviewed notice
    st.html("""
<div class="alert-info">
  🏦 <strong>Banka Onaylı İlan:</strong> Bu ilan yayınlanmadan önce DemoBank inceleme ekibi
  tarafından değerlendirilmiştir. Talep edilen fiyat, durum ve dokümantasyon
  bankanın iç kalite standartlarına göre incelenmiştir.
</div>
""")

    st.html("<br>")

    # Similar listings
    similar = [
        l for l in get_public_listings()
        if get_machine(l.machine_id) and get_machine(l.machine_id).category == machine.category
        and l.listing_id != selected_listing.listing_id
    ][:3]

    if similar:
        st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">Benzer Makineler</div>')
        sim_cols = st.columns(3)
        for i, sim_listing in enumerate(similar):
            sim_machine = get_machine(sim_listing.machine_id)
            with sim_cols[i]:
                render_machine_card(sim_listing, show_select_btn=True, rerun_on_click=True)

with side_col:
    # ── Price + Action card ──
    days_left = days_remaining(selected_listing.expires_at)

    st.html(f"""
<div style="background:white;border:1px solid #D6DCE8;border-radius:16px;padding:1.5rem;position:sticky;top:80px;margin-bottom:1rem;">
  <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.25rem;">
    Talep Edilen Fiyat
  </div>
  <div style="font-size:2.2rem;font-weight:800;color:#0A1628;margin-bottom:0.5rem;">
    {format_price(selected_listing.asking_price, selected_listing.currency)}
  </div>
  <div style="font-size:0.78rem;color:#8896A8;margin-bottom:1.25rem;">
    KDV ve diğer masraflar uygulanabilir. Fiyat çevrimiçi olarak bağlayıcı değildir.
  </div>
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.25rem;">
    {trust_badge_html("bank")}
    {trust_badge_html("verified")}
  </div>
  <div style="font-size:0.85rem;color:#B45309;background:#FFFBEB;padding:0.6rem;border-radius:8px;border:1px solid #FDE68A;margin-bottom:1rem;display:flex;align-items:center;gap:0.5rem;font-weight:600;">
    ⏳ İlan Geçerliliği: {days_left} (Maks. 6 Ay)
  </div>
</div>
""")

    if st.button(
        "📞 Başvuru İçin Beni Arayın",
        use_container_width=True,
        type="primary",
        key="lead_cta_main",
    ):
        st.session_state["lead_form_listing_id"] = selected_listing.listing_id
        st.switch_page("views/3_Lead_Form.py")

    if st.button("🏦 Şube ile İletişime Geç", use_container_width=True, key="branch_cta"):
        st.info("Bir leasing uzmanıyla görüşmek için lütfen en yakın DemoBank şubesini ziyaret edin veya 444 0 BANK'ı arayın.")

    st.html("<br>")

    # ── Masked Seller Info ──
    st.html(f"""
<div style="background:#F8F9FC;border:1px solid #D6DCE8;border-radius:14px;padding:1.25rem;">
  <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;">
    <div style="font-size:1.2rem;">🔒</div>
    <div style="font-size:0.9rem;font-weight:700;color:#0A1628;">Banka Aracılıklı Satıcı</div>
  </div>
  
  <div style="display:grid;gap:0.85rem;">
    <div>
      <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.15rem;">Satıcı Kimliği</div>
      <div style="font-size:0.9rem;font-weight:600;color:#0A1628;">{seller.masked_name}</div>
    </div>
    <div>
      <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.15rem;">Kayıtlı Merkez Konumu</div>
      <div style="font-size:0.9rem;font-weight:600;color:#0A1628;">📍 {seller.city}</div>
    </div>
    <div>
      <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.15rem;">Banka Doğrulaması</div>
      <div style="font-size:0.9rem;font-weight:600;color:#16A34A;display:flex;align-items:center;gap:0.3rem;">
        ✅ Doğrulanmış Leasing Müşterisi
      </div>
    </div>
  </div>
</div>
""")

    st.html("""
<div class="disclaimer" style="margin-top:0.75rem;">
  🔒 Satıcı iletişim bilgileri herkese açık olarak paylaşılmaz.
  Tüm alıcı talepleri, her iki tarafı da korumak amacıyla DemoBank üzerinden işleme alınır.
</div>
""")

    st.html("<br>")

    # Financing disclaimer
    st.html("""
<div class="alert-info">
  ℹ️ <strong>Finansman:</strong> Gösterilen veya görüşülen leasing koşulları, faiz oranları ve kampanya detayları 
  yalnızca gösterge niteliğindedir. Nihai onay ve şartlar DemoBank'ın kredi değerlendirmesine ve yürürlükteki mevzuatlara tabidir.
</div>
""")

render_footer()
