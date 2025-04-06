from django.db import models
from django.utils import timezone

# models
class User(models.Model):
    user_id = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField("date created", null=False, default=timezone.now)

class EngineType(models.Model):
    type = models.CharField(max_length=100, null=False)

class Engine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    engine_type = models.ForeignKey(EngineType, on_delete=models.SET_NULL, null=True)
    engine_identification = models.CharField(max_length=100, null=False, unique=False)
    rated_thrust = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    bp_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    pressure_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField("date created", null=False, default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'engine_identification'], 
                name='unique_user_engine_identification'
            )
        ]
