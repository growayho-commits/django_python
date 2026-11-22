from apps.catalogs.specifications.models.specification_profile import SpecificationProfile

def get_specifications_by_unit(unit_name):
    return SpecificationProfile.objects.filter(unit=unit_name)