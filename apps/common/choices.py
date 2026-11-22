from django.db import models

class ApprovalStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RECONSIDER = 'RECONSIDER', 'Reconsider'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'