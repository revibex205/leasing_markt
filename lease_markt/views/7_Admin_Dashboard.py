"""
views/7_Admin_Dashboard.py — Admin Analytics & Business Monitoring
Role-gated: bank admin only. KPI cards + Plotly charts + lead table.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta



from data.state import init_state, get_kpi_summary, get_listings, get_leads, get_machine
from data.models import ListingStatus
from components.styles import inject_global_css
from components.ui import render_sidebar_nav, require_role, render_footer, status_chip_html, page_title

init_state()
inject_global_css()

if not require_role("bank", "Admin Analitik Paneli"):
    render_footer()
    st.stop()

page_title(
    "📊 İş Takibi",
    "Platform Analitiği",
    "LeaseMarkt platform aktivitesi ve müşteri talebi performansının gerçek zamanlı özeti.",
)

kpi = get_kpi_summary()
all_listings = get_listings()
all_leads = get_leads()

# ────────────────────────────────────────────────────────────────────────────
# KPI CARDS ROW 1
# ────────────────────────────────────────────────────────────────────────────

kpi_row1 = st.columns(4)

kpi_configs_r1 = [
    ("📋", "Toplam İlan", kpi["total_listings"], "Tüm zamanlar", "blue"),
    ("✅", "Yayındaki İlanlar", kpi["live"], "Pazaryerinde aktif", "green"),
    ("⏳", "İnceleme Bekliyor", kpi["pending_review"], "Banka değerlendirmesi bekliyor", "amber"),
    ("🔄", "Revizyon İstenen", kpi["revision_requested"], "Satıcı işlemi gerekiyor", "amber"),
]

for i, (icon, label, value, sub, color) in enumerate(kpi_configs_r1):
    with kpi_row1[i]:
        bg = {"blue": "#EEF6FF", "green": "#F0FDF4", "amber": "#FFFBEB", "red": "#FEF2F2"}.get(color, "#F8F9FC")
        st.html(f"""
<div class="kpi-card">
  <div class="kpi-icon" style="background:{bg};width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;">{icon}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-sub">{sub}</div>
</div>
""")

st.html("<br>")

kpi_row2 = st.columns(4)
kpi_configs_r2 = [
    ("📞", "Toplam Talep", kpi["total_leads"], "Alınan arama talepleri", "blue"),
    ("🆕", "Yeni Talepler", kpi["new_leads"], "Banka iletişimi bekliyor", "amber"),
    ("🤝", "İletişime Geçildi", kpi["contacted_leads"], "Banka görüşme halinde", "green"),
    ("🎯", "Dönüştü", kpi["converted_leads"], "Leasing başvurusuna ilerledi", "green"),
]

for i, (icon, label, value, sub, color) in enumerate(kpi_configs_r2):
    with kpi_row2[i]:
        bg = {"blue": "#EEF6FF", "green": "#F0FDF4", "amber": "#FFFBEB"}.get(color, "#F8F9FC")
        st.html(f"""
<div class="kpi-card">
  <div class="kpi-icon" style="background:{bg};width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;">{icon}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-sub">{sub}</div>
</div>
""")

# ── Lead conversion highlight ────────────────────────────────────────────────
if kpi["total_leads"] > 0:
    conv_rate = kpi["converted_leads"] / kpi["total_leads"] * 100
    st.html(f"""
<div style="background:linear-gradient(135deg,#0A1628,#1A2E4A);border-radius:8px;padding:0.75rem 1rem;margin:0.5rem 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;border-left:4px solid #F5B942;">
  <div style="color:white;display:flex;align-items:center;gap:1rem;">
    <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#F5B942;">Talep Dönüşüm Oranı<br><span style="font-size:1.8rem;font-weight:800;color:white;line-height:1;">{conv_rate:.0f}%</span></div>
    <div style="font-size:0.75rem;color:rgba(255,255,255,0.7);max-width:200px;">Resmi leasing başvurusuna dönüşen arama taleplerinin payı</div>
  </div>
  <div style="text-align:right;color:white;display:flex;align-items:center;gap:1rem;">
    <div style="font-size:0.7rem;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;text-align:right;">Tahmini Portföy Değeri<br><span style="font-size:0.65rem;text-transform:none;">Ort. ₺420B standart işlem üzerinden</span></div>
    <div style="font-size:1.6rem;font-weight:800;color:#F5B942;line-height:1;">₺{kpi['total_leads'] * 420_000:,.0f}</div>
  </div>
