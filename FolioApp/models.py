from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Payment(models.Model):
    order_id = models.CharField(max_length=255)
    payer_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
