from django.db import models 

EmploymentType = [
    ("Full Time","Full Time"),
     ("Part Time", "Part Time"),
         ("Contract", "Contract")


]
LocationTypeChoice = [
    ("Onsite","Onsite"),
    ("Hybrid", "Hybrid"),
    ("Remote", "Remote"),
]
ExperienceLevel = [
    ("Entry Level", "Entry Level"),
    ("Mid Level", "Mid Level"),
    ("Senior", "Senior"),
]

class PaymentStatus(models.TextChoices):
        PENDING = ("PENDING", "Pending")
        PAID = ("PAID", "Paid")
        FAILED = ("FAILED", "Failed")


class ApplicationStatus(models.TextChoices):
    APPLIED = ("APPLIED","APPLIED")
    REJECTED = ("REJECTED","REJECTED")
    INTERVIEW = ("INTERVIEW","INTERVIEW")
    