</div>
""")

st.html("<br>")

# ────────────────────────────────────────────────────────────────────────────
# CHARTS
# ────────────────────────────────────────────────────────────────────────────

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;">Duruma Göre İlanlar</div>')

    status_counts = {
        "Yayında": kpi["live"],
        "İnceleme Bekliyor": kpi["pending_review"],
        "Revizyon İstenen": kpi["revision_requested"],
        "Taslak": kpi["draft"],
        "Reddedildi": kpi["rejected"],
        "Süresi Dolmuş": kpi["expired"],
    }
    colors_donut = ["#22C55E", "#3B82F6", "#F59E0B", "#94A3B8", "#EF4444", "#9CA3AF"]

    fig_donut = go.Figure(data=[go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        hole=0.55,
        marker=dict(colors=colors_donut, line=dict(color="white", width=2)),
        textinfo="label+value",
        textfont_size=12,
    )])
    fig_donut.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>{kpi['total_listings']}</b><br>Toplam", x=0.5, y=0.5,
                          font_size=14, showarrow=False, font_color="#0A1628")],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with chart_col2:
    st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;">Kategoriye Göre İlanlar</div>')

    # Build category counts from all listings
    from components.ui import CATEGORY_ICONS
    cat_counts: dict = {}
    for listing in all_listings:
        m = get_machine(listing.machine_id)
        if m:
            cat = m.category.value.split(" & ")[0]  # short label
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

    if cat_counts:
        sorted_cats = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)
        cat_labels, cat_vals = zip(*sorted_cats)
        fig_bar = go.Figure(data=[go.Bar(
            x=cat_vals,
            y=cat_labels,
            orientation="h",
            marker=dict(
                color=["#1147CC"] * len(cat_vals),
                opacity=[1.0 - (i * 0.08) for i in range(len(cat_vals))],
            ),
            text=cat_vals,
            textposition="outside",
        )])
        fig_bar.update_layout(
            margin=dict(t=20, b=20, l=10, r=40),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ── Simulated leads over time chart ─────────────────────────────────────────
st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;">Talep Sorguları — Son 90 Gün</div>')

# Generate synthetic time series for demo
import random
random.seed(42)
today = datetime.now()
dates = [today - timedelta(days=i) for i in range(89, -1, -1)]
lead_counts = [random.randint(0, 3) for _ in range(90)]
# Spike around seeded lead dates
for i in [38, 22, 12, 5, 8, 2]:
    if i < 90:
        lead_counts[89 - i] += 2

cumulative = []
total = 0
for v in lead_counts:
    total += v
    cumulative.append(total)

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=[d.strftime("%d %b") for d in dates],
    y=lead_counts,
    mode="lines",
    name="Günlük Talepler",
    line=dict(color="#1147CC", width=2.5),
    fill="tozeroy",
    fillcolor="rgba(17,71,204,0.08)",
))
fig_line.add_trace(go.Scatter(
    x=[d.strftime("%d %b") for d in dates],
    y=[sum(lead_counts[:i+1]) for i in range(90)],
    mode="lines",
    name="Kümülatif",
    line=dict(color="#F5B942", width=2, dash="dot"),
    yaxis="y2",
))
fig_line.update_layout(
    height=220,
    margin=dict(t=10, b=30, l=10, r=60),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, tickangle=-30, tickfont_size=10),
    yaxis=dict(showgrid=True, gridcolor="rgba(214,220,232,0.5)", rangemode="tozero"),
    yaxis2=dict(overlaying="y", side="right", showgrid=False, tickfont_size=10),
    legend=dict(font_size=11),
    hovermode="x unified",
)
st.plotly_chart(fig_line, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────
# RECENT LEADS TABLE
# ────────────────────────────────────────────────────────────────────────────

st.html("<br>")
st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">📞 Son Arama Talepleri</div>')

if all_leads:
    lead_data = []
    for lead in sorted(all_leads, key=lambda x: x.submitted_at, reverse=True)[:10]:
        machine = get_machine(lead.machine_id)
        machine_name = f"{machine.brand} {machine.model}" if machine else "Bilinmiyor"
        status_color = {
            "Yeni": "🔵", "İletişime Geçildi": "🟡", "Dönüştü": "🟢", "Kaybedildi": "🔴",
            "New": "🔵", "Contacted": "🟡", "Converted": "🟢", "Lost": "🔴",
        }.get(lead.status, "⚪")
        
        # Translate generic English statuses to Turkish if they are not already
        status_tr = {
            "New": "Yeni", "Contacted": "İletişime Geçildi", "Converted": "Dönüştü", "Lost": "Kaybedildi"
        }.get(lead.status, lead.status)
        
        lead_data.append({
            "Ref": lead.lead_id,
            "Alıcı (Gizlenmiş)": lead.buyer_name,
            "Firma": lead.buyer_company or "—",
            "Makine": machine_name,
            "Tarih": lead.submitted_at.strftime("%d %b %Y"),
            "Durum": f"{status_color} {status_tr}",
        })

    df = pd.DataFrame(lead_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Ref": st.column_config.TextColumn("Ref ID", width="small"),
            "Alıcı (Gizlenmiş)": st.column_config.TextColumn("Müşteri Adı", width="medium"),
            "Firma": st.column_config.TextColumn("Firma", width="medium"),
            "Durum": st.column_config.TextColumn("Durum", width="small"),
        }
    )
else:
    st.info("Henüz talep yok.")

st.html("<br>")

# ── Recent Review Actions ─────────────────────────────────────────────────────
st.html('<div style="font-size:0.9rem;font-weight:700;color:#0A1628;margin-bottom:0.75rem;">⚖️ Son İnceleme İşlemleri</div>')

from data.state import get_review_actions
review_actions = get_review_actions()

if review_actions:
    action_data = []
    for ra in sorted(review_actions, key=lambda x: x.timestamp, reverse=True)[:8]:
        action_icon = {"approved": "✅", "rejected": "❌", "revision_requested": "🔄"}.get(ra.action, "📋")
        action_data.append({
            "Tarih": ra.timestamp.strftime("%d %b %Y"),
            "İlan": ra.listing_id,
            "İnceleme Uzmanı": ra.reviewer_name,
            "İşlem": f"{action_icon} {ra.action.replace('_', ' ').title()}",
            "Yorum": ra.comment[:80] + "..." if len(ra.comment) > 80 else ra.comment,
        })
    df_actions = pd.DataFrame(action_data)
    st.dataframe(
        df_actions, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "İşlem": st.column_config.TextColumn("Denetim İşlemi", width="medium"),
            "Yorum": st.column_config.TextColumn("İç Yorum", width="large")
        }
    )

render_footer()
