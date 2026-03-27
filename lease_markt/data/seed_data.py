"""
data/seed_data.py
Synthetic demo data for LeaseMarkt.
All identities are masked / fictional. No real personal data.
Translated to Turkish.
"""

from datetime import date, datetime, timedelta
from data.models import (
    Machine, Listing, Lead, SellerProfile, ReviewAction,
    ListingStatus, MachineCategory
)

# ─── Seller Profiles (masked) ─────────────────────────────────────────────────

SELLERS = [
    SellerProfile(
        seller_id="S001",
        masked_name="M****i Makina A.Ş.",
        city="İstanbul",
        member_since_year=2018,
        leasing_customer_since=2018,
        verified=True,
    ),
    SellerProfile(
        seller_id="S002",
        masked_name="A**** İnşaat Ltd.",
        city="Ankara",
        member_since_year=2019,
        leasing_customer_since=2020,
        verified=True,
    ),
    SellerProfile(
        seller_id="S003",
        masked_name="T***** Tarım Kooperatifi",
        city="Konya",
        member_since_year=2020,
        leasing_customer_since=2020,
        verified=True,
    ),
    SellerProfile(
        seller_id="S004",
        masked_name="E*** Endüstri A.Ş.",
        city="İzmir",
        member_since_year=2017,
        leasing_customer_since=2017,
        verified=True,
    ),
    SellerProfile(
        seller_id="S005",
        masked_name="K****r Lojistik Ltd.",
        city="Bursa",
        member_since_year=2021,
        leasing_customer_since=2021,
        verified=True,
    ),
]

# ─── Machines (from leasing history) ─────────────────────────────────────────

