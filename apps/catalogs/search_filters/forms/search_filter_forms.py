from django import forms
from apps.catalogs.search_filters.models.search_filter_profile import SearchFilterProfile

class SearchFilterAdminForm(forms.ModelForm):
    class Meta:
        model = SearchFilterProfile
        fields = ['filter_name', 'filter_key', 'filter_type', 'is_active']