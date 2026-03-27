"""
views/5_Create_Listing.py — Seller Listing Creation Wizard
5-step flow: select machine → enter details → set price → set duration → review & submit.
"""

import streamlit as st
from datetime import datetime



from data.state import init_state, get_listings, add_listing, update_listing_fields, next_listing_id, get_listing_by_id
from data.models import Listing, ListingStatus
from data.seed_data import MACHINE_MAP
from components.styles import inject_global_css
from components.ui import render_sidebar_nav, require_role, render_footer, page_title, CATEGORY_ICONS

init_state()
inject_global_css()

if not require_role("seller", "Yeni İlan Oluştur — Satıcı Portalı"):
    render_footer()
    st.stop()

seller_id = st.session_state.get("current_seller_id", "S001")
edit_listing_id = st.session_state.get("edit_listing_id")

# Ensure create_listing_data exists
if "create_listing_data" not in st.session_state:
    st.session_state["create_listing_data"] = {}

# If editing existing listing, pre-populate
if edit_listing_id and not st.session_state["create_listing_data"]:
    existing = get_listing_by_id(edit_listing_id)
    if existing:
        st.session_state["create_listing_data"] = {
            "machine_id": existing.machine_id,
            "asking_price": existing.asking_price,
            "location_city": existing.location_city,
            "location_region": existing.location_region,
            "condition_notes": existing.condition_notes,
            "additional_notes": existing.additional_notes,
            "duration_months": existing.duration_months,
        }
        st.session_state["create_listing_step"] = 2

step = st.session_state.get("create_listing_step", 1)
data = st.session_state.get("create_listing_data", {})

# ── Wizard step indicator ─────────────────────────────────────────────────────

page_title("Satıcı Portalı", "Makinenizi Satışa Çıkarın", "Adım adım ilan oluşturma rehberi. Tüm ilanlar yayınlanmadan önce DemoBank incelemesinden geçer.")

STEPS = ["Makine Seçimi", "Makine Detayları", "Fiyat ve Konum", "Süre ve İnceleme", "Gönderildi"]

st.html('<div class="wizard-steps">')
for i, step_label in enumerate(STEPS, 1):
    css_class = "active" if i == step else ("done" if i < step else "")
    check = "✓" if i < step else str(i)
    st.html(f"""
<div class="wizard-step {css_class}">
  <div class="wizard-step-dot">{check}</div>
  <div>{step_label}</div>
</div>
""")
st.html("</div>")

st.html('<hr style="border:none;border-top:1px solid #EEF1F7;margin:0 0 1.5rem;">')

# ────────────────────────────────────────────────────────────────────────────
# STEP 1 — Select Eligible Machine
# ────────────────────────────────────────────────────────────────────────────

if step == 1:
    st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:1rem;">Leasing Geçmişinizden Bir Makine Seçin</div>')

    eligible = [m for m in MACHINE_MAP.values() if m.seller_id == seller_id]
    already_listed = {l.machine_id for l in get_listings(seller_id=seller_id)}

    if not eligible:
        st.html('<div class="alert-warning">Leasing geçmişinizde uygun makine bulunamadı. Lütfen destek için DemoBank ile iletişime geçin.</div>')
    else:
        for machine in eligible:
            is_listed = machine.machine_id in already_listed
            icon = CATEGORY_ICONS.get(machine.category, "🔧")
            col_info, col_action = st.columns([5, 1])
            with col_info:
                st.html(f"""
<div style="background:white;border:1px solid #D6DCE8;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:0.5rem;
     {'opacity:0.5;' if is_listed else ''}">
  <div style="display:flex;align-items:center;gap:0.75rem;">
    <div style="font-size:2rem;">{icon}</div>
    <div>
      <div style="font-size:0.95rem;font-weight:700;color:#0A1628;">{machine.brand} {machine.model}</div>
      <div style="font-size:0.78rem;color:#8896A8;">
        {machine.category.value} · {machine.production_year}
        · Sözleşme bitiş: {machine.leasing_contract_end_date.strftime("%b %Y")}
      </div>
      {"<div style='font-size:0.75rem;color:#16A34A;font-weight:600;margin-top:3px;'>✅ Zaten platformda listelenmiş</div>" if is_listed else ""}
    </div>
  </div>
</div>
""")
            with col_action:
                preselected = st.session_state.get("create_listing_machine_id") == machine.machine_id
                key = f"select_machine_{machine.machine_id}"
                if not is_listed:
                    if st.button("Seç →", key=key, use_container_width=True, type="primary" if preselected else "secondary"):
                        data["machine_id"] = machine.machine_id
                        st.session_state["create_listing_data"] = data
                        st.session_state["create_listing_step"] = 2
                        st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# STEP 2 — Machine Details (condition notes, description override)
