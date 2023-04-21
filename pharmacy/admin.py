from django.contrib import admin
from .models import Pharmacy, PharmacyImage, PharmaReview
# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(PharmacyImage)
admin.site.register(PharmaReview)