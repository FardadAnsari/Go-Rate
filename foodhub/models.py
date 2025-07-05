from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class FoodhubModel(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    address = models.CharField(max_length=255)
    apple_pay = models.CharField(max_length=255)
    card_payment = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    cuisines = models.CharField(max_length=255)
    last_update = models.DateTimeField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    new_takeaway = models.CharField(max_length=255)
    payment_provider = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    preorder = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    shop_id_company = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    shop_url_company = models.CharField(max_length=255)
    store_status_collection = models.CharField(max_length=255)
    store_status_delivery = models.CharField(max_length=255)
    store_status_restaurant = models.CharField(max_length=255)
    total_reviews = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        db_table = 'foodhub'

    def __str__(self):
        return f"phone"




class CachedYearlyStats(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = ObjectIdAutoField(primary_key=True)
    data = models.JSONField()  # store the 36-point response as JSON

    # class Meta:
    #     db_table = 'cachedyearlystats'