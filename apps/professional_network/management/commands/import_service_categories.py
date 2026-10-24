from django.core.management.base import BaseCommand
from apps.professional_network.service_categries.models import (
    ServiceCategory,
    ServiceAttribute,
    ServiceListing,
    ServiceVariationPlan,
)


class Command(BaseCommand):
    help = "உலகளாவிய சேவைக் கேட்டகிரிகள், சப்-கேட்டகிரிகள், அட்ரிபியூட்டுகள் மற்றும் திட்டங்களை (Plans) இம்போர்ட் செய்கிறது."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("உலகளாவிய சேவைகள் இம்போர்ட் செய்யப்படுகின்றன..."))

        # உலகளாவிய சேவைத் தரவுகள் (Global Service Taxonomy)
        global_services_data = [
            # 1. Home & Repair Services
            {
                "name": "Home & Repair Services",
                "google_business_category": "Home Repair & Maintenance",
                "sac_code": "998734",
                "subcategories": [
                    {
                        "name": "Electrician",
                        "google_business_category": "Electrician",
                        "sac_code": "998735",
                        "attributes": ["License Type", "Wiring Expertise", "Emergency Service Available"],
                        "listings": [
                            {
                                "title": "Residential Electrical Wiring & Repair",
                                "description": "Complete household wiring, switchboard installation, and fault finding.",
                                "plans": [
                                    {"plan_name": "Basic Inspection", "description": "General checkup and minor fix", "price": 499.00, "estimated_duration": "1 Hour"},
                                    {"plan_name": "Standard Repair", "description": "Switchboard/Fan installation or wiring fix", "price": 1200.00, "estimated_duration": "2-3 Hours"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Plumber",
                        "google_business_category": "Plumber",
                        "sac_code": "998736",
                        "attributes": ["Pipe Material Expertise", "Leak Detection Tools"],
                        "listings": [
                            {
                                "title": "Pipe Leakage & Sanitary Installation",
                                "description": "Fixing leaking pipes, tap replacements, and bathroom fittings.",
                                "plans": [
                                    {"plan_name": "Quick Leak Fix", "description": "Patching or replacing a single leaky pipe/tap", "price": 600.00, "estimated_duration": "1 Hour"},
                                ]
                            }
                        ]
                    }
                ]
            },
            # 2. Healthcare & Wellness
            {
                "name": "Healthcare & Wellness",
                "google_business_category": "Health & Medical",
                "sac_code": "999312",
                "subcategories": [
                    {
                        "name": "Doctor / General Physician",
                        "google_business_category": "Medical Clinic",
                        "sac_code": "999313",
                        "attributes": ["Medical Registration Number", "Specialization", "Consultation Mode"],
                        "listings": [
                            {
                                "title": "Online / Home Consultation",
                                "description": "General health checkup and prescription services.",
                                "plans": [
                                    {"plan_name": "Standard Consultation", "description": "15-minute detailed health discussion", "price": 500.00, "estimated_duration": "15 Minutes"},
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Yoga & Fitness Trainer",
                        "google_business_category": "Yoga Studio",
                        "sac_code": "999659",
                        "attributes": ["Certification Level", "Specialty (Hatha, Ashtanga, Weight Loss)"],
                        "listings": [
                            {
                                "title": "Personal Yoga & Fitness Training",
                                "description": "Customized wellness and yoga sessions at home or online.",
                                "plans": [
                                    {"plan_name": "Monthly Yoga Package", "description": "12 sessions per month", "price": 3500.00, "estimated_duration": "1 Month"},
                                ]
                            }
                        ]
                    }
                ]
            },
            # 3. Education & Tuition
            {
                "name": "Education & Tuition",
                "google_business_category": "Educational Services",
                "sac_code": "999293",
                "subcategories": [
                    {
                        "name": "Academic Tuition",
                        "google_business_category": "Tutoring Service",
                        "sac_code": "999294",
                        "attributes": ["Subjects Handled", "Board (State, CBSE, ICSE, International)", "Teaching Experience"],
                        "listings": [
                            {
                                "title": "Mathematics & Science Tuition",
                                "description": "One-on-one coaching for school and college students.",
                                "plans": [
                                    {"plan_name": "Per Subject Monthly", "description": "20 classes per month", "price": 2500.00, "estimated_duration": "1 Month"},
                                ]
                            }
                        ]
                    }
                ]
            },
            # 4. Entertainment & Media
            {
                "name": "Entertainment & Media",
                "google_business_category": "Entertainment Agency",
                "sac_code": "999619",
                "subcategories": [
                    {
                        "name": "Singer / Vocalist",
                        "google_business_category": "Musician",
                        "sac_code": "999622",
                        "attributes": ["Music Genre", "Performance Languages", "Live / Studio Experience"],
                        "listings": [
                            {
                                "title": "Live Singing Performance for Events",
                                "description": "Professional playback and acoustic singing for weddings, corporate events, and concerts.",
                                "plans": [
                                    {"plan_name": "Event Performance (2 Hours)", "description": "Live singing with basic acoustic setup", "price": 15000.00, "estimated_duration": "2 Hours"},
                                ]
                            }
                        ]
                    }
                ]
            },
            # 5. Industrial & Machinery Services (Groway Solutions Core)
            {
                "name": "Industrial Machinery Maintenance",
                "google_business_category": "Machinery Repair Service",
                "sac_code": "998715",
                "subcategories": [],
                "attributes": ["Machine Brand Compatibility", "PLC & CNC Expertise"],
                "listings": [
                    {
                        "title": "CNC & Cutting Machine Breakdown Service",
                        "description": "On-site mechanical and electrical repair for garment and manufacturing machinery.",
                        "plans": [
                            {"plan_name": "Emergency Breakdown Support", "description": "Immediate troubleshooting and repair", "price": 5000.00, "estimated_duration": "4 Hours"},
                        ]
                    }
                ]
            }
        ]

        # டேட்டாபேஸில் பதிவு செய்யும் லூப்
        for cat_data in global_services_data:
            parent_cat, created = ServiceCategory.objects.get_or_create(
                name=cat_data["name"],
                parent=None,
                defaults={
                    "google_business_category": cat_data["google_business_category"],
                    "sac_code": cat_data["sac_code"],
                    "is_active": True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"மட்டைக் கேட்டகிரி சேர்க்கப்பட்டது: {parent_cat.name}"))

            # Attributes பதிவு செய்தல் (இருந்தால்)
            for attr_title in cat_data.get("attributes", []):
                ServiceAttribute.objects.get_or_create(category=parent_cat, title=attr_title)

            # சப்-கேட்டகிரிகள் (Subcategories)
            for sub_data in cat_data.get("subcategories", []):
                sub_cat, sub_created = ServiceCategory.objects.get_or_create(
                    name=sub_data["name"],
                    parent=parent_cat,
                    defaults={
                        "google_business_category": sub_data["google_business_category"],
                        "sac_code": sub_data["sac_code"],
                        "is_active": True,
                    }
                )
                if sub_created:
                    self.stdout.write(self.style.SUCCESS(f"   -> சப்-கேட்டகிரி சேர்க்கப்பட்டது: {sub_cat.name}"))

                for sub_attr in sub_data.get("attributes", []):
                    ServiceAttribute.objects.get_or_create(category=sub_cat, title=sub_attr)

                # Listings & Plans
                for list_data in sub_data.get("listings", []):
                    listing, _ = ServiceListing.objects.get_or_create(
                        title=list_data["title"],
                        category=sub_cat,
                        defaults={"description": list_data["description"]}
                    )
                    for plan_data in list_data.get("plans", []):
                        ServiceVariationPlan.objects.get_or_create(
                            service=listing,
                            plan_name=plan_data["plan_name"],
                            defaults={
                                "description": plan_data["description"],
                                "price": plan_data["price"],
                                "estimated_duration": plan_data["estimated_duration"],
                            }
                        )

        self.stdout.write(self.style.SUCCESS("அனைத்து உலகளாவிய சேவைக் கேட்டகிரிகளும் வெற்றிகரமாக இம்போர்ட் செய்யப்பட்டன!"))