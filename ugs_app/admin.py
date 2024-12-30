from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from staking_app.models import *
# Register your models here.

class UserAccountLine(admin.StackedInline):
    model=UserAccount
    can_delete=False
    verbose_name_plural='useraccount'
    fk_name='user'

class UserWalletLine(admin.StackedInline):
    model=UserWallet
    can_delete=False
    verbose_name_plural='userwallet'
    fk_name='user'



class CustomUserAccountAdmin(UserAdmin):
    inlines=(UserAccountLine,UserWalletLine)

admin.site.register(Subcription)
admin.site.register(FightHistory)
admin.site.register(UWalletCashout)
admin.site.register(Commission)
admin.site.register(stake_commission)
admin.site.register(Stakefund)
admin.site.register(Points)
admin.site.register(Longestfight)
admin.site.register(Bet)
admin.site.register(Games)
admin.site.register(Fight)
admin.site.register(StakeLogs)
admin.site.register(StakeSlot)
admin.site.register(UserProfile, CustomUserAccountAdmin)
admin.site.register(ConvertRewards)
admin.site.register(Controls)