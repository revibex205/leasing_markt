"""
app.py — LeaseMarkt Landing Page
Public-facing hero, featured listings, how-it-works, trust section.
Entry point for the Streamlit multi-page app.
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ──────────────────────────────


# ── Shared modules ───────────────────────────────────────────────────────────
from data.state import init_state, get_public_listings, get_machine, get_seller
from components.styles import inject_global_css
from components.ui import (
    render_sidebar_nav, render_machine_card, trust_badge_html,
    render_footer, format_price, CATEGORY_ICONS,
)

init_state()
inject_global_css()

# ────────────────────────────────────────────────────────────────────────────
# HERO SECTION
# ────────────────────────────────────────────────────────────────────────────

st.html("""
<div class="hero-section">
  <div class="hero-eyebrow">
    🏦 DemoBank A.Ş. · Güvenilir Makine Pazaryeri
  </div>
  <div class="hero-title">
    Banka Onaylı İkinci El<br>Makine Keşif Platformu
  </div>
  <div class="hero-sub">
    Listelenen her makine, yayınlanmadan önce banka tarafından incelenir ve onaylanır.
    Güvenle inceleyin — tüm satıcılar doğrulanmış leasing müşterileridir
    ve tüm ilanlar kalite ve fiyat standartlarımızı karşılar.
  </div>
  <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
    <span style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.25);border-radius:999px;padding:5px 14px;font-size:0.78rem;color:rgba(255,255,255,0.85);font-weight:600;">
      🛡️ Banka Kalite İncelemesi
    </span>
    <span style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.25);border-radius:999px;padding:5px 14px;font-size:0.78rem;color:rgba(255,255,255,0.85);font-weight:600;">
      🔒 Yalnızca Doğrulanmış Satıcılar
    </span>
    <span style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.25);border-radius:999px;padding:5px 14px;font-size:0.78rem;color:rgba(255,255,255,0.85);font-weight:600;">
      📋 Leasing Finansmanı Mevcut
    </span>
  </div>
</div>
""")

# ── Search bar ───────────────────────────────────────────────────────────────
col_search, col_btn = st.columns([5, 1])
with col_search:
    search_query = st.text_input(
        "Makinelerde ara",
        placeholder="örn. Caterpillar ekskavatör, John Deere traktör, CNC işlem merkezi...",
        label_visibility="collapsed",
    )
with col_btn:
    if st.button("🔍 Ara", use_container_width=True, type="primary"):
        st.session_state["marketplace_search"] = search_query
        st.switch_page("views/1_Marketplace.py")

st.html('<div style="height: var(--space-8);"></div>')

# ── Quick category shortcuts ─────────────────────────────────────────────────
st.html("""
<div class="section-eyebrow">Kategoriye Göre İncele</div>
""")

cat_cols = st.columns(4)
quick_cats = [
    ("🏗️", "İş Makinesi"), ("🌾", "Tarım Makinesi"), ("⚙️", "İmalat & CNC"),
    ("🏭", "İstif & Depolama"), ("🖨️", "Matbaa & Ambalaj"), ("⚡", "Enerji Sistemleri"),
    ("🚛", "Ticari Araçlar"), ("🔍", "Tüm İlanlar"),
]
for i, (icon, label) in enumerate(quick_cats):
    with cat_cols[i % 4]:
        if st.button(f"{icon}  {label}", key=f"cat_{i}", use_container_width=True):
            if label == "Tüm İlanlar":
                st.switch_page("views/1_Marketplace.py")
            else:
                st.session_state["marketplace_category"] = label
                st.switch_page("views/1_Marketplace.py")

st.html('<div style="height: var(--space-8);"></div>')

# ────────────────────────────────────────────────────────────────────────────
# FEATURED LISTINGS
# ────────────────────────────────────────────────────────────────────────────

st.html("""
<div style="margin-bottom:1rem;">
  <div class="section-eyebrow">Öne Çıkan İlanlar</div>
  <div class="section-title">Şu Anda Mevcut Makineler</div>
  <div class="section-sub">Tüm ilanlar yayınlanmadan önce DemoBank tarafından incelenip onaylanmıştır.</div>
</div>
""")

live_listings = get_public_listings()
featured = live_listings[:4]  # Show top 4 on landing

if featured:
    cols = st.columns(4)
    for i, listing in enumerate(featured):
        with cols[i]:
            render_machine_card(listing, show_select_btn=True)
else:
    st.info("Şu anda mevcut ilan yok. Lütfen daha sonra tekrar kontrol edin.")

col_browse, col_spacer = st.columns([1, 3])
with col_browse:
    if st.button("Tüm İlanları Gör →", use_container_width=True, type="primary"):
        st.switch_page("views/1_Marketplace.py")

st.html('<div style="height: var(--space-12);"></div>')

# ────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS
# ────────────────────────────────────────────────────────────────────────────

st.html("""
<div style="background:#F8F9FC;border-radius:18px;padding:2.5rem 2rem;margin-bottom:2rem;">
  <div class="section-eyebrow" style="text-align:center;">Platform Süreci</div>
  <div class="section-title" style="text-align:center;">Sistem Nasıl Çalışır?</div>
  <div class="section-sub" style="text-align:center;max-width:560px;margin:0 auto 2rem;">
    Üç farklı rol, tek bir güvenilir iş akışı — bankanın inceleme ve onay avantajıyla.
  </div>
