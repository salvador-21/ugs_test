from django.utils.timezone import localtime
from django.db import models
from django.db.models.deletion import RESTRICT,CASCADE
from django.contrib.auth.models import User,AbstractUser
import uuid
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings

now=timezone.now


class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_joined=models.DateTimeField(default=datetime.now)
    username=models.CharField(max_length=50, unique=True)
    def clean(self):
        self.username = self.username.upper()

    # def save(self):
    #     self.username = self.username.upper()
    #     super().save()
    
    def get_local_start_time(self):
        return localtime(self.date_joined)
    
class UserAccount(models.Model):
    user=models.OneToOneField(UserProfile,on_delete=CASCADE,)
    contact_no=models.CharField(max_length=11,null=True, default='00000000000')
    relpass=models.CharField(max_length=50,null=True, blank=True)
    referral_code=models.CharField(max_length=200,null=True, blank=True)
    referral_link=models.CharField(max_length=200,null=True, blank=True)
    user_agent=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='agent')
    usertype=models.CharField(max_length=50,default='ADMIN', choices=[('SUPER ADMIN','SUPER ADMIN'),('ADMIN','ADMIN'),('DECLARATOR','DECLARATOR'),('MASTER OPERATOR','MASTER OPERATOR'),('INCORPORATOR','INCORPORATOR'),('SUB ADMIN','SUB ADMIN'),('SUB OPERATOR','SUB OPERATOR'),('MASTER AGENT','MASTER AGENT'),('PLAYER','PLAYER')]) 
    status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE'),('BANNED','BANNED')])
    coutstat=models.IntegerField(null=True, blank=True, default=0)
    dummy=models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.user.username+' - '+self.usertype)
        
    def __str__(self):
        return str(self.user.username)

class UserWallet(models.Model):
    user=models.OneToOneField(UserProfile, on_delete=CASCADE)
    w_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    w_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_points=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_betwins=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_betlong=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_commission=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE'),('BANNED','BANNED')])
    w_dateupdate=models.DateTimeField(auto_now=True)
    commission_rate=models.DecimalField(default=0.00,max_digits=5, decimal_places=4)
    default_rate=models.DecimalField(default=0.00,max_digits=5, decimal_places=4)
    wallet_out=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comms_claimed=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stakebal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stakecom = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stake_active = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stake_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stake_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stake_available= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_comms_bal=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_uplinecom=models.DecimalField(max_digits=10, decimal_places=3, default=0.00)

    w_stakecom_claim=models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    w_stakecom_bal=models.DecimalField(max_digits=10, decimal_places=3, default=0.00)

    def __str__(self):
        return str(self.user.username +' - '+str(self.w_id))
    
    


class Games(models.Model):
    g_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    g_name=models.CharField(max_length=50, blank=True)
    g_redname=models.CharField(max_length=50, blank=True)
    g_bluename=models.CharField(max_length=50, blank=True)
    g_plasada=models.DecimalField(default=0.00,max_digits=5, decimal_places=3)
    g_desc=models.CharField(max_length=100, blank=True)
    g_category=models.CharField(null=True,max_length=50,choices=[('E-SABONG','E-SABONG'),('E-SPORTS','E-SPORTS'),('E-PERYA','E-PERYA'),('E-MOVIES','E-MOVIES')])
    g_link=models.CharField(max_length=1000, blank=True)
    g_image=models.ImageField(blank=True, null=True ,upload_to='uploads')
    g_status=models.CharField(default='CLOSED',max_length=50,choices=[('OPEN','OPEN'),('CLOSED','CLOSED')])
    g_by=models.CharField(max_length=100, blank=True)
    g_update=models.DateTimeField(auto_now=True)
    g_created=models.DateTimeField(auto_now_add=True)
    g_col=models.IntegerField(default=1)

    class Meta:
       get_latest_by = ('-g_created',)

    def __str__(self):
        return str(self.g_name )
    
class Subcription(models.Model):
    s_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    s_movie=models.ForeignKey(Games,default=uuid.uuid4,on_delete=CASCADE,related_name='movie')
    s_by=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='subscriber')
    s_date=models.DateTimeField(auto_now_add=True)
    class Meta:
       get_latest_by = ('-s_date',)

    def __str__(self):
        return (str(self.s_movie) +'- Player:'+str(self.s_by)+' ( Date #: '+str(self.s_date))

class MovieWallet(models.Model):
    m_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    m_balance=models.IntegerField(default=0)
    m_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.m_balance))

