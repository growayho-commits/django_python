# django_python
Hybrid Marketplace


## Architecture Flow Chart

```mermaid
graph TD
    classDef appStyle fill:#f9f,stroke:#333,stroke-width:2px;
    classDef modelStyle fill:#bbf,stroke:#333,stroke-width:1px;
    finances -->|depends on| marketing_leads
    marketing_leads -->|depends on| catalogs
    systems -->|depends on| marketing_leads
    systems -->|depends on| catalogs
    users -->|depends on| catalogs
    users -->|depends on| marketing_leads
    catalogs --- AttributeProfile[Model: AttributeProfile]
    catalogs --- BundleKitProfile[Model: BundleKitProfile]
    catalogs --- CatalogMediaProfile[Model: CatalogMediaProfile]
    catalogs --- CatalogStatusProfile[Model: CatalogStatusProfile]
    catalogs --- CatalogWishlistProfile[Model: CatalogWishlistProfile]
    catalogs --- CategoryProfile[Model: CategoryProfile]
    catalogs --- CoreCatalogProfile[Model: CoreCatalogProfile]
    catalogs --- InventoryProfile[Model: InventoryProfile]
    catalogs --- PricingExtraProfile[Model: PricingExtraProfile]
    catalogs --- PricingTierProfile[Model: PricingTierProfile]
    catalogs --- ReviewRatingProfile[Model: ReviewRatingProfile]
    catalogs --- SearchFilterProfile[Model: SearchFilterProfile]
    catalogs --- SpecificationProfile[Model: SpecificationProfile]
    catalogs --- CatalogVariantProfile[Model: CatalogVariantProfile]
    customer_supports --- FAQProfile[Model: FAQProfile]
    customer_supports --- HelpdeskTicket[Model: HelpdeskTicket]
    customer_supports --- ReturnRefundProfile[Model: ReturnRefundProfile]
    finances --- BankAccountProfile[Model: BankAccountProfile]
    finances --- CommissionProfile[Model: CommissionProfile]
    finances --- PaymentGatewayConfig[Model: PaymentGatewayConfig]
    finances --- PayoutProfile[Model: PayoutProfile]
    finances --- TaxProfile[Model: TaxProfile]
    logistics --- LogisticsPartnerProfile[Model: LogisticsPartnerProfile]
    logistics --- LogisticsReturnProfile[Model: LogisticsReturnProfile]
    logistics --- ShipmentProfile[Model: ShipmentProfile]
    logistics --- WarehouseTransferProfile[Model: WarehouseTransferProfile]
    marketing_leads --- AdsCampaignProfile[Model: AdsCampaignProfile]
    marketing_leads --- CartProfile[Model: CartProfile]
    marketing_leads --- CartItem[Model: CartItem]
    marketing_leads --- CheckoutProfile[Model: CheckoutProfile]
    marketing_leads --- CouponDiscountProfile[Model: CouponDiscountProfile]
    marketing_leads --- CustomerLeadProfile[Model: CustomerLeadProfile]
    marketing_leads --- OrderProfile[Model: OrderProfile]
    marketing_leads --- OrderItem[Model: OrderItem]
    marketing_leads --- PushNotificationProfile[Model: PushNotificationProfile]
    marketing_leads --- Wishlist[Model: Wishlist]
    professional_network --- SkillEnquiry[Model: SkillEnquiry]
    professional_network --- ProfessionalProfile[Model: ProfessionalProfile]
    professional_network --- ServiceRequest[Model: ServiceRequest]
    professional_network --- ProviderAvailability[Model: ProviderAvailability]
    professional_network --- ProfessionalProfile[Model: ProfessionalProfile]
    professional_network --- ProfessionalMedia[Model: ProfessionalMedia]
    professional_network --- ProfessionalStory[Model: ProfessionalStory]
    professional_network --- ProfessionalEvent[Model: ProfessionalEvent]
    professional_network --- SkillRating[Model: SkillRating]
    professional_network --- SearchLog[Model: SearchLog]
    professional_network --- ServiceCategory[Model: ServiceCategory]
    professional_network --- ServiceAttribute[Model: ServiceAttribute]
    professional_network --- ServiceListing[Model: ServiceListing]
    professional_network --- ServiceVariationPlan[Model: ServiceVariationPlan]
    systems --- AnalyticsProfile[Model: AnalyticsProfile]
    systems --- AuditLogProfile[Model: AuditLogProfile]
    systems --- IntegrationProfile[Model: IntegrationProfile]
    users --- ExecutiveProfile[Model: ExecutiveProfile]
    users --- MemberProfile[Model: MemberProfile]
    users --- MerchantProfile[Model: MerchantProfile]
    users --- SellerProfile[Model: SellerProfile]
    users --- UserAddress[Model: UserAddress]
    users --- BusinessProfile[Model: BusinessProfile]
    users --- IndividualProfile[Model: IndividualProfile]
    users --- InternalMail[Model: InternalMail]
    users --- RoleUpgradeRequest[Model: RoleUpgradeRequest]
    users --- SuperuserProfile[Model: SuperuserProfile]
```