MACHINES = [
    Machine(
        machine_id="M001",
        seller_id="S001",
        brand="Caterpillar",
        model="320D Ekskavatör",
        category=MachineCategory.CONSTRUCTION,
        production_year=2019,
        serial_number="CAT****32**",
        engine_hours=4200,
        weight_kg=21500,
        description=(
            "Şehir içi inşaat projelerinde kullanılmış bakımlı hidrolik ekskavatör. "
            "Tüm servis geçmişi mevcuttur. Kova ve hidrolik hortumlar 2023 yılında yenilendi. "
            "Yaşına göre düşük motor saati ile mükemmel çalışma koşulunda."
        ),
        image_files=["cat_320d.png"],
        internal_quality_score=88,
        market_reference_price=2_850_000,
        leasing_contract_end_date=date(2025, 6, 30),
    ),
    Machine(
        machine_id="M002",
        seller_id="S002",
        brand="Liebherr",
        model="LTM 1060-3.1 Mobil Vinç",
        category=MachineCategory.CONSTRUCTION,
        production_year=2018,
        serial_number="LBH****18**",
        engine_hours=6100,
        weight_kg=48000,
        description=(
            "60 ton kapasiteli arazi tipi mobil vinç. Endüstriyel tesis kurulumu "
            "ve köprü inşaatlarında kullanıldı. Tüm belgeler ve sertifikalar dahil. "
            "Yetkili serviste düzenli bakımları yapıldı."
        ),
        image_files=["liebherr_crane.png"],
        internal_quality_score=76,
        market_reference_price=5_200_000,
        leasing_contract_end_date=date(2025, 3, 31),
    ),
    Machine(
        machine_id="M003",
        seller_id="S003",
        brand="John Deere",
        model="6130M Traktör",
        category=MachineCategory.AGRICULTURAL,
        production_year=2021,
        serial_number="JD****21**",
        engine_hours=1850,
        weight_kg=6200,
        description=(
            "CommandQuad şanzımanlı 130 HP çok amaçlı traktör. Konya ovasında tahıl ve ayçiçeği "
            "tarımında kullanıldı. Klimalı kabin, ön yükleyici ve arka bağlantı dahildir. "
            "Çok düşük saatte, mükemmel durumda."
        ),
        image_files=["jd_6130m.png"],
        internal_quality_score=93,
        market_reference_price=1_650_000,
        leasing_contract_end_date=date(2025, 9, 30),
    ),
    Machine(
        machine_id="M004",
        seller_id="S004",
        brand="Mazak",
        model="INTEGREX i-400S CNC",
        category=MachineCategory.MANUFACTURING,
        production_year=2020,
        serial_number="MZK****20**",
        engine_hours=None,
        weight_kg=14000,
        description=(
            "Entegre iş mili ve tornalama kapasitesine sahip 5 eksenli CNC işleme merkezi. "
            "Havacılık, otomotiv ve hassas parça üretimi için ideal. "
            "Tam takım paketi dahil. Yazılım lisansları devredilebilir."
        ),
        image_files=["mazak_integrex.png"],
        internal_quality_score=91,
        market_reference_price=4_400_000,
        leasing_contract_end_date=date(2025, 12, 31),
    ),
    Machine(
        machine_id="M005",
        seller_id="S001",
        brand="Toyota",
        model="8FBE18 Elektrikli Forklift",
        category=MachineCategory.MATERIAL_HANDLING,
        production_year=2022,
        serial_number="TOY****22**",
        engine_hours=2100,
        weight_kg=3800,
        description=(
            "1.8 ton kapasiteli elektrikli denge ağırlıklı forklift. Gümrüklü antrepo lojistiğinde kullanıldı. "
            "Lityum-iyon batarya paketi 2024'te yenilendi. Çok temiz, sadece kapalı alanda kullanılmış cihaz."
        ),
        image_files=["toyota_forklift.png"],
        internal_quality_score=95,
        market_reference_price=680_000,
        leasing_contract_end_date=date(2025, 4, 30),
    ),
    Machine(
        machine_id="M006",
        seller_id="S005",
        brand="Komatsu",
        model="PC210LC-11 Ekskavatör",
        category=MachineCategory.CONSTRUCTION,
        production_year=2020,
        serial_number="KOM****20**",
        engine_hours=3900,
        weight_kg=22000,
        description=(
            "21 tonluk hidrolik paletli ekskavatör. Komatsu KOMTRAX telematik sistemi kurulu. "
            "Marmara bölgesindeki altyapı ve yol inşaatlarında kullanıldı. "
            "Tam servis kitapçığı ile temiz, bakımlı cihaz."
        ),
        image_files=["komatsu_pc210.png"],
        internal_quality_score=84,
        market_reference_price=2_650_000,
        leasing_contract_end_date=date(2025, 7, 31),
    ),
    Machine(
        machine_id="M007",
        seller_id="S004",
        brand="Heidelberg",
        model="Speedmaster XL 75 Ofset Baskı",
        category=MachineCategory.PRINTING,
        production_year=2019,
        serial_number="HDB****19**",
        engine_hours=None,
        weight_kg=11500,
        description=(
            "5 renk + lak ofset baskı makinesi. Prinect iş akışı entegrasyonu. "
            "Toplam 125 milyon baskı. Ticari ve ambalaj baskı üretiminde kullanıldı. "
            "Yetkili bayiden tam servis sözleşmesi geçmişi mevcuttur."
        ),
        image_files=["heidelberg_press.png"],
        internal_quality_score=79,
        market_reference_price=3_100_000,
        leasing_contract_end_date=date(2025, 11, 30),
    ),
    Machine(
        machine_id="M008",
        seller_id="S003",
        brand="New Holland",
        model="CR9.90 Biçerdöver",
        category=MachineCategory.AGRICULTURAL,
        production_year=2020,
        serial_number="NH****20**",
        engine_hours=1620,
        weight_kg=18500,
        description=(
            "9.0L motor ve 40-ft tablaya sahip çift rotorlu biçerdöver. "
            "PLM Intelligence hassas tarım hazır. "
            "Yıllık bakımları yapılmış, kapalı alanda muhafaza edilmiştir. Tahıl tarım operasyonları için ideal."
        ),
        image_files=["nh_cr990.png"],
        internal_quality_score=87,
        market_reference_price=3_800_000,
        leasing_contract_end_date=date(2025, 8, 31),
    ),
    Machine(
        machine_id="M009",
        seller_id="S002",
        brand="Atlas Copco",
        model="QAC 800 Jeneratör",
        category=MachineCategory.ENERGY,
        production_year=2021,
        serial_number="ATC****21**",
        engine_hours=5200,
        weight_kg=9800,
        description=(
            "Bir üretim tesisi için birincil yedek güç olarak kullanılan 800 kVA dizel jeneratör. "
            "Senkronizasyon kapasitesi, dış hava şartlarına dayanıklı kabin. "
            "Tüm bakım kayıtları mevcuttur."
        ),
        image_files=["atlasc_gen.png"],
        internal_quality_score=72,
        market_reference_price=1_890_000,
        leasing_contract_end_date=date(2025, 5, 31),
    ),
    Machine(
        machine_id="M010",
        seller_id="S005",
        brand="Mercedes-Benz",
        model="Actros 1848 LS Tır",
        category=MachineCategory.TRANSPORT,
        production_year=2022,
        serial_number="MBZ****22**",
        engine_hours=None,
        weight_kg=18000,
        description=(
            "480 HP OM 471 motorlu ve 12 vitesli PowerShift 3 şanzımanlı uzun yol tırı. "
            "MirrorCam sistemi ve Aktif Fren Asistanı 5. 320.000 km, tek kullanıcılı, tam servis geçmişi."
        ),
        image_files=["mb_actros.png"],
        internal_quality_score=82,
        market_reference_price=2_200_000,
        leasing_contract_end_date=date(2025, 10, 31),
    ),
]

