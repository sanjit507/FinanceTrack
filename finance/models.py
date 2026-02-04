from django.db import models

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPE=[
        ('income','Income'),
        ('expense','Expense'),
        
        ]
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    amount=models.FloatField()
    date=models.DateTimeField()
    Transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE)


    def __str__(self):
        return f"{self.title} - {self.amount} - {self.Transaction_type}"    



class Goal(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    target_amount=models.FloatField()
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    deadline=models.DateField()
    def __str__(self):
        return f"{self.name} - {self.target_amount} - {self.deadline}"    














   