# ────────────────────────────────────────────────────────────────────────────

elif step == 2:
    machine = MACHINE_MAP.get(data.get("machine_id"))
    if not machine:
        st.error("Makine seçilmedi. Lütfen 1. Adıma dönün.")
        if st.button("← 1. Adıma Dön"):
            st.session_state["create_listing_step"] = 1
            st.rerun()
    else:
        icon = CATEGORY_ICONS.get(machine.category, "🔧")
        st.html(f"""
<div style="background:white;border:1px solid #D6DCE8;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:1.25rem;display:flex;gap:1rem;align-items:center;">
  <div style="font-size:2.5rem;">{icon}</div>
  <div>
    <div style="font-size:1rem;font-weight:700;color:#0A1628;">{machine.brand} {machine.model}</div>
    <div style="font-size:0.82rem;color:#8896A8;">{machine.category.value} · {machine.production_year}</div>
  </div>
</div>
""")

        with st.form("step2_form"):
            st.html('<div style="font-size:0.85rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">Durum Notları</div>')
            condition_notes = st.text_area(
                "Makinenin mevcut durumunu açıklayın",
                value=data.get("condition_notes", ""),
                height=100,
                placeholder="Örn. Mükemmel çalışır durumda. Tam servis geçmişi mevcut. Lastikler 2024'te değiştirildi.",
            )
            additional_notes = st.text_area(
                "Alıcılar İçin Ek Notlar",
                value=data.get("additional_notes", ""),
                height=80,
                placeholder="Örn. KDV hariç. Makine depomuzda incelenebilir.",
            )

            subcols = st.columns(2)
            with subcols[0]:
                back = st.form_submit_button("← Geri")
            with subcols[1]:
                nxt = st.form_submit_button("İleri: Fiyat ve Konum →", type="primary", use_container_width=True)

        if nxt:
            data.update({"condition_notes": condition_notes, "additional_notes": additional_notes})
            st.session_state["create_listing_data"] = data
            st.session_state["create_listing_step"] = 3
            st.rerun()
        if back:
            st.session_state["create_listing_step"] = 1
            st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# STEP 3 — Pricing & Location
# ────────────────────────────────────────────────────────────────────────────

