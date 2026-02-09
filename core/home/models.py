from django.db import models
from django.contrib.auth.models import AbstractUser

class Family(models.Model):
    user = models.ForeignKey("User_a", on_delete=models.CASCADE, related_name="family_members")
    family_name = models.CharField(max_length=100)
    member_name = models.CharField(max_length=100)
    member_age = models.IntegerField(default=18)
    member_gender = models.CharField(max_length=10)
    is_owner = models.BooleanField(default=False)
    joining_id = models.CharField(max_length=6)

    def __str__(self):
        return self.member_name

class User_a(AbstractUser):
    has_joined = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True, related_name="user_accounts")

class Expenses(models.Model):
    expense_name = models.CharField(max_length=100)
    expense_amount = models.IntegerField(default=0)
    expense_date = models.DateField(auto_now_add=True)
    the_id = models.ForeignKey(Family, on_delete=models.CASCADE)
    expenses_by = models.ForeignKey(User_a, on_delete=models.CASCADE)