# Helper: machine lookup dict
MACHINE_MAP = {m.machine_id: m for m in MACHINES}
SELLER_MAP = {s.seller_id: s for s in SELLERS}


# ─── Listings ─────────────────────────────────────────────────────────────────

_now = datetime.now()
_today = date.today()

def _dt(days_ago: int) -> datetime:
    return _now - timedelta(days=days_ago)

def _exp(months: int) -> date:
    return _today + timedelta(days=30 * months)

LISTINGS = [
    # --- LIVE / APPROVED listings ---
    Listing(
        listing_id="L001", machine_id="M001", seller_id="S001",
        asking_price=2_650_000, currency="TRY",
        location_city="İstanbul", location_region="Marmara",
        additional_notes="KDV dahil değildir. Makine Pendik'teki depomuzda incelenebilir.",
        condition_notes="Mükemmel çalışma durumunda. Tam servis defteri mevcuttur.",
        status=ListingStatus.LIVE,
        duration_months=3,
        created_at=_dt(45), submitted_at=_dt(44), approved_at=_dt(40),
        expires_at=_exp(3),
        reviewer_comment="Kalite puanı 88 — piyasa referansına göre fiyat makul. Onaylandı.",
        approved_duration_months=3,
    ),
    Listing(
        listing_id="L002", machine_id="M003", seller_id="S003",
        asking_price=1_550_000, currency="TRY",
        location_city="Konya", location_region="İç Anadolu",
        additional_notes="Ön yükleyici ve 3 nokta askı sistemi dahildir. Sahada test edilebilir.",
        condition_notes="Düşük saatte, yeni gibi makine. Tüm belgeler tam.",
        status=ListingStatus.LIVE,
        duration_months=2,
        created_at=_dt(20), submitted_at=_dt(19), approved_at=_dt(15),
        expires_at=_exp(2),
        reviewer_comment="Mükemmel kalite puanı 93. Fiyat piyasanın biraz altında — onaylandı.",
        approved_duration_months=2,
    ),
    Listing(
        listing_id="L003", machine_id="M004", seller_id="S004",
        asking_price=4_200_000, currency="TRY",
        location_city="İzmir", location_region="Ege",
        additional_notes="Tam takım seti ve yazılım lisansları dahildir. Uzaktan demo yapılabilir.",
        condition_notes="Üretim sınıfı cihaz. Tüm kalibrasyon sertifikaları mevcuttur.",
        status=ListingStatus.LIVE,
        duration_months=4,
        created_at=_dt(30), submitted_at=_dt(29), approved_at=_dt(25),
        expires_at=_exp(4),
        reviewer_comment="Yüksek değerli endüstriyel varlık, kalite puanı 91. 4 aylık liste kaydı için onaylandı.",
        approved_duration_months=4,
    ),
    Listing(
        listing_id="L004", machine_id="M005", seller_id="S001",
        asking_price=650_000, currency="TRY",
        location_city="İstanbul", location_region="Marmara",
        additional_notes="Batarya garanti devri dahildir. İstanbul içi teslimat yapılabilir.",
        condition_notes="Sadece kapalı alanda kullanılmıştır, çok temiz.",
        status=ListingStatus.LIVE,
        duration_months=2,
        created_at=_dt(10), submitted_at=_dt(9), approved_at=_dt(6),
        expires_at=_exp(2),
        reviewer_comment="Kalite puanı 95 — premium durum. Onaylandı.",
        approved_duration_months=2,
    ),
    Listing(
        listing_id="L005", machine_id="M008", seller_id="S003",
        asking_price=3_600_000, currency="TRY",
        location_city="Konya", location_region="İç Anadolu",
        additional_notes="Gelecek hasat sezonu için hazırdır. Tabla ayrı olarak depolanmaktadır.",
        condition_notes="Sezonsal durumu harika, boyutuna göre saatler düşük.",
        status=ListingStatus.LIVE,
        duration_months=3,
        created_at=_dt(15), submitted_at=_dt(14), approved_at=_dt(10),
        expires_at=_exp(3),
        reviewer_comment="Kalite puanı 87, sezonsal ürünler — onaylandı.",
        approved_duration_months=3,
    ),
    # --- SUBMITTED (pending review) ---
    Listing(
        listing_id="L006", machine_id="M006", seller_id="S005",
        asking_price=2_500_000, currency="TRY",
        location_city="Bursa", location_region="Marmara",
        additional_notes="Bursa park sahamızda incelenebilir.",
        condition_notes="İyi çalışma durumunda. Bazı kozmetik aşınmalar mevcut.",
        status=ListingStatus.SUBMITTED,
        duration_months=3,
        created_at=_dt(3), submitted_at=_dt(2),
    ),
    Listing(
        listing_id="L007", machine_id="M009", seller_id="S002",
        asking_price=1_750_000, currency="TRY",
        location_city="Ankara", location_region="İç Anadolu",
        additional_notes="Uzak saha operasyonları için uygundur.",
        condition_notes="Jeneratörün saatleri yüksek fakat iyi bakımlıdır.",
        status=ListingStatus.SUBMITTED,
        duration_months=2,
        created_at=_dt(1), submitted_at=_dt(1),
    ),
    Listing(
        listing_id="L008", machine_id="M010", seller_id="S005",
        asking_price=2_100_000, currency="TRY",
        location_city="Bursa", location_region="Marmara",
        additional_notes="Mercedes yetkili bayisinde tam servis geçmişi mevcuttur.",
        condition_notes="Mükemmel durumda, tek kullanıcı.",
        status=ListingStatus.SUBMITTED,
        duration_months=4,
        created_at=_dt(2), submitted_at=_dt(1),
    ),
    # --- REVISION REQUESTED ---
    Listing(
        listing_id="L009", machine_id="M002", seller_id="S002",
        asking_price=5_800_000, currency="TRY",
        location_city="Ankara", location_region="İç Anadolu",
        additional_notes="Arma ve denge ayak yastıkları dahildir.",
        condition_notes="Operasyonel, bazı hidrolik servis vakti gelmiştir.",
        status=ListingStatus.REVISION_REQUESTED,
        duration_months=3,
        created_at=_dt(14), submitted_at=_dt(13),
        reviewer_comment=(
            "₺5.800.000 talep fiyatı ₺5.200.000 olan piyasa referansımızın belirgin şekilde üzerinde. "
            "Lütfen talep fiyatını revize edin veya ilave gerekçeler sunun (örneğin opsiyonel donanımlar, "
            "yakın zamanda yapılmış ağır bakım). Ayrıca lütfen hidrolik servis durumunu netleştirin."
        ),
        revision_history=["İlk başvuru — fiyat revizyonu incelemeci K. Arslan tarafından talep edildi."],
    ),
    Listing(
        listing_id="L010", machine_id="M007", seller_id="S004",
        asking_price=3_300_000, currency="TRY",
        location_city="İzmir", location_region="Ege",
        additional_notes="Tam baskı iş akışı yazılımı dahildir.",
        condition_notes="Baskı kafaları yakın zamanda bakıma girdi.",
        status=ListingStatus.REVISION_REQUESTED,
        duration_months=4,
        created_at=_dt(7), submitted_at=_dt(6),
        reviewer_comment=(
            "Lütfen toplam baskı sayısı ve baskı kauçuklarının güncel durumu hakkında daha fazla detay sağlayın. "
            "Ayrıca fotoğraflarda kontrol konsolu ve besleyici ünite net bir şekilde görünmelidir."
        ),
        revision_history=["İlave belgeler incelemeci S. Yıldız tarafından talep edildi."],
    ),
    # --- DRAFT ---
    Listing(
        listing_id="L011", machine_id="M009", seller_id="S002",
        asking_price=1_800_000, currency="TRY",
        location_city="Ankara", location_region="İç Anadolu",
        status=ListingStatus.DRAFT,
        duration_months=2,
        created_at=_dt(5),
    ),
    # --- EXPIRED ---
    Listing(
        listing_id="L012", machine_id="M006", seller_id="S005",
        asking_price=2_400_000, currency="TRY",
        location_city="Bursa", location_region="Marmara",
        status=ListingStatus.EXPIRED,
        duration_months=1,
        created_at=_dt(65), submitted_at=_dt(64), approved_at=_dt(60),
        expires_at=_today - timedelta(days=30),
        reviewer_comment="Onaylandı.",
        approved_duration_months=1,
    ),
]