elif step == 3:
    machine = MACHINE_MAP.get(data.get("machine_id"))
    st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">Fiyat ve Konum</div>')

    with st.form("step3_form"):
        price_col, _ = st.columns([2, 1])
        with price_col:
            asking_price = st.number_input(
                "Talep Edilen Fiyat (₺) *",
                min_value=10_000,
                max_value=50_000_000,
                value=int(data.get("asking_price", machine.market_reference_price if machine else 1_000_000)),
                step=10_000,
                format="%d",
            )

        if machine:
            diff = ((asking_price - machine.market_reference_price) / machine.market_reference_price) * 100
            if abs(diff) > 15:
                direction = "üzerinde" if diff > 0 else "altında"
                st.html(f'<div class="alert-warning">⚠️ Talep ettiğiniz fiyat, piyasa referansımızın %{abs(diff):.0f} {direction}. Banka inceleme uzmanı revizyon talep edebilir.</div>')
            else:
                st.html(f'<div class="alert-success">✅ Talep ettiğiniz fiyat makul piyasa aralığındadır (referans: ₺{machine.market_reference_price:,.0f}).</div>')

        city_col, region_col = st.columns(2)
        with city_col:
            location_city = st.text_input("Şehir *", value=data.get("location_city", ""), placeholder="Örn: İstanbul")
        with region_col:
            location_region = st.selectbox(
                "Bölge *",
                ["Marmara", "İç Anadolu", "Ege", "Akdeniz", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"],
                index=["Marmara", "İç Anadolu", "Ege", "Akdeniz", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"].index(data.get("location_region", "Marmara")),
            )

        subcols = st.columns(2)
        with subcols[0]:
            back = st.form_submit_button("← Geri")
        with subcols[1]:
            nxt = st.form_submit_button("İleri: Süre ve İnceleme →", type="primary", use_container_width=True)

    if nxt:
        if not location_city.strip():
            st.error("Şehir bilgisi zorunludur.")
        else:
            data.update({"asking_price": asking_price, "location_city": location_city, "location_region": location_region})
            st.session_state["create_listing_data"] = data
            st.session_state["create_listing_step"] = 4
            st.rerun()
    if back:
        st.session_state["create_listing_step"] = 2
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# STEP 4 — Duration + Final Review + Submit
# ────────────────────────────────────────────────────────────────────────────

elif step == 4:
    machine = MACHINE_MAP.get(data.get("machine_id"))
    st.html('<div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">İlan Süresi ve Son İnceleme</div>')

    with st.form("step4_form"):
        duration = st.selectbox(
            "İstenen İlan Süresi (1-6 ay, banka onayına tabidir)",
            options=[1, 2, 3, 4, 5, 6],
            index=data.get("duration_months", 3) - 1,
            format_func=lambda x: f"{x} ay (maks 6 ay)",
        )

        st.html('<hr style="border:none;border-top:1px solid #EEF1F7;margin:1rem 0;">')
        st.html('<div style="font-size:0.85rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">İlanınızı Gözden Geçirin</div>')

        if machine:
            summary_rows = [
                ("Makine", f"{machine.brand} {machine.model}"),
                ("Kategori", machine.category.value),
                ("Yıl", str(machine.production_year)),
                ("Talep Edilen Fiyat", f"₺{data.get('asking_price', 0):,.0f}"),
                ("Konum", f"{data.get('location_city', '—')}, {data.get('location_region', '—')}"),
                ("İstenen Süre", f"{duration} ay"),
                ("Durum Notları", data.get("condition_notes", "—") or "—"),
            ]
            rows_html = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in summary_rows)
            st.html(f'<table class="spec-table">{rows_html}</table>')

        st.html("""
<div class="alert-info" style="margin-top:0.75rem;">
  ℹ️ İlanınız gönderildikten sonra <strong>DemoBank İnceleme Sırasına</strong> girecektir.
  Bir uzman, ilanı herkese açık hale getirmeden önce kaliteyi ve fiyatlandırmayı değerlendirecektir.
  Tipik inceleme süresi 1-3 iş günüdür.
</div>
""")

        st.html("""
<div class="disclaimer" style="margin-top:0.75rem;">
  Göndererek, bilgilerin doğru olduğunu ve bu makinenin gerçekten satılık olduğunu onaylarsınız. 
  DemoBank inceleme sırasında ek bilgi için sizinle iletişime geçebilir.
</div>
""")

        subcols = st.columns(2)
        with subcols[0]:
            back = st.form_submit_button("← Geri")
        with subcols[1]:
            submit = st.form_submit_button("🚀 Banka İncelemesi İçin Gönder", type="primary", use_container_width=True)

    if submit:
        data["duration_months"] = duration
        st.session_state["create_listing_data"] = data

        # Create or update listing
        if edit_listing_id:
            update_listing_fields(
                edit_listing_id,
                asking_price=data["asking_price"],
                location_city=data["location_city"],
                location_region=data["location_region"],
                condition_notes=data["condition_notes"],
                additional_notes=data["additional_notes"],
                duration_months=duration,
                status=ListingStatus.SUBMITTED,
                submitted_at=datetime.now(),
            )
        else:
            new_listing = Listing(
                listing_id=next_listing_id(),
                machine_id=data["machine_id"],
                seller_id=seller_id,
                asking_price=data["asking_price"],
                currency="TRY",
                location_city=data.get("location_city", ""),
                location_region=data.get("location_region", ""),
                condition_notes=data.get("condition_notes", ""),
                additional_notes=data.get("additional_notes", ""),
                status=ListingStatus.SUBMITTED,
                duration_months=duration,
                created_at=datetime.now(),
                submitted_at=datetime.now(),
            )
            add_listing(new_listing)

        # Clear wizard state
        st.session_state["create_listing_data"] = {}
        st.session_state["edit_listing_id"] = None
        st.session_state["create_listing_machine_id"] = None
        st.session_state["create_listing_step"] = 5
        st.rerun()

    if back:
        st.session_state["create_listing_step"] = 3
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# STEP 5 — Success / Submitted
# ────────────────────────────────────────────────────────────────────────────

elif step == 5:
    st.html("""
<div class="lead-confirm-box">
  <div class="lc-icon">📤</div>
  <div class="lc-title">İlan Banka İncelemesine Gönderildi</div>
  <div class="lc-sub">
    İlanınız DemoBank inceleme ekibine iletilmiştir.<br>
    Alanında uzman ekibimiz, ilanınızı yayına almadan önce detaylı bir şekilde değerlendirecektir.<br>
    İnceleme kararı 1-3 iş günü içinde tarafınıza bildirilecektir.<br><br>
    <strong>İlanınızın durumunu Satıcı Paneli üzerinden takip edebilirsiniz.</strong>
  </div>
</div>
""")

    st.html("<br>")
    col1, col2, _ = st.columns(3)
    with col1:
        if st.button("📋 Satıcı Paneline Git", type="primary", use_container_width=True):
            st.session_state["create_listing_step"] = 1
            st.switch_page("views/4_Seller_Dashboard.py")
    with col2:
        if st.button("➕ Başka Bir Makine Listele", use_container_width=True):
            st.session_state["create_listing_step"] = 1
            st.session_state["create_listing_data"] = {}
            st.rerun()

render_footer()
