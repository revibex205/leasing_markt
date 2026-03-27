"""
views/3_Lead_Form.py — Buyer "Please Call Me" Lead Form
Bank-style lead capture. No direct seller contact.
"""

import streamlit as st
import uuid
from datetime import datetime



from data.state import init_state, get_listing_by_id, get_machine, add_lead, next_lead_id
from data.models import Lead
from components.styles import inject_global_css
from components.ui import render_sidebar_nav, render_footer, trust_badge_html, page_title

init_state()
inject_global_css()

# ── Resolve pre-filled listing ────────────────────────────────────────────────
prefill_listing_id = st.session_state.get("lead_form_listing_id")
prefill_listing = get_listing_by_id(prefill_listing_id) if prefill_listing_id else None
prefill_machine = get_machine(prefill_listing.machine_id) if prefill_listing else None

# ── Confirmation mode ─────────────────────────────────────────────────────────
if st.session_state.get("lead_submitted"):
    submitted_lead = st.session_state.get("last_submitted_lead", {})
    st.html(f"""
<div class="lead-confirm-box">
  <div class="lc-icon">✅</div>
  <div class="lc-title">Talebiniz Alınmıştır</div>
  <div class="lc-sub">
    Teşekkürler, <strong>{submitted_lead.get("name", "")}</strong>.<br>
    Bir DemoBank leasing uzmanı sizinle 1 iş günü içinde
    <strong>{submitted_lead.get("phone", "")}</strong> numarası üzerinden iletişime geçecektir.<br><br>
    Referans Numarası: <strong>{submitted_lead.get("ref", "")}</strong>
  </div>
</div>
""")

    st.html("<br>")
    st.html("""
<div class="alert-info">
  🏦 <strong>Sırada ne var?</strong><br>
  Leasing ekibimiz talebinizi inceleyecek ve finansman seçeneklerini görüşmek üzere sizinle 
  iletişime geçecektir. Leasing onaylanırsa, makine satın alımını DemoBank üzerinden gerçekleştirerek 
  banka güvencesinde sorunsuz bir mülkiyet geçişi sağlayabilirsiniz.
</div>
""")

    st.html("<br>")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Pazaryerine Dön", use_container_width=True):
            st.session_state["lead_submitted"] = False
            st.session_state["lead_form_listing_id"] = None
            st.switch_page("views/1_Marketplace.py")
    with col2:
        if st.button("Başka Bir Makine İncele", use_container_width=True):
            st.session_state["lead_submitted"] = False
            st.switch_page("views/2_Machine_Detail.py")

    render_footer()
    st.stop()

# ── Form page ─────────────────────────────────────────────────────────────────
page_title(
    "📄 Finansal Başvuru Talebi",
    "Ön Leasing Sorgusu",
    "Bilgilerinizi güvenli bir şekilde iletin. Bir DemoBank Ticari Leasing Uzmanı finansman koşullarını görüşmek üzere 1 iş günü içinde sizinle iletişime geçecektir.",
)

form_col, info_col = st.columns([3, 2], gap="large")