# ─── Leads (Buyer Callback Requests) ─────────────────────────────────────────

LEADS = [
    Lead(
        lead_id="LD001", listing_id="L001", machine_id="M001",
        buyer_name="Emre K.",
        buyer_company="K**** Yapı A.Ş.",
        buyer_phone="+90 532 *** ** 41",
        buyer_email="e.k****@kyyy.com.tr",
        interest_notes="Haziran ayında başlayacak yol projesi için ekskavatöre acil ihtiyacım var.",
        submitted_at=_dt(38), status="İletişime Geçildi",
    ),
    Lead(
        lead_id="LD002", listing_id="L003", machine_id="M004",
        buyer_name="Burak T.",
        buyer_company="T*** Havacılık Ltd.",
        buyer_phone="+90 544 *** ** 07",
        buyer_email="b.t****@taero.com",
        interest_notes="Finansman seçenekleriyle ilgileniyorum — şu anda 3 benzer makineyi de değerlendiriyoruz.",
        submitted_at=_dt(22), status="Yeni",
    ),
    Lead(
        lead_id="LD003", listing_id="L002", machine_id="M003",
        buyer_name="Hasan O.",
        buyer_company="O*** Tarım Ltd.",
        buyer_phone="+90 505 *** ** 18",
        buyer_email="h.o****@otarim.com.tr",
        interest_notes="Bu sezon için traktör arayışımız var — finansman mevcut ise hızlıca imzalayabiliriz.",
        submitted_at=_dt(12), status="Dönüştü",
    ),
    Lead(
        lead_id="LD004", listing_id="L004", machine_id="M005",
        buyer_name="Zeynep A.",
        buyer_company="A*** Lojistik A.Ş.",
        buyer_phone="+90 542 *** ** 33",
        buyer_email="z.a****@alog.com.tr",
        interest_notes="2 birime ihtiyacımız var, bunun yanına başka bir birim eklenebilir mi?",
        submitted_at=_dt(5), status="Yeni",
    ),
    Lead(
        lead_id="LD005", listing_id="L005", machine_id="M008",
        buyer_name="Mehmet Y.",
        buyer_company="Y*** Tarım Kooperatifi",
        buyer_phone="+90 533 *** ** 55",
        buyer_email="m.y****@ytk.org.tr",
        interest_notes="Kooperatifimiz büyüyor. Bu biçerdöver 3 köye hizmet verecek.",
        submitted_at=_dt(8), status="Yeni",
    ),
    Lead(
        lead_id="LD006", listing_id="L001", machine_id="M001",
        buyer_name="Ali R.",
        buyer_company="R*** İnşaat Ltd.",
        buyer_phone="+90 551 *** ** 29",
        buyer_email="a.r****@rins.com.tr",
        interest_notes="Bunu Pendik'te gördüm — çok ilgileniyorum.",
        submitted_at=_dt(2), status="Yeni",
    ),
]


