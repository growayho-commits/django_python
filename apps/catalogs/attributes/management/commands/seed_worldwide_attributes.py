from django.core.management.base import BaseCommand
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

WORLDWIDE_ATTRIBUTES = [
    # Variation Axes (GS1 / Amazon / Shopify Standard)
    {"name": "Size", "code": "size", "data_type": "string", "input_type": "select", "options": ["XS", "S", "M", "L", "XL", "XXL", "3XL", "Free Size"], "unit": "", "is_variant_axis": True},
    {"name": "Color", "code": "color", "data_type": "string", "input_type": "color", "options": ["Black", "White", "Red", "Blue", "Navy", "Green", "Yellow", "Grey", "Brown", "Multicolor"], "unit": "", "is_variant_axis": True},
    {"name": "Weight / Net Quantity", "code": "weight", "data_type": "string", "input_type": "select", "options": ["100g", "250g", "500g", "1kg", "5kg", "10kg", "25kg", "50kg"], "unit": "kg/g", "is_variant_axis": True},
    {"name": "Volume / Capacity", "code": "volume", "data_type": "string", "input_type": "select", "options": ["100ml", "250ml", "500ml", "1L", "5L", "20L"], "unit": "ml/L", "is_variant_axis": True},
    {"name": "Pack Size / Case Pack", "code": "pack-size", "data_type": "string", "input_type": "select", "options": ["1 Pc", "Pack of 2", "Pack of 6", "Pack of 12", "Box of 24", "Carton of 100"], "unit": "pcs", "is_variant_axis": True},
    {"name": "Storage Capacity", "code": "storage-capacity", "data_type": "string", "input_type": "select", "options": ["32GB", "64GB", "128GB", "256GB", "512GB", "1TB", "2TB"], "unit": "GB/TB", "is_variant_axis": True},
    {"name": "RAM / Memory", "code": "ram-memory", "data_type": "string", "input_type": "select", "options": ["4GB", "8GB", "16GB", "32GB", "64GB"], "unit": "GB", "is_variant_axis": True},
    {"name": "Power / Wattage", "code": "wattage", "data_type": "string", "input_type": "select", "options": ["10W", "50W", "100W", "500W", "1000W", "2000W"], "unit": "W", "is_variant_axis": True},
    {"name": "Voltage", "code": "voltage", "data_type": "string", "input_type": "select", "options": ["110V", "220V", "240V", "415V (3-Phase)"], "unit": "V", "is_variant_axis": True},
    # Global Technical & Compliance Attributes
    {"name": "Brand", "code": "brand", "data_type": "string", "input_type": "string", "options": [], "unit": "", "is_variant_axis": False},
    {"name": "Material / Fabric", "code": "material", "data_type": "string", "input_type": "select", "options": ["Cotton", "Polyester", "Stainless Steel", "Mild Steel", "Plastic (ABS)", "Wood", "Glass", "Leather", "Ceramic", "Aluminum"], "unit": "", "is_variant_axis": False},
    {"name": "Country of Origin", "code": "country-of-origin", "data_type": "string", "input_type": "select", "options": ["India", "China", "USA", "Germany", "Japan", "South Korea", "Taiwan", "Vietnam"], "unit": "", "is_variant_axis": False},
    {"name": "Warranty Period", "code": "warranty", "data_type": "string", "input_type": "select", "options": ["No Warranty", "3 Months", "6 Months", "1 Year", "2 Years", "3 Years", "5 Years"], "unit": "", "is_variant_axis": False},
    {"name": "Quality Certification", "code": "certification", "data_type": "string", "input_type": "select", "options": ["ISO 9001", "BIS / ISI", "FSSAI", "CE", "RoHS", "GMP", "Organic Certified"], "unit": "", "is_variant_axis": False},
    {"name": "Model / Part Number", "code": "model-number", "data_type": "string", "input_type": "string", "options": [], "unit": "", "is_variant_axis": False},
    {"name": "Shelf Life", "code": "shelf-life", "data_type": "string", "input_type": "string", "options": [], "unit": "months", "is_variant_axis": False},
    {"name": "Dimensions (L x W x H)", "code": "dimensions", "data_type": "string", "input_type": "string", "options": [], "unit": "cm", "is_variant_axis": False},
    {"name": "Finish / Texture", "code": "finish", "data_type": "string", "input_type": "select", "options": ["Matte", "Glossy", "Brushed", "Powder Coated", "Polished"], "unit": "", "is_variant_axis": False},
]


class Command(BaseCommand):
    help = "Seed worldwide GS1/Amazon/Shopify standard attributes and variation axes."

    def handle(self, *args, **options):
        created, updated = 0, 0
        for item in WORLDWIDE_ATTRIBUTES:
            _, is_created = AttributeProfile.objects.update_or_create(
                code=item["code"],
                defaults=item,
            )
            if is_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Worldwide attributes ready -> Created: {created}, Updated: {updated}"))
