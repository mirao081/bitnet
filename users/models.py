from django.db import models
from django.contrib.auth.models import User


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} Balance"
    
    
class ActiveInvestment(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"
    

class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    referrer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals"
    )

    def __str__(self):
        return f"{self.user.username} Referrals"

class Deposit(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Deposit {self.amount} - {self.status}"
    

class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Withdrawal {self.amount} - {self.status}"
    


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Not Verified'}"
    
class UserKYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'KYC Pending'),
        ('approved', 'KYC Approved'),
        ('rejected', 'KYC Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    document = models.FileField(upload_to='kyc_documents/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"
    

class Notification(models.Model):
    TYPE_CHOICES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("admin", "Admin"),
        ("promotion", "Promotion"),
        ("signup", "Signup"),
        ("verification", "Verification"),
        ("investment", "Investment"),
        ("referral", "Referral"),
        ("bonus", "Bonus"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.message[:30]}"