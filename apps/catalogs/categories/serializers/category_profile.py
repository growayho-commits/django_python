import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class CategoryProfile(models.Model):
    """
    Global Master Category Tree supporting multi-level parent/child hierarchy.
    Pre-synced global standard categories (No custom manual user creation).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=180, unique=True)
    
    # Self-referencing Foreign Key for Parent-Child Hierarchy (Root -> Sub -> Leaf)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories',
        help_text="Parent category reference for multi-tier tree"
    )
    
    is_global_standard = models.BooleanField(default=True, help_text="Pre-synced global standard category flag")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_category_profile'
        verbose_name = _('Category Profile')
        verbose_name_plural = _('Category Profiles')

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} --> {self.name}"
        return self.name
[cite: 1]