from django.urls import path
from .views.core_catalog_views import CoreCatalogListCreateAPIView
from .views.catalogue_portal_views import (
    add_to_cart_session_view,
    approve_catalogue_view,
    catalogue_detail_view,
    catalogue_marketplace_view,
    catalogue_workspace_view,
    configure_catalogue_pricing_view,
    manage_bundles_view,
    manage_catalogue_details_view,
    manage_categories_view,
    my_wishlist_view,
    submit_catalogue_review_view,
    toggle_wishlist_view,
)

app_name = 'core_catalogs'

urlpatterns = [
    path('core-catalog-list-create-a-p-i/', CoreCatalogListCreateAPIView.as_view(), name='core_catalog_list_create_a_p_i'),
    path('workspace/', catalogue_workspace_view, name='catalogue_workspace'),
    path('manage-details/<int:pk>/', manage_catalogue_details_view, name='manage_catalogue_details'),
    path('categories/', manage_categories_view, name='manage_categories'),
    path('bundles/', manage_bundles_view, name='manage_bundles'),
    path('wishlist/', my_wishlist_view, name='my_wishlist'),
    path('configure-pricing/<int:pk>/', configure_catalogue_pricing_view, name='configure_catalogue_pricing'),
    path('approve/<int:pk>/', approve_catalogue_view, name='approve_catalogue'),
    path('marketplace/', catalogue_marketplace_view, name='catalogue_marketplace'),
    path('marketplace/<int:pk>/', catalogue_detail_view, name='catalogue_detail'),
    path('wishlist/toggle/<int:pk>/', toggle_wishlist_view, name='toggle_wishlist'),
    path('review/submit/<int:pk>/', submit_catalogue_review_view, name='submit_catalogue_review'),
    path('cart/add/<int:pk>/', add_to_cart_session_view, name='add_to_cart_session'),
]