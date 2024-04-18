from django.db import models

class Product(models.Model):
    product_type = models.CharField(max_length=100)

class Component(models.Model):
    component_type = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    supplier_address = models.CharField(max_length=100)

class ProductComponent(models.Model):
    product_type = models.CharField(max_length=100)
    component_type = models.CharField(max_length=100)
    quantity = models.IntegerField()

class Order(models.Model):
    order_id = models.IntegerField()
    adress = models.CharField(max_length=100)
    phone_number = models.IntegerField(null = True)
    status = models.CharField(max_length=100)

class ProductInOrder(models.Model):
    order_id = models.IntegerField()
    product_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    
class ComponentQuantity(models.Model):
    component_type = models.CharField(max_length=100)
    now = models.IntegerField()
    supplying = models.IntegerField()
    need = models.IntegerField()
    miss = models.IntegerField()

    def save(self, *args, **kwargs):
        self.miss = max(0, self.need - self.now - self.supplying)
        super().save(*args, **kwargs)