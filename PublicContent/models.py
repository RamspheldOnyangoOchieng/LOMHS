from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class (e.g., 'bi-hospital')")
    
    def __str__(self):
        return self.title


class Impact(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="FontAwesome/Bootstrap icon class (e.g., 'bi-tree')")
    color = models.CharField(max_length=20, default="primary", help_text="Bootstrap color class (e.g., 'text-success')")

    def __str__(self):
        return self.title

