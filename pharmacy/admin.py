from django.contrib import admin
from .models import Pharmacy, PharmaReview, PharmacyUser
# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(PharmaReview)
admin.site.register(PharmacyUser)