from django.db import models

# Create your models here.
class Prop(models.Model):
    name = models.CharField(max_length=255)
    p_type=models.IntegerField()
    start_date=models.CharField(max_length=255)
    term_month=models.IntegerField()
    rate=models.FloatField(default=0.0)
    currency=models.IntegerField(default=0, null=True)
    ctype=models.IntegerField(null=True)
    comment=models.CharField(max_length=255, null=True)
    is_fake=models.IntegerField(default=0)


class Detail(models.Model):
    target_id=models.ForeignKey(Prop, on_delete=models.CASCADE)
    occur_date=models.CharField(max_length=255)
    amount=models.IntegerField()
    comment=models.CharField(max_length=255, null=True)
