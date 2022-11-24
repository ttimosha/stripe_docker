from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Item(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    
    def __str__(self):
        return self.name

class Tax(models.Model):
    
    class TaxCode(models.TextChoices):
        TANGIBLE = 'txcd_99999999'
        SERVICES = 'txcd_20030000'
        ESSERVICES = 'txcd_10000000'

    class TaxBehavior(models.TextChoices):
        INCLUSIVE = 'inclusive'
        EXCLUSIVE = 'exclusive'
        UNSPECIFIED = 'unspecified'

    code = models.CharField(
        max_length = 20,
        choices = TaxCode.choices,
        null=True)

    tax_behavior = models.CharField(
        max_length = 20, 
        choices = TaxBehavior.choices, 
        default = TaxBehavior.UNSPECIFIED)

    def __str__(self):
        return f'{self.code}, {self.tax_behavior}'

class Discount(models.Model):
    percent_off = models.IntegerField(validators = [MaxValueValidator(99), MinValueValidator(1)], unique=True)
    duration = models.CharField(max_length=4, default='once', editable=False)

    def __str__(self):
        return f'{self.percent_off} %'

class Order(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(Item, through='ItemOrder', null = True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.session_key

class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


