from django.db import models

class UserRole(models.TextChoices):
    SUPERUSER = 'SUPERUSER', 'Superuser'
    EXECUTIVE = 'EXECUTIVE', 'Executive'
    MERCHANT = 'MERCHANT', 'Merchant'
    SELLER = 'SELLER', 'Seller'
    MEMBER = 'MEMBER', 'Member'

class ApprovalStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Approval'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    APPROVED = 'APPROVED', 'Accepted / Approved'
    REJECTED = 'REJECTED', 'Rejected'
    RESUBMIT = 'RESUBMIT', 'Reconsideration / Resubmit'