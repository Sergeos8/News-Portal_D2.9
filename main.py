from django.db import models
#
# class Order(models.Model):
#     pass
#
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.FloatField(default=0.0)
#
# class Staff(models.Model):
#     pass
#
# class ProductOrder(models.Model):
#     pass


class Author(models.Model):
    full_name = models.CharField()
    name = models.CharField(null=True)

    def some_method(self):
        self.name = self.full_name.split()[0]
        self.save()