# ─── Review Audit Log ─────────────────────────────────────────────────────────

REVIEW_ACTIONS = [
    ReviewAction(
        action_id="RA001", listing_id="L001",
        reviewer_name="K. Arslan",
        action="onaylandı",
        comment="Kalite puanı 88 — piyasa referansına göre fiyat makul. Onaylandı.",
        timestamp=_dt(40), approved_duration_months=3,
    ),
    ReviewAction(
        action_id="RA002", listing_id="L002",
        reviewer_name="S. Yıldız",
        action="onaylandı",
        comment="Mükemmel kalite puanı 93. Fiyat piyasanın biraz altında — onaylandı.",
        timestamp=_dt(15), approved_duration_months=2,
    ),
    ReviewAction(
        action_id="RA003", listing_id="L009",
        reviewer_name="K. Arslan",
        action="revizyon_istendi",
        comment="Talep fiyatı piyasa değerinin belirgin şekilde üzerinde. Revizyon talep edildi.",
        timestamp=_dt(10),
    ),
    ReviewAction(
        action_id="RA004", listing_id="L003",
        reviewer_name="B. Çelik",
        action="onaylandı",
        comment="Yüksek değerli endüstriyel varlık. 4 aylık liste kaydı için onaylandı.",
        timestamp=_dt(25), approved_duration_months=4,
    ),
    ReviewAction(
        action_id="RA005", listing_id="L010",
        reviewer_name="S. Yıldız",
        action="revizyon_istendi",
        comment="Baskı detayları hakkında daha fazla bilgi gerekli.",
        timestamp=_dt(4),
    ),
]
