from django import forms
import django.forms.utils
import django.forms.widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserAccount,UserWallet,Games,UserProfile,Fight,Points
from django.contrib.auth.password_validation import validate_password
from django.core import validators



class LoginForm(forms.Form):
    
    username=forms.CharField(label="Username",max_length=50, widget=forms.TextInput(attrs={'autocomplete':'off','placeholder':'Username','class':'form-control inputclass mb-4 input-lg'}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control inputclass mb-4 input-lg '}))
   

class SignUpForm(forms.ModelForm):
    first_name=forms.CharField(label='First Name',max_length=50, widget=forms.TextInput(attrs={'placeholder':'Firstname','class':'form-control inputclass '}))
    last_name=forms.CharField(label='Last Name',max_length=50, widget=forms.TextInput(attrs={'placeholder':'LastName','class':'form-control inputclass'}))
    contact_no=forms.IntegerField(label='Contact', widget=forms.NumberInput(attrs={'minlength':'10','placeholder':'Mobile Number','class':'form-control inputclass'}))
    username=forms.CharField(label='Username',max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control inputclass'}))
    password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control inputclass pass1'}))
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':' Confirmation','class':'form-control inputclass pass2'}))
    # coutstat=forms.IntegerField(label='Stat', widget=forms.NumberInput(attrs={'minlength':'10','placeholder':'Mobile Number','class':'form-control inputclass'}))
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','contact_no','username', 'password')

GENDER=(
    ('','SELECT GENDER'),
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
)
USERTYPE=(
    ('','-------'),
    ('ADMIN','ADMIN'),
    ('DECLARATOR','DECLARATOR'),
    ('MASTER OPERATOR','MASTER OPERATOR'),
    ('INCORPORATOR','INCORPORATOR'),
    ('SUB ADMIN','SUB ADMIN'),
    ('SUB OPERATOR','SUB OPERATOR'),
    ('MASTER AGENT','MASTER AGENT'),
    ('PLAYER','PLAYER'),
)

WALLET_STATUS=(
    ('ACTIVE','ACTIVE'),
    ('ONHOLD','ONHOLD'),
    ('BANNED','BANNED'),
)
GAMES=(
    ('E-SABONG','E-SABONG'),
    ('E-SPORTS','E-SPORTS'),
    ('E-PERYA','E-PERYA'),
    ('E-MOVIES','E-MOVIES'),
)

class UserForm(ModelForm):
    contact_no=forms.IntegerField(label='Contact', widget=forms.NumberInput(attrs={'minlength':'10','placeholder':'Mobile Number','class':'form-control inputclass'}))
    usertype=forms.ChoiceField(label='Account Type',widget=forms.Select(attrs={'class':'form-control inputclass bg-dark'}), choices=USERTYPE)
    class Meta:
        model = UserAccount
        fields=('usertype',)

class WalletForm(ModelForm):
    w_balance=forms.IntegerField(label='Balance', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_points=forms.IntegerField(label='Points', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_commission=forms.IntegerField(label='Commission', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_status=forms.ChoiceField(label='Status',widget=forms.Select(attrs={'class':'form-control inputclass'}), choices=WALLET_STATUS)
    class Meta:
        model = UserWallet
        fields=('w_balance','w_points','w_commission',)


class GameForm(ModelForm):
    
    g_name=forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder':'Title','class':'form-control inputclass'}))
    g_redname=forms.CharField(label='Meron Name', widget=forms.TextInput(attrs={'placeholder':'Red Side','class':'form-control inputclass'}))
    g_bluename=forms.CharField(label='Wala Name', widget=forms.TextInput(attrs={'placeholder':'Blue Side','class':'form-control inputclass'}))
    g_plasada=forms.DecimalField(label='Plasada',widget=forms.NumberInput(attrs={'placeholder':'Plasada','class':'form-control inputclass'}))
    g_desc=forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows':'5','class':'form-control inputclass'}))
    g_category=forms.ChoiceField(label='Category',widget=forms.Select(attrs={'class':'form-control inputclass'}), choices=GAMES)
    g_image=forms.FileField(label='Event Image', widget=forms.FileInput(attrs={'class':'form-control inputclass'}))
    g_link=forms.CharField(label='Game Url', widget=forms.TextInput(attrs={'placeholder':'Url','class':'form-control inputclass'}))
    
    class Meta:
        model = Games
        fields=('g_name','g_redname','g_bluename','g_plasada','g_desc','g_category','g_link','g_image')

class FightForm(ModelForm):
    class Meta:
        model = Fight
        fields = "__all__"


class LoadPointsForm(forms.ModelForm):
    class Meta:
        model = Points
        fields = ['p_receiver', 'p_amount']  # Assuming you want to show owner selection

    p_receiver = forms.ModelChoiceField(
        queryset=UserAccount.objects.all(),
        label='Agent',
        to_field_name='user',
        widget=forms.Select(attrs={'id': 'agentid','class': 'form-control text-white inputclass '})
    )
    p_amount = forms.IntegerField(
        label='Amount',
        widget=forms.NumberInput(attrs={'id': 'loadAmountField','maxlength': '2', 'placeholder': 'Points Amount', 'class': 'form-control inputclass ','min':'1','step':'any'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(LoadPointsForm, self).__init__(*args, **kwargs)
   

        if user is not None:
            # Filter the queryset to only show instances related to the logged-in user
            self.fields['p_receiver'].queryset = UserAccount.objects.filter(user_agent=user)

# class LoadPointsForm(forms.ModelForm):
#     user_agent = forms.ModelChoiceField(
#         queryset=UserAccount.objects.exclude(usertype='ADMIN').exclude(usertype='DECLARATOR'),
#         label='Agent',
#         to_field_name='user',
#         widget=forms.Select(attrs={'id': 'agentid','class': 'form-control text-white inputclass '})
#     )
 
#     load_amount = forms.IntegerField(
#         label='Amount',
#         widget=forms.NumberInput(attrs={'id': 'loadAmountField','maxlength': '2', 'placeholder': 'Points Amount', 'class': 'form-control inputclass ','min':'1','step':'any'})
#     )
    
       

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['user_agent'].label_from_instance = self.label_from_user_account

#     def label_from_user_account(self, user_account):
#         return f'{user_account.user.username} - {user_account.user.first_name}'

#     class Meta:
#         model = Points
#         fields = ('user_agent', 'load_amount')







class SendPoint(forms.ModelForm):
    user_agent = forms.ModelChoiceField(
        queryset=UserAccount.objects.exclude(usertype='ADMIN').exclude(usertype='DECLARATOR'),
        label='Agent',
        to_field_name='user',
        widget=forms.Select(attrs={'id': 'playerids','class': 'form-control text-white inputclass '})
    )
    load_amount = forms.IntegerField(
        label='Amount',
        widget=forms.NumberInput(attrs={'id': 'loadAmount','maxlength': '2', 'placeholder': 'Points Amount', 'class': 'form-control inputclass ','min':'1','step':'any'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_agent'].label_from_instance = self.label_from_user_account

    def label_from_user_account(self, user_account):
        return f'{user_account.user.username} - {user_account.user.first_name}'

    class Meta:
        model = Points
        fields = ('user_agent', 'load_amount')
