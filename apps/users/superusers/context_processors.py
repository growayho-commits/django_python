def enterprise_navigation_context(request):
    """
    Professional dynamic context processor mapping all enterprise modules 
    and sub-apps in strict alphabetical order without numeric prefixes,
    fully wired with redirect paths for base.html and dashboard.html.
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        return {}

    enterprise_modules = [
        {
            'id': 'subCatalogs',
            'name': 'Catalogs & Products',
            'short_name': 'Catalogs',
            'icon': 'fa-boxes-stacked',
            'color': 'indigo',
            'badge': '13 Sub-Apps',
            'status': 'Synced',
            'description': 'Attributes, Inventories & Master Catalogs',
            'main_url': '/api/v1/catalogs/',
            'sub_apps': sorted([
                {'title': 'Attributes', 'url': '/api/v1/catalogs/attributes/'},
                {'title': 'Bundles & Kits', 'url': '/api/v1/catalogs/bundles/'},
                {'title': 'Catalog Medias', 'url': '/api/v1/catalogs/media/'},
                {'title': 'Catalog Statuses', 'url': '/api/v1/catalogs/status/'},
                {'title': 'Catalog Wishlist', 'url': '/api/v1/catalogs/wishlist/'},
                {'title': 'Categories', 'url': '/api/v1/catalogs/categories/'},
                {'title': 'Core Catalogs', 'url': '/api/v1/catalogs/core/'},
                {'title': 'Inventories', 'url': '/api/v1/catalogs/inventory/'},
                {'title': 'Pricing Tiers', 'url': '/api/v1/catalogs/pricing/'},
                {'title': 'Reviews & Ratings', 'url': '/api/v1/catalogs/reviews/'},
                {'title': 'Search Filters', 'url': '/api/v1/catalogs/search-filters/'},
                {'title': 'Specifications', 'url': '/api/v1/catalogs/specifications/'},
                {'title': 'Variants', 'url': '/api/v1/catalogs/variants/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subSupport',
            'name': 'Customer Support',
            'short_name': 'Support',
            'icon': 'fa-headset',
            'color': 'sky',
            'badge': 'Help Desk',
            'status': 'Active',
            'description': 'FAQs, Tickets, Live Chats & Refund Complaints',
            'main_url': '/api/v1/support/',
            'sub_apps': sorted([
                {'title': 'FAQs', 'url': '/api/v1/support/'},
                {'title': 'Helpdesk Tickets', 'url': '/api/v1/support/'},
                {'title': 'Live Chats', 'url': '/api/v1/support/'},
                {'title': 'Refunds & Complaints', 'url': '/api/v1/support/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subFinances',
            'name': 'Finances & Banking',
            'short_name': 'Finances',
            'icon': 'fa-wallet',
            'color': 'emerald',
            'badge': 'Gateways',
            'status': 'Secured',
            'description': 'Accounts, Taxes, Commissions & Payouts',
            'main_url': '/api/v1/finances/',
            'sub_apps': sorted([
                {'title': 'Bank Accounts', 'url': '/api/v1/finances/'},
                {'title': 'Commissions', 'url': '/api/v1/finances/'},
                {'title': 'Payment Gateways', 'url': '/api/v1/finances/'},
                {'title': 'Payouts', 'url': '/api/v1/finances/'},
                {'title': 'Taxes', 'url': '/api/v1/finances/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subLogistics',
            'name': 'Logistics & Supply',
            'short_name': 'Logistics',
            'icon': 'fa-truck-fast',
            'color': 'purple',
            'badge': 'Tracking',
            'status': 'Live',
            'description': 'Partners, Shipments & Warehouse Transfers',
            'main_url': '/api/v1/logistics/',
            'sub_apps': sorted([
                {'title': 'Logistics Partners', 'url': '/api/v1/logistics/'},
                {'title': 'Returns & Tracking', 'url': '/api/v1/logistics/'},
                {'title': 'Shipments', 'url': '/api/v1/logistics/'},
                {'title': 'Warehouse Transfers', 'url': '/api/v1/logistics/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subMarketing',
            'name': 'Marketing & Leads',
            'short_name': 'Marketing',
            'icon': 'fa-bullhorn',
            'color': 'amber',
            'badge': 'Campaigns',
            'status': 'Running',
            'description': 'Ad Campaigns, Coupons, Orders & Leads',
            'main_url': '/api/v1/marketing/',
            'sub_apps': sorted([
                {'title': 'Ad Campaigns', 'url': '/api/v1/marketing/'},
                {'title': 'Carts', 'url': '/api/v1/marketing/carts/'},
                {'title': 'Checkout Flows', 'url': '/api/v1/marketing/checkout/'},
                {'title': 'Coupons & Discounts', 'url': '/api/v1/marketing/coupons/'},
                {'title': 'Customer Leads', 'url': '/api/v1/marketing/'},
                {'title': 'Orders', 'url': '/api/v1/marketing/orders/'},
                {'title': 'Push Notifications', 'url': '/api/v1/marketing/notifications/'},
                {'title': 'Wishlists', 'url': '/api/v1/marketing/wishlist/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subProfessional',
            'name': 'Professional Network',
            'short_name': 'Professionals',
            'icon': 'fa-user-tie',
            'color': 'blue',
            'badge': '5 Sub-Apps',
            'status': 'Active',
            'description': 'Service Categories, Profiles, Enquiries & Search',
            'main_url': '/api/v1/professional-network/',
            'sub_apps': sorted([
                {'title': 'Directory Search Engine', 'url': '/api/v1/professional-network/'},
                {'title': 'Professional Profiles', 'url': '/api/v1/professional-network/'},
                {'title': 'Ratings & Reviews', 'url': '/api/v1/professional-network/'},
                {'title': 'Service Categories', 'url': '/api/v1/professional-network/'},
                {'title': 'Skill Enquiries Inbox', 'url': '/api/v1/professional-network/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subSystems',
            'name': 'Systems & Analytics',
            'short_name': 'Systems',
            'icon': 'fa-server',
            'color': 'teal',
            'badge': 'Monitoring',
            'status': 'Healthy',
            'description': 'Security Audits, ROI & API Integrations',
            'main_url': '/api/v1/systems/',
            'sub_apps': sorted([
                {'title': 'Analytics & Forecasting', 'url': '/api/v1/systems/'},
                {'title': 'Integrations & AI Tools', 'url': '/api/v1/systems/'},
                {'title': 'Security Audits', 'url': '/api/v1/systems/'},
            ], key=lambda x: x['title'])
        },
        {
            'id': 'subUsers',
            'name': 'Users & Executives',
            'short_name': 'Users',
            'icon': 'fa-users-gear',
            'color': 'rose',
            'badge': 'Full Control',
            'status': 'Restricted',
            'description': 'Executives, Merchants, Sellers & Members',
            'main_url': '/api/v1/users/',
            'sub_apps': sorted([
                {'title': 'Executives Management', 'url': '/api/v1/users/executives/dashboard/'},
                {'title': 'Guests & Auth', 'url': '/api/v1/users/guests/'},
                {'title': 'Members Portal', 'url': '/api/v1/users/members/dashboard/'},
                {'title': 'Merchants Portal', 'url': '/api/v1/users/merchant/dashboard/'},
                {'title': 'Sellers Portal', 'url': '/api/v1/users/sellers/dashboard/'},
                {'title': 'Superusers Dashboard', 'url': '/api/v1/users/superusers/dashboard/'},
            ], key=lambda x: x['title'])
        },
    ]

    # Main modules list sorted alphabetically (A to Z)
    enterprise_modules = sorted(enterprise_modules, key=lambda x: x['name'])

    return {'enterprise_modules': enterprise_modules}