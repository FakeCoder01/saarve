from django.contrib import admin
from .models import Pharmacy, PharmacyImage, PharmaReview, PharmacyUser
# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(PharmacyImage)
admin.site.register(PharmaReview)
admin.site.register(PharmacyUser)