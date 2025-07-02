from django.db import models


class JustEat(models.Model):
    last_update = models.DateTimeField()
    shop_id_company = models.CharField(max_length=20, unique=True)
    shop_url_company = models.CharField(max_length=200)
    shop_name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    total_reviews = models.CharField(max_length=100, null=True, blank=True)
    cuisines = models.CharField(max_length=255, null=True, blank=True)
    openingTimeLocal = models.DateTimeField(null=True, blank=True)
    deliveryOpeningTimeLocal = models.DateTimeField(null=True, blank=True)
    isCollection = models.CharField(max_length=255)
    isDelivery = models.CharField(max_length=255)
    isOpenNowForCollection =models.CharField(max_length=255)
    isOpenNowForDelivery =models.CharField(max_length=255)
    isOpenNowForPreorder = models.CharField(max_length=255)
    isTemporarilyOffline = models.CharField(max_length=255)
    isTemporaryBoost = models.CharField(max_length=255)
    isPremier = models.CharField(max_length=255)
    isNew = models.CharField(max_length=255)
    isTestRestaurant = models.CharField(max_length=255)

    class Meta:
        db_table = 'justeat'

    def __str__(self):
        return f"JustEat"