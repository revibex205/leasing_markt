# LeaseMarkt — Bank-Approved Machinery Discovery Platform

**A Python/Streamlit prototype** for a bank-approved second-hand machinery discovery and leasing lead platform.

## Purpose
This platform enables bank leasing customers to list their end-of-lease machines for sale. Public buyers can discover and express interest. The bank converts that interest into new leasing leads — combining its review and trust advantage with open-market demand.

## Architecture
```
lease_markt/
├── app.py                     # Landing page (Streamlit entry point)
├── pages/
│   ├── 1_Marketplace.py       # Public machine catalogue
│   ├── 2_Machine_Detail.py    # Single machine detail view
│   ├── 3_Lead_Form.py         # Buyer "call me back" lead form
│   ├── 4_Seller_Dashboard.py  # Seller portal (listing management)
│   ├── 5_Create_Listing.py    # Seller listing creation flow
│   ├── 6_Bank_Review.py       # Bank review & approval panel
│   └── 7_Admin_Dashboard.py   # Admin analytics & KPIs
├── data/
│   ├── models.py              # Dataclass definitions & status enum
│   ├── seed_data.py           # Synthetic demo data
│   └── state.py               # Session state management
├── components/
│   ├── ui.py                  # Shared UI components (cards, badges, nav)
│   └── styles.py              # Custom CSS injection
├── assets/
│   └── generate_assets.py     # Machine placeholder image generator
├── requirements.txt
└── README.md
```

## Quick Start

```bash
# 1. Clone / navigate to project
cd /home/user1/lease_markt

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate placeholder machine images
python assets/generate_assets.py

# 5. Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Role Switching (Demo Navigation)
Use the **role selector** in the top navigation to switch between:
- 🌐 **Public Visitor** — browse the marketplace and submit lead forms
- 🏭 **Seller (Leasing Customer)** — manage listings and submit machines for review
- 🏦 **Bank Admin** — review listings, approve/reject, monitor analytics

## User Flow Summary
1. **Public buyer** browses catalogue → views machine detail → clicks "Call Me Back"
2. **Seller** logs in from internet banking → selects eligible machine → creates listing → submits for review
3. **Bank reviewer** reviews listing, checks internal quality score → approves, requests revision, or rejects
4. **Live listing** appears on public marketplace → drives new leasing lead enquiries

## Notes
- All data is synthetic and in-memory (`st.session_state`)
- No database or authentication required for demo
- Seller identities are masked on all public-facing pages
- Internal bank quality scores are only visible in the Bank Review panel
- The leasing calculator module is a placeholder (future-ready area)
