"""
data/models.py
Dataclass definitions and status enums for LeaseMarkt.
All business entities are defined here and shared across all modules.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


# ─── Status Enumerations ──────────────────────────────────────────────────────

class ListingStatus(str, Enum):
    DRAFT = "Taslak"
    SUBMITTED = "İnceleme Bekliyor"
    REVISION_REQUESTED = "Revizyon İstendi"
    APPROVED = "Onaylandı"
    LIVE = "Yayında"
    REJECTED = "Reddedildi"
    EXPIRED = "Süresi Doldu"
    CLOSED = "Kapalı"


class MachineCategory(str, Enum):
    CONSTRUCTION = "İş Makinesi"
    AGRICULTURAL = "Tarım Makinesi"
    MANUFACTURING = "İmalat & CNC"
    MATERIAL_HANDLING = "İstif & Depolama"
    PRINTING = "Matbaa & Ambalaj"
    FOOD_PROCESSING = "Gıda İşleme"
    ENERGY = "Enerji Sistemleri"
    TRANSPORT = "Ticari Araçlar"


class ListingDuration(int, Enum):
    ONE_MONTH = 1
    TWO_MONTHS = 2
    THREE_MONTHS = 3
    FOUR_MONTHS = 4
    FIVE_MONTHS = 5
    SIX_MONTHS = 6


# ─── Core Data Models ─────────────────────────────────────────────────────────

@dataclass
class SellerProfile:
    """
    Existing bank leasing customer who can create listings.
    Identity is masked on all public-facing pages.
    """
    seller_id: str
    masked_name: str          # e.g. "M****i Makina A.Ş." — shown publicly
    city: str
    member_since_year: int
    leasing_customer_since: int
    verified: bool = True


@dataclass
class Machine:
    """
    A physical machine from a seller's leasing history.
    Only machines from completed/ending leasing contracts are eligible for listing.
    """
    machine_id: str
    seller_id: str
    brand: str
    model: str
    category: MachineCategory
    production_year: int
    serial_number: str        # masked for public
    engine_hours: Optional[int]   # operating hours
    weight_kg: Optional[int]
    description: str
    image_files: List[str]    # list of asset filenames
    # Bank-internal fields
    internal_quality_score: int   # 1–100, visible only to bank admin
    market_reference_price: float # bank's market price estimate
    leasing_contract_end_date: date


@dataclass
class Listing:
    """
    A marketplace listing wrapping a Machine, created by a Seller.
    Tracks the full lifecycle from Draft to Live/Expired.
    """
    listing_id: str
    machine_id: str
    seller_id: str
    asking_price: float
    currency: str = "TRY"
    location_city: str = ""
    location_region: str = ""
    additional_notes: str = ""
    condition_notes: str = ""
    status: ListingStatus = ListingStatus.DRAFT
    duration_months: int = 3          # 1–6 months
    created_at: datetime = field(default_factory=datetime.now)
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    expires_at: Optional[date] = None
    # Bank review fields
    reviewer_comment: str = ""
    revision_history: List[str] = field(default_factory=list)
    approved_duration_months: Optional[int] = None


@dataclass
class Lead:
    """
    Buyer callback request — the core business output of the platform.
    Each lead is a potential new leasing opportunity for the bank.
    """
    lead_id: str
    listing_id: str
    machine_id: str
    buyer_name: str
    buyer_company: str
    buyer_phone: str
    buyer_email: str
    interest_notes: str
    submitted_at: datetime = field(default_factory=datetime.now)
    status: str = "Yeni"    # Yeni | İletişime Geçildi | Dönüştü | Kaybedildi


@dataclass
class ReviewAction:
    """
    Audit trail of bank review actions on a listing.
    """
    action_id: str
    listing_id: str
    reviewer_name: str
    action: str           # "approved" | "rejected" | "revision_requested"
    comment: str
    timestamp: datetime = field(default_factory=datetime.now)
    approved_duration_months: Optional[int] = None
