import uuid
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey,MPTTModel
from django.contrib.auth.models import User
import csv
from io import StringIO

class ProductManager(models.Manager):
    def get_queryset(self):
        queryset = super(ProductManager, self).get_queryset()
        queryset = queryset.filter(status="publish")
        return queryset


class Category(MPTTModel,models.Model):
    name = models.CharField(max_length = 150, verbose_name=_("Category Name"),unique=True)
    slug = models.SlugField(max_length = 50, unique_for_date="published")

    published = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name= "children", verbose_name = _("Parent"), blank=True, unique=False,null=True)

    class MPTTMetal:
        order_insersion_by = ["name"]
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("goshop:category_list", args=[self.slug])
    
    


class Brand(models.Model):
    name = models.CharField(max_length = 150, verbose_name=_("Brand Name"), unique=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


    
    
class Product(models.Model):
    STATUS = (
        ("publish", "Publish"),
        ("draft","Draft")
    )
    owner = models.ForeignKey(User, verbose_name=_("Store Owner"), default=User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length = 150, verbose_name=_("Product Name"), unique=False)
    slug = models.SlugField(max_length = 50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name=_("product"), verbose_name=_("Product Category"))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name=_("brand"), verbose_name=_("Product Brand"))
    image = models.ImageField(upload_to="images/", height_field=None, width_field=None, max_length=100, verbose_name=_("Featured Image"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    web_id = models.UUIDField(default=uuid.uuid1, verbose_name=_("Web ID"), editable=False, unique=True)
    description = models.TextField(verbose_name=_("Product Specifications"))
    specification = models.TextField(verbose_name=_("Product Specifications"))

    status = models.CharField(max_length=10,verbose_name=_("Product Status"), default="draft", choices=STATUS)

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    products = ProductManager()
    
    
    class MPTTMetal:
        order_insertion_by = ["updated_on"]

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("goshop:product_details", args=[self.slug])  

class ProductType(models.Model):
    name = models.CharField(max_length = 150, verbose_name=_("Product Type"), unique=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Type")
    

    
   
class SubProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product Parent"))
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name=_("Product Type"))
    sku = models.UUIDField(default=uuid.uuid1, verbose_name=_("Stock Keeping Unit"), editable=False, unique=True)
    upc = models.UUIDField(default=uuid.uuid1, verbose_name=_("Universal Product Code"), editable=False, unique=True)
    image = models.ImageField(upload_to="images/", height_field=None, width_field=None, max_length=100, verbose_name=_("Image"))
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    weight = models.FloatField(verbose_name=_("Product Weight"))

    in_stock = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return ("%s" % (self.product))