from django.db import models
from ugs_app.models import *
from django.db import models
from django.db.models.deletion import RESTRICT,CASCADE
from django.contrib.auth.models import User,AbstractUser
import uuid
import datetime
from django.utils import timezone
from django.utils.translation import gettext as _
now= timezone.now
from django.conf import settings
now= timezone.now


class StakeSlot(models.Model):
    sl_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sl_code = models.CharField(blank=True, max_length=50, null=True)
    sl_name=models.CharField(default=0,max_length=50, blank=True)
    sl_rate=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sl_amount=models.IntegerField(default=0, blank=True)
    sl_total=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sl_daily = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sl_earnings=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sl_type=models.CharField(default=0,max_length=50, blank=True)
    sl_status=models.CharField(max_length=50,default='PENDING',choices=[('PENDING','PENDING'),('ACTIVE','ACTIVE'),('CLAIMED','CLAIMED')])
    sl_duration=models.IntegerField(default=0, blank=True)
    sl_daysactive=models.IntegerField(default=0, blank=True)
    sl_date=models.DateTimeField(auto_now=True)
    sl_claimed=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sl_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.user.username +' - [ '+str(self.sl_date)+' - [ '+str(self.sl_code)+' ] - [ '+str(self.sl_name)+' ] - [ '+str(self.sl_amount)+' ] - [ '+str(self.sl_total)+' ] - [ '+str(self.sl_daily)+' ] - [ '+str(self.sl_earnings)+' ] - [ '+str(self.sl_status))






class StakeLogs(models.Model):
    stk_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stk_code = models.CharField(blank=True, max_length=50, null=True)
    stk_name=models.CharField(default=0,max_length=50, blank=True)
    stk_earnings=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stk_type=models.CharField(default=0,max_length=50, blank=True)
    stk_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username +' - [ '+str(self.st_code)+' - [ '+str(self.st_name)+' ] - [ '+str(self.st_earnings)+' ] - [ '+str(self.st_type)+' ] - [ '+str(self.st_date))
    

    

    
class stake_commission(models.Model):
    sc_id = models.AutoField(primary_key=True)
    sc_code = models.CharField(max_length=50, default=0)
    sc_player = models.CharField(max_length=100, default='')
    sc_agent = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sc_level = models.CharField(max_length=50, default=0)
    sc_percent = models.CharField(max_length=50, default=0)
    sc_type = models.CharField(max_length=50, default=0)
    sc_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sc_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    screated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sc_code} -- [ {self.screated} ] - [    ] - [  {self.sc_level} ] - [ {self.sc_percent} ] - [ {self.sc_amount} ] - [ {self.sc_commission} ]"
    





class Stake_withdrawal(models.Model):
    sw_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sw_code = models.CharField(blank=True, max_length=50, null=True)
    sw_mop = models.CharField(blank=True, max_length=50, null=True)
    sw_ac_name = models.CharField(blank=True, max_length=50, null=True)
    sw_ac_number = models.CharField(blank=True, max_length=50, null=True)
    sw_available=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sw_withdraw=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sw_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sw_date=models.DateTimeField(auto_now=True)
    sw_status=models.CharField(max_length=50,default='PENDING',choices=[('PENDING','PENDING'),('APPROVED','APPROVED')])
    sw_confirmed = models.CharField(blank=True, max_length=50, null=True)
    sw_dateconfirm=models.CharField(blank=True, max_length=50, null=True)

    def __str__(self):
        return str(self.user.username +' - [ '+str(self.sw_available)+' - [ '+str(self.sw_withdraw)+' ] - [ '+str(self.sw_balance)+' ] - [ '+str(self.sw_date))
    


class Stake_claimed_comms(models.Model):
    sr_id=models.AutoField(primary_key=True)
    sr_code = models.CharField(blank=True, max_length=50, null=True)
    sr_mop = models.CharField(blank=True, max_length=50, null=True)
    sr_ac_name = models.CharField(blank=True, max_length=50, null=True)
    sr_ac_number = models.CharField(blank=True, max_length=50, null=True)
    sr_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sr_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sr_user = models.ForeignKey(UserProfile, related_name='sr_user', on_delete=models.CASCADE)
    sr_date=models.DateTimeField(auto_now=True)
    sr_status = models.IntegerField(default=0)
    sr_confirmed = models.CharField(blank=True, max_length=50, null=True)
    sr_dateconfirm=models.CharField(blank=True, max_length=50, null=True)

    def __str__(self):
        return f"convertid {self.sr_id} - User: {self.sr_user} - Amount: {self.sr_amount}  - Date: {self.sr_date}"