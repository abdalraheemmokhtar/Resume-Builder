# resume_app/models.py
from django.db import models

class CV(models.Model):
    content = models.TextField()
    desired_role = models.TextField()
    # Add any additional fields as needed

    def __str__(self):
        return f"CV #{self.id}"

