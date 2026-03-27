"""
data/state.py
Centralized session state management for LeaseMarkt.
All runtime mutations go through these helper functions.
"""

import streamlit as st
from datetime import datetime, date, timedelta
from copy import deepcopy
from typing import List, Optional

from data.models import Listing, Lead, ReviewAction, ListingStatus
from data.seed_data import (
    LISTINGS, LEADS, MACHINES, SELLERS, REVIEW_ACTIONS,
    MACHINE_MAP, SELLER_MAP,
)


def init_state():
    """Initialise session state on first load (idempotent)."""
    if st.session_state.get("_initialized"):
        return

    st.session_state["listings"] = deepcopy(LISTINGS)
    st.session_state["leads"] = deepcopy(LEADS)
    st.session_state["review_actions"] = deepcopy(REVIEW_ACTIONS)
    st.session_state["machines"] = MACHINES
    st.session_state["sellers"] = SELLERS

    # Current user role: "public" | "seller" | "bank"
    st.session_state["current_role"] = "public"
    # Current seller context (for demo: S001 is active seller)
    st.session_state["current_seller_id"] = "S001"
    # Selected machine/listing for detail/edit pages
    st.session_state["selected_machine_id"] = None
    st.session_state["selected_listing_id"] = None
    # Lead form pre-fill
    st.session_state["lead_form_listing_id"] = None
    # Create listing wizard step
    st.session_state["create_listing_step"] = 1
    st.session_state["create_listing_data"] = {}

    st.session_state["_initialized"] = True


# ─── Accessors ────────────────────────────────────────────────────────────────

def get_listings(
    status: Optional[List[ListingStatus]] = None,
    seller_id: Optional[str] = None,
) -> List[Listing]:
    """Return listings filtered by optional status list and/or seller."""
    listings = st.session_state["listings"]
    if status:
        listings = [l for l in listings if l.status in status]
    if seller_id:
        listings = [l for l in listings if l.seller_id == seller_id]
    return listings


def get_public_listings() -> List[Listing]:
    """Return only Live listings (visible to public)."""
    return get_listings(status=[ListingStatus.LIVE])


def get_listing_by_id(listing_id: str) -> Optional[Listing]:
    for l in st.session_state["listings"]:
        if l.listing_id == listing_id:
            return l
    return None


def get_machine(machine_id: str):
    return MACHINE_MAP.get(machine_id)


def get_seller(seller_id: str):
    return SELLER_MAP.get(seller_id)


def get_leads(listing_id: Optional[str] = None) -> List[Lead]:
    leads = st.session_state["leads"]
    if listing_id:
        leads = [l for l in leads if l.listing_id == listing_id]
    return leads


def get_review_actions(listing_id: Optional[str] = None) -> List[ReviewAction]:
    actions = st.session_state["review_actions"]
    if listing_id:
        actions = [a for a in actions if a.listing_id == listing_id]
    return actions


# ─── Mutators ─────────────────────────────────────────────────────────────────

def update_listing_status(
    listing_id: str,
    new_status: ListingStatus,
    reviewer_comment: str = "",
    approved_duration_months: Optional[int] = None,
    reviewer_name: str = "Bank Reviewer",
) -> bool:
    """Update a listing's status and record the review action."""
    now = datetime.now()
    today = date.today()

    for listing in st.session_state["listings"]:
        if listing.listing_id != listing_id:
            continue

        listing.status = new_status
        listing.reviewer_comment = reviewer_comment

        if new_status == ListingStatus.SUBMITTED:
            listing.submitted_at = now
        elif new_status == ListingStatus.LIVE:
            listing.approved_at = now
            dur = approved_duration_months or listing.duration_months
            listing.approved_duration_months = dur
            listing.expires_at = today + timedelta(days=30 * dur)
        elif new_status == ListingStatus.REVISION_REQUESTED:
            listing.revision_history.append(
                f"{now.strftime('%d %b %Y')} — {reviewer_comment[:80]}..."
            )

        # Record review action for audit trail
        action_id = f"RA{len(st.session_state['review_actions']) + 1:03d}"
        action_map = {
            ListingStatus.LIVE: "approved",
            ListingStatus.REJECTED: "rejected",
            ListingStatus.REVISION_REQUESTED: "revision_requested",
        }
        if new_status in action_map:
            st.session_state["review_actions"].append(
                ReviewAction(
                    action_id=action_id,
                    listing_id=listing_id,
                    reviewer_name=reviewer_name,
                    action=action_map[new_status],
                    comment=reviewer_comment,
                    timestamp=now,
                    approved_duration_months=approved_duration_months,
                )
            )
        return True
    return False


def add_listing(listing: Listing):
    """Append a new listing to session state."""
    st.session_state["listings"].append(listing)


def update_listing_fields(listing_id: str, **kwargs):
    """Update arbitrary fields on a listing by ID."""
    for listing in st.session_state["listings"]:
        if listing.listing_id == listing_id:
            for key, value in kwargs.items():
                setattr(listing, key, value)
            return True
    return False


def add_lead(lead: Lead):
    """Append a new buyer lead to session state."""
    st.session_state["leads"].append(lead)


def next_listing_id() -> str:
    existing = [l.listing_id for l in st.session_state["listings"]]
    nums = [int(lid[1:]) for lid in existing if lid.startswith("L") and lid[1:].isdigit()]
    return f"L{(max(nums) + 1 if nums else 1):03d}"


def next_lead_id() -> str:
    existing = [l.lead_id for l in st.session_state["leads"]]
    nums = [int(lid[2:]) for lid in existing if lid.startswith("LD") and lid[2:].isdigit()]
    return f"LD{(max(nums) + 1 if nums else 1):03d}"


# ─── Summary Statistics ───────────────────────────────────────────────────────

def get_kpi_summary() -> dict:
    """Compute platform-wide KPI counts for the admin dashboard."""
    listings = st.session_state["listings"]
    leads = st.session_state["leads"]
    today = date.today()

    # Check and mark expired listings
    for l in listings:
        if l.status == ListingStatus.LIVE and l.expires_at and l.expires_at < today:
            l.status = ListingStatus.EXPIRED

    status_counts = {s: 0 for s in ListingStatus}
    for l in listings:
        status_counts[l.status] += 1

    converted = sum(1 for ld in leads if ld.status == "Converted")

    return {
        "total_listings": len(listings),
        "live": status_counts[ListingStatus.LIVE],
        "pending_review": status_counts[ListingStatus.SUBMITTED],
        "revision_requested": status_counts[ListingStatus.REVISION_REQUESTED],
        "approved": status_counts[ListingStatus.APPROVED],
        "rejected": status_counts[ListingStatus.REJECTED],
        "expired": status_counts[ListingStatus.EXPIRED],
        "draft": status_counts[ListingStatus.DRAFT],
        "total_leads": len(leads),
        "converted_leads": converted,
        "new_leads": sum(1 for ld in leads if ld.status == "New"),
        "contacted_leads": sum(1 for ld in leads if ld.status == "Contacted"),
    }