class MovieWallet_Logs(models.Model):
    ml_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    ml_amount=models.IntegerField(default=0)
    ml_type=models.CharField(null=True,max_length=50,choices=[('SUBSCRIBE','SUBSCRIBE'),('DONATE','DONATE')])
    ml_movie=models.ForeignKey(Games,default=uuid.uuid4,on_delete=CASCADE,related_name='ml_movie')
    ml_player=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='watcher')
    ml_date=models.DateTimeField(auto_now_add=True)

    class Meta:
       get_latest_by = ('-ml_date',)

    def __str__(self):
        return (str(self.ml_movie) +'- Type:'+str(self.ml_type)+' ( Amount #: '+str(self.ml_amount))

class Fight(models.Model):
    f_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    f_code=models.CharField(max_length=10,null=True, blank=True)
    f_number=models.IntegerField(blank=True,null=True)
    f_multiplier=models.DecimalField(default=0.00,max_digits=5, decimal_places=3)
    f_game=models.ForeignKey(Games,on_delete=CASCADE,related_name='game')
    f_winner=models.CharField(max_length=100,null=True, blank=True)
    f_longest=models.IntegerField(default=0)
    f_status=models.CharField(null=True,max_length=50,choices=[('OPEN','OPEN'),('CLOSED','CLOSED'),('CLOSING','CLOSING'),('DONE','DONE'),('LAST CALL','LAST CALL'),('DECLARED','DECLARED')])
    f_update=models.DateTimeField(auto_now=True)
    f_created=models.DateTimeField(auto_now_add=True)
    f_tblrows=models.IntegerField(default=0)
    f_revert = models.CharField(blank=True, max_length=50, null=True)
    f_mpout = models.CharField(max_length=50, default=0)
    f_wpout = models.CharField(max_length=50, default=0)
    f_prevwin= models.CharField(blank=True, max_length=50, null=True)

    class Meta:
        ordering = ['-f_created']
    
    def __str__(self):
        return str(str(self.f_game) +'- Winner:'+str(self.f_winner)+' ( Fight #: '+str(self.f_number)+' ) Status: '+str(self.f_status) )
    
class FightHistory(models.Model):
    f_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    f_code=models.CharField(max_length=10,null=True, blank=True)
    f_number=models.IntegerField(blank=True,null=True)
    f_multiplier=models.DecimalField(default=0.00,max_digits=5, decimal_places=3)
    f_game=models.ForeignKey(Games,on_delete=CASCADE,related_name='fight_history')
    f_winner=models.CharField(max_length=100,null=True, blank=True)
    f_longest=models.IntegerField(default=0)
    f_status=models.CharField(null=True,max_length=50,choices=[('OPEN','OPEN'),('CLOSED','CLOSED'),('CLOSING','CLOSING'),('DONE','DONE'),('LAST CALL','LAST CALL'),('DECLARED','DECLARED')])
    f_update=models.DateTimeField(auto_now=True)
    f_created=models.DateTimeField(auto_now_add=True)
    f_tblrows=models.IntegerField(default=0)

    class Meta:
        ordering = ['-f_created']

    def __str__(self):
        return str(str(self.f_game) +'- Winner:'+str(self.f_winner)+' ( Fight #: '+str(self.f_number)+' ) Status: '+str(self.f_status) )
    


    
class Bet(models.Model):
    id=models.AutoField(primary_key=True)
    player=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='player')
    fight=models.ForeignKey(Fight,default=uuid.uuid4,on_delete=CASCADE,related_name='fight')
    amount=models.IntegerField(blank=True)
    winning_amnt = models.CharField(max_length=50, default=0)
    won_amnt = models.CharField(max_length=100, default=0)
    winStat = models.CharField(max_length=100, default=0)
    category=models.CharField(null=True,max_length=50,choices=[('MERON','MERON'),('WALA','WALA'),('DRAW','DRAW'),('LONGEST','LONGEST')])
    status=models.CharField(default='PENDING',max_length=50,choices=[('PENDING','PENDING'),('WIN','WIN'),('LOSE','LOSE'),('CANCELLED','CANCELLED'),('DRAW','DRAW')])
    created=models.DateTimeField(auto_now_add=True)
    fightno = models.IntegerField(default=0)
    longest = models.IntegerField(default=0)
    event=models.CharField(max_length=100, default='')
    walletbal=models.CharField(max_length=50, default=0)
    waltotal=models.CharField(max_length=50, default=0)
    eventid=models.CharField(max_length=100, default='')
    decimal=models.CharField(max_length=50, default=0)
    result=models.CharField(null=True,max_length=50,choices=[('MERON','MERON'),('WALA','WALA'),('DRAW','DRAW'),('LONGEST','LONGEST')])
   
    def __str__(self):
        return str(str(self.player) + ' - '+ str(self.category)+' - '+str(self.amount)+' - '+str(self.fight) )

    