""")

step_cols = st.columns(5)
steps = [
    ("🏦", "1", "Satıcı Makinesini Listeler",
     "Mevcut bir banka leasing müşterisi, leasing geçmişinden uygun bir makine seçer ve ilan oluşturur."),
    ("➡️", "", "", ""),
    ("⚖️", "2", "Banka İncelemesi ve Onayı",
     "Banka, ilan kalitesini, durumu ve fiyatı inceler. Yalnızca onaylanan ilanlar yayınlanır."),
    ("➡️", "", "", ""),
    ("📞", "3", "Alıcı Aranma Talebi İletir",
     "İlgilenen alıcılar arama talebi bırakır. Banka kendileriyle leasing seçeneklerini görüşmek üzere iletişime geçer."),
]

for i, (icon, num, title, desc) in enumerate(steps):
    with step_cols[i]:
        if not num:
            st.html(
                '<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:2rem;font-size:1.5rem;color:#D6DCE8;">→</div>'
            )
        else:
            st.html(f"""
<div class="step-card">
  <div class="step-number">{num}</div>
  <div class="step-icon">{icon}</div>
  <div class="step-title">{title}</div>
  <div class="step-desc">{desc}</div>
</div>
""")

st.html("</div>")

# ────────────────────────────────────────────────────────────────────────────
# TRUST SECTION
# ────────────────────────────────────────────────────────────────────────────

trust_col, cta_col = st.columns([3, 2], gap="large")

with trust_col:
    st.html("""
<div style="margin-bottom:1.5rem;">
  <div class="section-eyebrow">Neden LeaseMarkt?</div>
  <div class="section-title">Bankanın Güvence Avantajı</div>
</div>
""")

    trust_points = [
        ("🛡️", "Her İlan Banka Onaylıdır",
         "Ekibimiz, herhangi bir ilan yayına girmeden önce durum, fiyat ve dokümantasyon değerlendirmesi yapar. Kendi kendine yayınlanan ilan yoktur."),
        ("🔒", "Yalnızca Doğrulanmış Satıcılar",
         "Sadece mevcut banka leasing müşterileri makine listeleyebilir. Kimlik ve leasing geçmişi önceden doğrulanmıştır."),
        ("📊", "Uygun Fiyat Kontrolü",
         "Talep edilen fiyatları piyasa değerleriyle karşılaştırıyoruz. Aşırı fiyatlı ilanlar revizyon için geri gönderilir."),
        ("🤝", "Korunan Alıcı Deneyimi",
         "Alıcılar satıcı iletişim bilgilerini asla görmez. Tüm sorgular banka üzerinden geçer — tüm tarafları korur."),
        ("🏛️", "Finansman Sürekliliği",
         "İlgilenen alıcılar aynı banka üzerinden leasing başvurusunda bulunabilir, böylece sorunsuz bir mülkiyet geçişi sağlanır."),
    ]
    for icon, title, desc in trust_points:
        st.html(f"""
<div style="display:flex;gap:0.75rem;align-items:flex-start;padding:0.75rem 0;border-bottom:1px solid #EEF1F7;">
  <div style="font-size:1.3rem;margin-top:0.1rem;">{icon}</div>
  <div>
    <div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.15rem;">{title}</div>
    <div style="font-size:0.82rem;color:#4A5568;line-height:1.55;">{desc}</div>
  </div>
</div>
""")

with cta_col:
    # Seller CTA
    st.html("""
<div style="background:linear-gradient(135deg,#0A1628,#1A2E4A);border-radius:18px;padding:2rem;color:white;margin-bottom:1rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#F5B942;margin-bottom:0.6rem;">
    Leasing Müşterileri İçin
  </div>
  <div style="font-size:1.3rem;font-weight:800;margin-bottom:0.5rem;line-height:1.25;">
    Makinenizi Listelemeye Hazır Mısınız?
  </div>
  <div style="font-size:0.85rem;color:rgba(255,255,255,0.7);line-height:1.6;margin-bottom:1.25rem;">
    Eğer bir DemoBank leasing müşterisiyseniz, kira süresi dolan makinelerinizi 
    pazaryerimizde listeleyebilirsiniz. Doğrulanmış alıcılara ulaşın ve varlıklarınızı yeni fırsatlara dönüştürün.
  </div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.5);">
    Başlamak için sol menüden <strong style="color:#F5B942;">Satıcı Görünümüne</strong> geçin →
  </div>
</div>
""")

    # Platform stats
    kpi_data = [
        ("📋", f"{len(live_listings)}", "Aktif İlan"),
        ("🏦", "100%", "Banka Onaylı"),
        ("⏱️", "≤ 6 AY", "Maks İlan Süresi"),
        ("📞", "Gizli", "Alıcı Satıcı İletişimi"),
    ]
    k_cols = st.columns(2)
    for i, (icon, val, label) in enumerate(kpi_data):
        with k_cols[i % 2]:
            st.html(f"""
<div class="kpi-card" style="margin-bottom:0.75rem;">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-value" style="font-size:1.5rem;">{val}</div>
  <div class="kpi-sub">{label}</div>
</div>
""")

st.html('<div style="height: var(--space-8);"></div>')

# ────────────────────────────────────────────────────────────────────────────
# DISCLAIMER + FOOTER
# ────────────────────────────────────────────────────────────────────────────

st.html("""
<div class="disclaimer">
  ⚠️ <strong>Önemli Bilgi:</strong> Bu platform doğrudan satın alma, ödeme veya bağlayıcı finansal taahhütler sunmaz.
  Tüm ilanlar yalnızca keşif ve ön talep oluşturma amaçlıdır. Finansman uygunluğu, leasing oranları ve kampanya detayları 
  gösterge niteliğindedir ve DemoBank'ın kredi değerlendirme ve onay sürecine tabidir.
  Satıcı detayları veri gizliliği politikamız uyarınca gizlenmektedir.
</div>
""")

render_footer()
