from django.contrib import admin
from .models import (MyUser, BankAccountType, UserBankAccount,
                    RequiredCode, GenerateCode, Profile)

admin.site.register(MyUser)
admin.site.register(Profile)
admin.site.register(BankAccountType)
# admin.site.register(SendEmail)
# admin.site.register(SendNotification)
admin.site.register(UserBankAccount)
# admin.site.register(NextOfKin)
admin.site.register(RequiredCode)
admin.site.register(GenerateCode)
# admin.site.register(LoanAppliction)