class Commission(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_fight = models.ForeignKey('Fight', on_delete=models.CASCADE, related_name='commissions')
    c_player = models.CharField(max_length=100)
    c_agent = models.CharField(max_length=100, default='')
    c_fnumber = models.CharField(max_length=50, default=0)
    c_betamnt = models.CharField(max_length=50)
    c_winner = models.CharField(max_length=50)
    c_commission = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    c_event=models.CharField(max_length=101, default='')
    c_eventid=models.CharField(max_length=101, default='')
    c_bet = models.CharField(max_length=50, default='')
    c_level = models.CharField(max_length=50, default=0)
    
    def __str__(self):
        return f"Fight: {self.c_fight}, Player: {self.c_player}, Bet Amount: {self.c_betamnt}, Winner: {self.c_winner}, Commission: {self.c_commission}"
    
    
class Points(models.Model):
    p_id = models.AutoField(primary_key=True, editable=False)
    p_receiver = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='p_userkey')
    p_sender = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='p_headKey')
    p_code = models.CharField(blank=True, max_length=50, null=True)
    p_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    p_created = models.DateTimeField(auto_now=True)
    p_update = models.DateTimeField(auto_now_add=True)
    p_processby = models.CharField(null=True, max_length=100, blank=True)
    p_transtype = models.CharField(null=True, max_length=20, blank=True)
    p_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    p_agentbal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    

    def __str__(self):
        return f'{self.p_code} - {self.p_receiver} - {self.p_sender} -  {self.p_amount} -  {self.p_created}  -  {self.p_transtype}'
    
class UWalletCashout(models.Model):
    cw_id = models.AutoField(primary_key=True)
    cw_code = models.CharField(blank=True, max_length=50, null=True)
    cw_player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cw_player')
    cw_bal = models.DecimalField(max_digits=10, decimal_places=2)
    cw_out = models.DecimalField(max_digits=10, decimal_places=2)
    cw_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    cw_update = models.DateTimeField(auto_now=True)
    cw_created = models.DateTimeField(default=datetime.now)
    cw_agentid = models.CharField(blank=True, max_length=100, null=True)
    cw_stat = models.CharField(max_length=50, default=0)
    cw_approved = models.CharField(blank=True, max_length=100, null=True)
    cw_appdate = models.CharField(blank=True, max_length=20, null=True)
    
    def __str__(self):
        return f"Player: {self.cw_player}, Cashout: {self.cw_out}, Remaining: {self.cw_remaining}"
    

class Longestfight(models.Model):
    id=models.AutoField(primary_key=True)
    l_player=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='l_player')
    l_fight=models.ForeignKey(Fight,default=uuid.uuid4,on_delete=CASCADE,related_name='l_fight')
    l_amount=models.IntegerField(blank=True)
    l_won_amnt = models.CharField(max_length=100, default=0)
    l_category=models.CharField(null=True,max_length=50,choices=[('LONGEST','LONGEST')])
    l_status=models.CharField(default='WAITING',max_length=50,choices=[('WAITING','WAITING'),('CLAIMED','CLAIMED')])
    l_fightno = models.IntegerField(default=0)
    l_created=models.DateTimeField(auto_now_add=True)
    l_event=models.CharField(max_length=100, default='')
    l_walletbal=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    l_waltotal=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    l_eventid=models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Player: {self.l_player}, Cashout: {self.l_won_amnt}, FightNo: {self.l_fightno}, Event: {self.l_event}, WalletBal: {self.l_walletbal}, WalletTotal: {self.l_waltotal}"

class Stakefund(models.Model):
    s_id=models.AutoField(primary_key=True)
    s_code = models.CharField(blank=True, max_length=50, null=True)
    s_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    s_user = models.ForeignKey(UserProfile, related_name='stakefund_user', on_delete=models.CASCADE)
    s_sender = models.ForeignKey(UserProfile, related_name='stakefund_sender', on_delete=models.CASCADE)
    s_date=models.DateTimeField(auto_now_add=True)
    s_status = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.s_user} - from: {self.s_sender}  - Amount: {self.s_amount}"
    

class ConvertRewards(models.Model):
    r_id=models.AutoField(primary_key=True)
    r_code = models.CharField(blank=True, max_length=50, null=True)
    r_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    r_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    r_user = models.ForeignKey(UserProfile, related_name='r_user', on_delete=models.CASCADE)
    r_date=models.DateTimeField(auto_now=True)
    r_status = models.IntegerField(default=0)

    def __str__(self):
        return f"convertid {self.r_id} - User: {self.r_user} - Amount: {self.r_amount}  - Date: {self.r_date}"
    


class Controls(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name = models.CharField(blank=True, max_length=50, null=True)
    c_status = models.IntegerField(default=0)
    c_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"control_id {self.c_id} - control _name: {self.c_name} - control_status: {self.c_status}  - Date: {self.c_date}"
    

    


       