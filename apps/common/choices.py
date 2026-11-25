from django.db import models


class CoverageScopeChoices(models.TextChoices):
    PINCODE = 'pincode', 'Specific Pincode(s)'
    TALUK = 'taluk', 'Taluk Based'
    DISTRICT = 'district', 'Single District'
    MULTI_DISTRICT = 'multi_district', 'Multiple Districts'
    STATE = 'state', 'Single State'
    MULTI_STATE = 'multi_state', 'Multiple States'
    ALL_INDIA = 'all_india', 'All Over India'
    ONLINE = 'online', 'Online / Remote Service'