with form_col:
    st.html("""
<div style="background:white;border:1px solid #D6DCE8;border-radius:16px;padding:1.75rem;margin-bottom:1rem;">
  <div style="font-size:0.85rem;font-weight:700;color:#0A1628;margin-bottom:1.25rem;padding-bottom:0.75rem;border-bottom:1px solid #EEF1F7;">
    İletişim Bilgileriniz
  </div>
""")

    with st.form("lead_form"):
        name_col, company_col = st.columns(2)
        with name_col:
            buyer_name = st.text_input("Ad Soyad *", placeholder="Adınız ve soyadınız")
        with company_col:
            buyer_company = st.text_input("Firma Adı", placeholder="Firmanız (varsa)")

        phone_col, email_col = st.columns(2)
        with phone_col:
            buyer_phone = st.text_input("Telefon Numarası *", placeholder="+90 5XX XXX XX XX")
        with email_col:
            buyer_email = st.text_input("E-posta Adresi", placeholder="ornek@email.com")

        # Machine of interest
        from data.state import get_public_listings
        live_listings = get_public_listings()
        machine_options = {}
        for l in live_listings:
            m = get_machine(l.machine_id)
            if m:
                label = f"{m.brand} {m.model} — ₺{l.asking_price:,.0f} ({l.location_city})"
                machine_options[label] = l.listing_id

        if prefill_machine and prefill_listing:
            prefill_label = f"{prefill_machine.brand} {prefill_machine.model} — ₺{prefill_listing.asking_price:,.0f} ({prefill_listing.location_city})"
            default_idx = list(machine_options.keys()).index(prefill_label) if prefill_label in machine_options else 0
        else:
            default_idx = 0

        selected_machine_label = st.selectbox(
            "İlgilenilen Makine *",
            options=list(machine_options.keys()),
            index=default_idx,
        )

        interest_notes = st.text_area(
            "Finansman İhtiyaçları ve Kullanım Amacı",
            placeholder="Lütfen ekipmanı nasıl kullanmayı planladığınızı ve tercih ettiğiniz leasing vadesini (örn. 36 ay, 48 ay) kısaca açıklayın...",
            height=100,
        )

        st.html("""
<div style="background:#F8F9FC;border:1px solid #D6DCE8;border-radius:8px;padding:1rem;margin-bottom:1rem;">
  <div style="font-size:0.75rem;font-weight:700;color:#0A1628;margin-bottom:0.4rem;">Ön Başvuru Koşulları</div>
  <div style="font-size:0.75rem;color:#4A5568;line-height:1.5;">
    Bu talep formunu göndererek DemoBank Ticari Leasing Bölümü'nden bir arama talep etmiş oluyorsunuz. 
    Bu işlem bağlayıcı bir kredi sözleşmesi değildir. DemoBank, sağlanan verileri sıkı bir şekilde KVKK uyumlu olarak, 
    yalnızca leasing uygunluğunu değerlendirmek amacıyla işleyecektir. Satıcı bilgileri kesinlikle gizli kalır.
  </div>
</div>
""")

        consent = st.checkbox("Bu makineyle ilgili olarak DemoBank'ın benimle iletişime geçmesine ve bilgilerimi ön kredi değerlendirmesi için saklamasına izin veriyorum. *")

        submitted = st.form_submit_button(
            "🏦 Finansman Talebini Gönder",
            use_container_width=True,
            type="primary",
        )

    st.html("</div>")

    if submitted:
        # Validation
        errors = []
        if not buyer_name.strip():
            errors.append("Ad Soyad bilgisi zorunludur.")
        if not buyer_phone.strip():
            errors.append("Telefon numarası zorunludur.")
        if not selected_machine_label:
            errors.append("Lütfen ilgilenilen bir makine seçin.")
        if not consent:
            errors.append("İşleme devam etmek için ön başvuru şartlarını kabul etmelisiniz.")

        if errors:
            for e in errors:
                st.html(f'<div class="alert-danger">⚠️ {e}</div>')
        else:
            # Save lead
            listing_id_selected = machine_options[selected_machine_label]
            new_lead_id = next_lead_id()
            new_lead = Lead(
                lead_id=new_lead_id,
                listing_id=listing_id_selected,
                machine_id=get_listing_by_id(listing_id_selected).machine_id,
                buyer_name=buyer_name.strip(),
                buyer_company=buyer_company.strip(),
                buyer_phone=buyer_phone.strip(),
                buyer_email=buyer_email.strip(),
                interest_notes=interest_notes.strip(),
                submitted_at=datetime.now(),
                status="Yeni",
            )
            add_lead(new_lead)

            st.session_state["lead_submitted"] = True
            st.session_state["last_submitted_lead"] = {
                "name": buyer_name.strip(),
                "phone": buyer_phone.strip(),
                "ref": f"LM-{new_lead_id}-{datetime.now().strftime('%y%m%d')}",
            }
            st.rerun()

with info_col:
    st.html("""
<div style="background:linear-gradient(135deg,#0A1628,#1A2E4A);border-radius:16px;padding:1.75rem;color:white;margin-bottom:1rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#F5B942;margin-bottom:0.75rem;">
    Süreç Nasıl İşler?
  </div>
  <div style="display:flex;flex-direction:column;gap:1rem;">
    <div style="display:flex;gap:0.75rem;align-items:flex-start;">
      <div style="font-size:1.2rem;">📞</div>
      <div>
        <div style="font-size:0.85rem;font-weight:700;margin-bottom:0.15rem;">Banka Sizi Arar</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.65);line-height:1.55;">
          Bir DemoBank leasing uzmanı 1 iş günü içerisinde sizi arayarak süreç hakkında bilgi verir.
        </div>
      </div>
    </div>
    <div style="display:flex;gap:0.75rem;align-items:flex-start;">
      <div style="font-size:1.2rem;">📄</div>
      <div>
        <div style="font-size:0.85rem;font-weight:700;margin-bottom:0.15rem;">Başvuru Değerlendirmesi</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.65);line-height:1.55;">
          Banka leasing uygunluğunuzu değerlendirir ve size kişiselleştirilmiş bir teklif sunar.
        </div>
      </div>
    </div>
    <div style="display:flex;gap:0.75rem;align-items:flex-start;">
      <div style="font-size:1.2rem;">🏛️</div>
      <div>
        <div style="font-size:0.85rem;font-weight:700;margin-bottom:0.15rem;">Finansman Düzenlenir</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.65);line-height:1.55;">
          Onaylandıktan sonra makineyi doğrudan DemoBank leasing üzerinden edinebilirsiniz — satıcıyla direkt iletişim kurmanıza gerek kalmaz.
        </div>
      </div>
    </div>
  </div>
</div>
""")

    if prefill_machine and prefill_listing:
        st.html(f"""
<div style="background:white;border:1px solid #D6DCE8;border-radius:14px;padding:1.2rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#8896A8;margin-bottom:0.5rem;">
    İlgilenilen Makine
  </div>
  <div style="font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.25rem;">
    {prefill_machine.brand} {prefill_machine.model}
  </div>
  <div style="font-size:0.85rem;color:#4A5568;margin-bottom:0.75rem;">
    {prefill_machine.production_year} · {prefill_listing.location_city}
  </div>
  <div style="font-size:1.3rem;font-weight:800;color:#0A1628;margin-bottom:0.75rem;">
    ₺{prefill_listing.asking_price:,.0f}
  </div>
  <div>{trust_badge_html("bank")}</div>
</div>
""")

    st.html("<br>")
    st.html("""
<div class="alert-info">
  🏦 <strong>Satıcıyla doğrudan etkileşim yok.</strong>
  DemoBank, her iki tarafın gizliliğini korumak amacıyla tüm başvuru süreçlerini üstlenir.
</div>
""")

render_footer()
