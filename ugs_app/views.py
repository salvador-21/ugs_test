from django.http import Http404
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils import timezone
from .models import UserAccount,UserWallet,Games,Bet,Fight,UserProfile,Commission,Points,UWalletCashout,Longestfight,Stakefund,FightHistory,ConvertRewards,Subcription
from staking_app.models import StakeSlot,Stake_claimed_comms
import datetime,time
import uuid
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.crypto import get_random_string
from .forms import SignUpForm,LoginForm,UserForm,WalletForm,GameForm,FightForm,LoadPointsForm,SendPoint
from django.core import serializers
from django.core.serializers import serialize
import json
from .serializers import GameSerializer,FightSerializer,UserSerializer
from django.db.models import Sum,Count


from django_minify_html.middleware import MinifyHtmlMiddleware
from django.http import HttpRequest, HttpResponse

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError

from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from django.urls import reverse
from datetime import datetime

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
import requests
from django.db.models import Sum, Q, Case, When, DecimalField
from django.db.models import Sum, Q, F

import pytz


tz = pytz.timezone('Asia/Manila')
now = timezone.now()



class ProjectMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    def should_minify(self, request: HttpRequest, response: HttpResponse) -> bool:
        return super().should_minify(request, response) and not request.path.startswith(
            "/admin/"
        )



def index(request):
     # bets=Bet.objects.select_related('fight__f_game').all()
     # ldata=serialize('json',bets)
     # gdata=json.loads(ldata)
     
     if request.user.is_authenticated:
          return redirect('homepage')
     referral=request.META['HTTP_HOST']+'/agent='+get_random_string(50)
     context={
          'page':'AUTHENTICATION',
          'login_frm':LoginForm()
     }
     return render(request,'ugs_app/auth/index.html',context)

def player_games(request,gamecat):
     try:
          games=Games.objects.filter(g_category=gamecat, g_status='OPEN')
     except Exception as e:
          games=''
     context={
               'page':'GAMES',
               'games':list(games),
               'gtitle':gamecat
          } 
     return render(request,'ugs_app/homepage/player_games.html',context)


@login_required(login_url='/')
def homepage(request):
     games=Games.objects.filter(g_status='OPEN')
     ccommi=UserWallet.objects.get(user=request.user.id)
     curcommis = ccommi.commission_rate*100
     totalcom = ccommi.w_commission

     totalclm = ccommi.comms_claimed
     adactivecom = float(totalcom) - float(totalclm)
     try:
          current_date_str = datetime.now().strftime('%Y-%m-%d')
          mydailycoms = Commission.objects.filter(c_agent=request.user.id,created__date=current_date_str).aggregate(total=Sum('c_commission'))['total']
          if mydailycoms is None:
               mydailycoms = 0
     except Exception as e:
          mydailycoms = 0


     result = Points.objects.filter(Q(p_sender=request.user.id, p_transtype="DEPOSIT") | Q(p_receiver=request.user.id, p_transtype="WITHDRAW")).aggregate(
     total_deposit=Sum(Case(
          When(p_transtype="DEPOSIT", then='p_amount'),
          output_field=DecimalField()
     )),
     total_withdraw=Sum(Case(
          When(p_transtype="WITHDRAW", then='p_amount'),
          output_field=DecimalField()
     ))
     )
     deposit = result.get('total_deposit') or 0
     withdraw = result.get('total_withdraw') or 0
     
     # ///////////////////////
     dumresult = Points.objects.filter(
    Q(p_sender=request.user.id, p_transtype="DEPOSIT") | 
    Q(p_receiver=request.user.id, p_transtype="WITHDRAW")
     ).aggregate(
          dum_deposit=Sum(
               Case(
                    When(
                         Q(p_transtype="DEPOSIT") & Q(p_receiver__useraccount__dummy='1'), 
                         then='p_amount'
                    ),
                    output_field=DecimalField()
               )
          ),
          dum_withdraw=Sum(
               Case(
                    When(
                         Q(p_transtype="WITHDRAW") & Q(p_sender__useraccount__dummy='1'), 
                         then='p_amount'
                    ),
                    output_field=DecimalField()
               )
          )
     )
     dumdeposit = dumresult.get('dum_deposit') or 0
     dumwithdraw = dumresult.get('dum_withdraw') or 0
     # //////////////////////



     try:
          # realbet=Bet.objects.exclude(status='PENDING').aggregate(total=Sum('amount'))['total']
          realbet=Bet.objects.exclude(winStat='3').exclude(winStat='4').aggregate(total=Sum('amount'))['total']
          if realbet is None:
               realbet=0
     except Exception as e:
          realbet=0
     # ////////////////////
     try:
          aggregates = Bet.objects.exclude(winStat='3').exclude(winStat='4').aggregate(
               dummybet=Sum('amount', filter=Q(player__useraccount__dummy='1'))
          )
          dummybet = aggregates.get('dummybet') or 0
     except Exception as e:
          dummybet = 0

     try:
          aggregates = Bet.objects.exclude(winStat='3').exclude(winStat='4').filter(category='DRAW').aggregate(
               dummybetdraw=Sum('amount', filter=Q(player__useraccount__dummy='1'))
          )
          dummybetdraw = aggregates.get('dummybetdraw') or 0
     except Exception as e:
          dummybetdraw = 0
     # //////////////////



     try:
          wondecimals=Bet.objects.filter(winStat=1).aggregate(total=Sum('decimal'))['total']
          if wondecimals is None:
               wondecimals=0
     except Exception as e:
          wondecimals=0
     # ////////////////////
     try:
          aggregates = Bet.objects.filter(winStat=1).aggregate(
               dummydecimal=Sum('decimal', filter=Q(player__useraccount__dummy='1'))
          )
          dummydecimal = aggregates.get('dummydecimal') or 0
     except Exception as e:
          dummydecimal = 0
     # //////////////////




     try:
          aggregates = UserWallet.objects.aggregate(
               plpoint=Sum('w_balance', filter=Q(user__useraccount__usertype='PLAYER')),
               agntpoint=Sum('w_balance', filter=~Q(user__useraccount__usertype__in=['PLAYER', 'ADMIN', 'SUPER ADMIN'])),
               tlcom=Sum('w_commission', filter=~Q(user__useraccount__usertype__in=['ADMIN', 'SUPER ADMIN'])),
               clmcom=Sum('comms_claimed', filter=~Q(user__useraccount__usertype__in=['ADMIN', 'SUPER ADMIN']))
          )
          plpoint = aggregates.get('plpoint') or 0
          agntpoint = aggregates.get('agntpoint') or 0
          tlcom = aggregates.get('tlcom') or 0
          clmcom = aggregates.get('clmcom') or 0
          agntcomm = float(tlcom) - float(clmcom)

     except Exception as e:
          plpoint = agntpoint = tlcom = clmcom = agntcomm = 0

     # //////////////////////////
     try:
          aggregates = UserWallet.objects.aggregate(
               dumplpoint=Sum('w_balance', filter=Q(user__useraccount__usertype='PLAYER') & Q(user__useraccount__dummy='1')),               
               dumagntpoint = Sum('w_balance', filter=~Q(user__useraccount__usertype__in=['PLAYER', 'ADMIN', 'SUPER ADMIN']) & Q(user__useraccount__dummy='1'))
          )
          dumplpoint = aggregates.get('dumplpoint') or 0
          dumagntpoint = aggregates.get('dumagntpoint') or 0
     except Exception as e:
          dumplpoint = 0
          dumagntpoint = 0
     # /////////////////////////
     


     try:
          totalusers=UserAccount.objects.exclude(usertype='SUPER ADMIN').exclude(usertype='ADMIN') .exclude(usertype='DECLARATOR').aggregate(total=Count('user'))['total']
          if totalusers is None:
               totalusers=0
     except Exception as e:
          totalusers=0

     try:
          inactiveusers=UserAccount.objects.filter(status='INACTIVE').exclude(usertype='SUPER ADMIN').exclude(usertype='ADMIN') .exclude(usertype='DECLARATOR').aggregate(total=Count('user'))['total']
          if inactiveusers is None:
               inactiveusers=0
     except Exception as e:
          inactiveusers=0
     try:
          activeusers=UserAccount.objects.filter(status='ACTIVE').exclude(usertype='SUPER ADMIN').exclude(usertype='ADMIN') .exclude(usertype='DECLARATOR').aggregate(total=Count('user'))['total']
          if activeusers is None:
               activeusers=0
     except Exception as e:
          activeusers=0

     
     

     try:
          drawbet=Bet.objects.filter(category='DRAW').aggregate(total=Sum('amount'))['total']
          if drawbet is None:
               drawbet=0
     except Exception as e:
          drawbet=0

     try:
          drawwins=Bet.objects.filter(category='DRAW', result='DRAW').aggregate(total=Sum('won_amnt'))['total']
          if drawwins is None:
               drawwins=0
     except Exception as e:
          drawwins=0

     drawincome = drawbet-drawwins
     newrealbet = float(realbet) - float(dummybet)
     realdecimal = float(wondecimals) - float(dummydecimal)
     realplpoint = float(plpoint) - float(dumplpoint)
     realdeposit = float(deposit) - float(dumdeposit)
     realwithdraw = float(withdraw) - float(dumwithdraw)
     realdummybet = float(dummybet) - float(dummybetdraw)
     realagntpoint = float(agntpoint) - float(dumagntpoint)

     
     context={
          'page':'HOMEPAGE',
          'comrates':curcommis,
          'mydailycoms':mydailycoms,
           'games':list(games),
           'ref_url':request.META['HTTP_HOST']+'/registration/',
           'wallet':request.user.userwallet.w_balance,
          # admin
           'deposit':realdeposit,
           'totaldeposit':deposit,
           'dumdeposit':dumdeposit,
           'withdraw':realwithdraw,
           'totalwithdraw':withdraw,
           'dumwithdraw':dumwithdraw,
           'realbet':newrealbet,
           'totalbet':realbet,
           'dummybet':realdummybet,
           'dummybetdraw':dummybetdraw,
           'plpoint':realplpoint,
           'totalplpoint':plpoint,
           'dumplpoint':dumplpoint,
           'adactivecom':adactivecom,
           'agntpoint':realagntpoint,
           'totalagntpoint':agntpoint,
           'dumagntpoint':dumagntpoint,
           'agntcomm':agntcomm,
           'wondecimals':realdecimal,
           'totaldecimal':wondecimals,
           'dummydecimal':dummydecimal,
           'drawincome':drawincome,
          #  super admin
          'totalusers':totalusers,
          'inactiveusers':inactiveusers,
          'activeusers':activeusers,
          'spdeposit':deposit,
          'spwithdraw':withdraw,
     }
     if request.user.useraccount.usertype == 'SUPER ADMIN':
          return render(request,'ugs_app/homepage/super_admin.html',context)
     elif request.user.useraccount.usertype == 'ADMIN':
          return render(request,'ugs_app/homepage/admin.html',context)
     elif request.user.useraccount.usertype == 'DECLARATOR':
          return render(request,'ugs_app/homepage/declarator.html',context)
     elif request.user.useraccount.usertype == 'PLAYER':
          return render(request,'ugs_app/homepage/player.html',context)
     elif request.user.useraccount.usertype == 'MASTER OPERATOR' or request.user.useraccount.usertype == 'INCORPORATOR' or request.user.useraccount.usertype == 'SUB ADMIN' or request.user.useraccount.usertype == 'SUB OPERATOR' or request.user.useraccount.usertype == 'MASTER AGENT':
          return render(request,'ugs_app/homepage/agent.html',context)




@login_required(login_url='/')
def games(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'PLAYER':
          games=Games.objects.filter(g_status='OPEN')
          context={
               'page':'GAMES',
               'games':list(games)
          }
          return render(request,'ugs_app/homepage/games.html',context)
    else:
         return redirect(reverse('homepage'))

@login_required(login_url='/')
def setting(request):
     context={
          'page':'SETTING',
          'form':SignUpForm()
     }
     return render(request,'ugs_app/homepage/setting.html',context)





@login_required(login_url='/')
def users(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN':
          users=UserProfile.objects.all().order_by('-date_joined').exclude(useraccount__usertype='DECLARATOR').exclude(useraccount__usertype='SUPER ADMIN').exclude(useraccount__usertype='ADMIN')
          
          for u in users:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100 
               else:
                    comrate = 0
               
               u.comrate = comrate

          context = {
               'page': 'USERS',
               'signup_frm': SignUpForm(),
               'user_frm': UserForm(),
               'users': list(users)
               }
          return render(request,'ugs_app/homepage/users.html',context)
     else:
           return redirect(reverse('homepage'))
     







# updated admin commission rate 100924
@csrf_exempt
def adminActivateUser(request):
     aid=request.POST.get('acct_id')
     astat=request.POST.get('plstatus')
     comirate=request.POST.get('commirate')
     commi=request.POST.get('adcomrate')
     agentid=request.POST.get('agentid')
     usertype=request.POST.get('usertype')

     acommi=UserWallet.objects.get(user=agentid)
     aurcommi = acommi.commission_rate
     nwcommi = comirate

     if usertype == 'ADMIN' or usertype == 'MASTER OPERATOR' or usertype == 'INCORPORATOR' or usertype == 'SUB ADMIN' or usertype == 'SUB OPERATOR' or usertype == 'MASTER AGENT':
          comms = Decimal(commi) / 100
          aurcommif = Decimal(aurcommi)
          comminf = Decimal(comms)
          print(f"Debug: commi={commi}, comirate={comirate}")
          # curcommif = Decimal(curcommi)
          # modulo    = curcommif-comminf
          print(comminf)

          if aurcommif>comminf: 
               try:
                    ucommi=UserAccount.objects.get(user=aid)
                    accounttype = ucommi.usertype
                    if accounttype == "PLAYER":
                         ucommi.usertype=usertype
                    ucommi.status=astat
                    ucommi.save()
          
                    wcommi=UserWallet.objects.get(user=aid)
                    ucommibal=wcommi.commission_rate
                    uplinecom = aurcommif-comminf
                   
                    if ucommibal==0.00 and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom

                    elif comminf>ucommibal and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom
                    else:
                         nwcommi = comirate
                         
                    if wcommi.default_rate == 0.00:
                       wcommi.default_rate = comminf
                    wcommi.save()

                    data='ok'
               except Exception as e:
                   data='Error'
          else:
            data='Error'
     else:
          try:
             ucommi=UserAccount.objects.get(user=aid)
             ucommi.status=astat
             ucommi.save()
             nwcommi = comirate
             data='ok'
          except Exception as e:
           data='Error'
     
     return JsonResponse({'data':data, 'nwcommi':nwcommi})
# updated admin commission rate 100924





# updated super admin commission rate 100924
@csrf_exempt
def supradmiactiveuser(request):
     aid=request.POST.get('acct_id')
     astat=request.POST.get('plstatus')
     comirate=request.POST.get('commirate')
     commi=request.POST.get('commission')
     agentid=request.POST.get('agentid')
     usertype=request.POST.get('usertype')

     # ccommi=UserWallet.objects.get(user=aid)
     # curcommi = ccommi.commission_rate
     aurcommi = 0.13
     nwcommi = 0
     
     if usertype == 'ADMIN' or usertype == 'MASTER OPERATOR' or usertype == 'INCORPORATOR' or usertype == 'SUB ADMIN' or usertype == 'SUB OPERATOR' or usertype == 'MASTER AGENT':
          comms = Decimal(commi) / Decimal(100)
          aurcommif = Decimal(aurcommi)
          comminf = Decimal(comms)
          # curcommif = Decimal(curcommi)
          # modulo    = curcommif-comminf
          print(aurcommi)
          print(comminf)
          if aurcommif>=comminf: 
               try:
                    ucommi=UserAccount.objects.get(user=aid)
                    accounttype = ucommi.usertype
                    if accounttype == "PLAYER":
                         ucommi.usertype=usertype
                    ucommi.status=astat
                    ucommi.save()
          
                    wcommi=UserWallet.objects.get(user=aid)
                    ucommibal=wcommi.commission_rate
                    uplinecom = aurcommif-comminf

                    if ucommibal==0.00 and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom

                    elif comminf>=ucommibal and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom
                    else:
                         nwcommi = 0
                    
                    if wcommi.default_rate == 0.00:
                       wcommi.default_rate = comminf
                    wcommi.save()

                    data='ok'
               except Exception as e:
                   data='Error1'
          else:
            data='Error2'
     else:
          try:
             ucommi=UserAccount.objects.get(user=aid)
             ucommi.status=astat
             ucommi.save()
             nwcommi = aurcommi
             data='ok'
          except Exception as e:
           data='Error3'
     
     return JsonResponse({'data':data, 'nwcommi':nwcommi})






@login_required(login_url='/')
def import_adminUser(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
          users=UserProfile.objects.all().order_by('-date_joined').exclude(useraccount__usertype='DECLARATOR').exclude(useraccount__usertype='SUPER ADMIN').exclude(useraccount__usertype='ADMIN')
          for u in users:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100
               else:
                    comrate = 0
               u.comrate = comrate

               context={
               'page':'USERS',
               'userId':request.user.id,
               'users':list(users)
          }
          html_content = render_to_string('ugs_app/homepage/import_adminUser.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))
    

@login_required(login_url='/')
def import_super_adminuser(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'SUPER ADMIN':
          myagent=UserProfile.objects.all().exclude(useraccount__usertype='SUPER ADMIN')
          for u in myagent:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100 
               else:
                    comrate = 0 
               u.comrate = comrate 
          context={
               'page':'DOWNLINES',
               'signup_frm':SignUpForm(),
               'user_frm':UserForm(),
               'users':myagent
          }
          html_content = render_to_string('ugs_app/homepage/imprt_supaduser.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))










@csrf_exempt
def upstat(request):
     aid=request.POST.get('acc_id')
     astat=request.POST.get('acc_stat')
     acctype=request.POST.get('acc_type')
     agentcommi=request.POST.get('agentcommi')
     try:
          ucommi=UserAccount.objects.get(user=aid)
          ucommi.status=astat
          ucommi.usertype=acctype
          ucommi.save()
          
          wcommi=UserWallet.objects.get(user=aid)
          wcommi.commission_rate=agentcommi
          if wcommi.default_rate == 0.00:
             wcommi.default_rate = agentcommi
          wcommi.save()
        
          data='ok'
     except Exception as e:
          print(e)
          data='Error'
     return JsonResponse({'data':data})



@csrf_exempt
def getusers(request):
     acc=UserProfile.objects.all().select_related('useraccount',)
     data=[]
     for a in acc:
          a.date_joined=a.date_joined.strftime("%Y-%m-%d %I:%M %p")
        
          try:
               gwallet=UserWallet.objects.get(user=a)
               wallet=gwallet.w_balance
               comrate=gwallet.commission_rate
          except Exception as e:
               wallet=0
          res={
               'uid':a.id,
               'user':a.username,
               'type':a.useraccount.usertype,
               'agent':str(a.useraccount.user_agent),
               'wallet':wallet,
               'comrate':comrate,
               'status':a.useraccount.status,
               'datejoin':a.date_joined

          }

          data.append(res)
     return JsonResponse({'data':data})
     
     # return JsonResponse(data,safe=False)
# @xframe_options_exempt


# @xframe_options_sameorigin
@xframe_options_exempt
def arena(request,game_id):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'PLAYER':    
          fstatus=''
          fid=''
          meron=0
          wala=0
          fnum=0
          mymeronbet=0
          mywalabet=0
          mydrawbet=0
          mylongbet=0
          print(game_id)
          try:
               g_arena=Games.objects.get(g_id=game_id)
               gname=g_arena.g_name
               gid=g_arena.g_id
               meron_name=g_arena.g_redname
               wala_name=g_arena.g_bluename
               video=g_arena.g_link
               category=g_arena.g_category
               img=g_arena.g_image
               try:
                    g_fight=Fight.objects.filter(f_game=g_arena).latest('f_created')
                    fid=g_fight.f_id
                    status=g_fight.f_status
                    fnum=g_fight.f_number
                    fmulti=g_fight.f_multiplier
                    fwin=g_fight.f_winner
                    flong=g_fight.f_longest
                    try:
                         mymeronbet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='MERON',player=request.user).aggregate(total=Sum('amount'))['total']
                         if mymeronbet is None:
                              mymeronbet=0
                    except Exception as e:
                         mymeronbet=0
                    try:
                         mywalabet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='WALA',player=request.user).aggregate(total=Sum('amount'))['total'] 
                         if mywalabet is None:
                              mywalabet=0
                    except Exception as e:
                         mywalabet=0
                    try:
                         mydrawbet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='DRAW',player=request.user).aggregate(total=Sum('amount'))['total'] 
                         if mydrawbet is None:
                              mydrawbet=0
                    except Exception as e:
                         mydrawbet=0
                    try:
                         mylongbet=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST',l_player=request.user).aggregate(total=Sum('l_amount'))['total'] 
                         if mylongbet is None:
                              mylongbet=0
                    except Exception as e:
                         mylongbet=0
                    try:
                         meron=Bet.objects.filter(fight=fid,eventid=game_id,category='MERON').aggregate(total=Sum('amount'))['total']
                         if meron is None:
                              meron=0
                    except Exception as e:
                         meron=0
                    try:
                         wala=Bet.objects.filter(fight=fid,eventid=game_id,category='WALA').aggregate(total=Sum('amount'))['total'] 
                         if wala is None:
                              wala=0
                    except Exception as e:
                         wala=0
               except Exception as e:
                    status='CLOSED'
                    fnum=0
                    fmulti=0
                    fwin=0
                    flong=0
                    fid=0
          except Exception as e:
               print(e)

          dmeron=float(meron)*float(fmulti)
          dwala=float(wala)*float(fmulti)
          wallet=UserWallet.objects.get(user=request.user)
          wbalance=wallet.w_balance
     
          context={
               'page':'ARENA',
               'game':game_id,
               'game_name':gname,
               'betstat':status,
               'fight_id':fid,
               'fnumber':fnum,
               'wallet':wbalance,
               'mybetmeron':mymeronbet,
               'mybetwala':mywalabet,
               'mydrawbet':mydrawbet,
               'mylongbet':mylongbet,
               'dmeron':dmeron,
               'dwala':dwala,
               'nmeron':meron_name,
               'nwala':wala_name,
               'video':video,
               'game_category':category,
               'game_img':img
          }
          return render(request,'ugs_app/homepage/player_arena.html',context)
     else:
          return redirect(reverse('homepage'))












# @xframe_options_sameorigin
@xframe_options_exempt
def decla_arena(request,game_id):
     referrer = request.META.get('HTTP_REFERER')
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'DECLARATOR':    
          fform=FightForm()
          fstatus=''
          fid=''
          meron=0
          wala=0
          fnum=0
          try:
               g_arena=Games.objects.get(g_id=game_id)
               gname=g_arena.g_name
               gid=g_arena.g_id
               meron_name=g_arena.g_redname
               wala_name=g_arena.g_bluename
               video=g_arena.g_link

               try:
                    g_fight=Fight.objects.filter(f_game=g_arena).latest('f_created')
                    fid=g_fight.f_id
                    status=g_fight.f_status
                    fnum=g_fight.f_number
                    fmulti=g_fight.f_multiplier
                    fwin=g_fight.f_winner
                    flong=g_fight.f_longest
                    # try:
                    #      mymeronbet=Bet.objects.filter(fight=g_fight,status='PENDING',category='MERON',player=request.user).aggregate(total=Sum('amount'))['total']
                    #      if mymeronbet is None:
                    #           mymeronbet=0
                    # except Exception as e:
                    #      mymeronbet=0
                         
                    # try:
                    #      mywalabet=Bet.objects.filter(fight=g_fight,status='PENDING',category='WALA',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    #      if mywalabet is None:
                    #           mywalabet=0
                    # except Exception as e:
                    #      mywalabet=0

                    try:
                         meron=Bet.objects.filter(fight=fid,eventid=game_id,category='MERON').aggregate(total=Sum('amount'))['total']
                         if meron is None:
                              meron=0
                    except Exception as e:
                         meron=0
                    try:
                         wala=Bet.objects.filter(fight=fid,eventid=game_id,category='WALA').aggregate(total=Sum('amount'))['total'] 
                         if wala is None:
                              wala=0
                    except Exception as e:
                         wala=0
                    try:
                         draw=Bet.objects.filter(fight=fid,eventid=game_id,category='DRAW').aggregate(total=Sum('amount'))['total'] 
                         if draw is None:
                              draw=0
                    except Exception as e:
                         draw=0

                    try:
                         long=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST').aggregate(total=Sum('l_amount'))['total']
                         clong=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST').aggregate(total=Count('id'))['total'] 
                         if long is None or clong is None:
                              long=0
                              clong=0
                    except Exception as e:
                         long=0
                         clong=0

               except Exception as e:
                    status='NONE'
                    fnum=0
                    fmulti=0
                    fwin=0
                    flong=0
                    fid=0
                    draw=0
                    long=0
                    clong=0
          except Exception as e:
               print(e)
          
          dmeron=float(meron)*float(fmulti)
          dwala=float(wala)*float(fmulti)
          wallet=UserWallet.objects.get(user=request.user)
          wbalance=wallet.w_balance
     
          context={
               'page':'DECLA ARENA',
               'game':game_id,
               'game_name':gname,
               'meron':meron,
               'wala':wala,
               'draw':draw,
               'long':long,
               'status':status,
               'fnum':fnum,
               'fwin':fwin,
               'flong':flong,
               'multiplier':fmulti,
               'fform':fform,
               'fight_id':fid,
               'wallet':wbalance,
               # 'mybetmeron':mymeronbet,
               # 'mybetwala':mywalabet,
               'dmeron':dmeron,
               'dwala':dwala,
               'nmeron':meron_name,
               'nwala':wala_name,
               'clong':clong,
               'video':video,
               'referer':referrer
          }
          return render(request,'ugs_app/homepage/decla_arena.html',context)
     else:
         return redirect(reverse('homepage'))




# disbusement
# upline commission - disbuse
@csrf_exempt
def disburse(request):
    fid = request.POST.get('fight')
    try:
        if not fid:
            raise ValueError("Fight ID is required")

        gfight = Fight.objects.get(f_id=fid)
        gfight.f_status = 'DONE'
        gfight.save()

        bets = Bet.objects.filter(fight=gfight, winStat=0)
        if not bets.exists():
            raise ValueError("No bets found for this fight")

        for bet in bets:
          with transaction.atomic():
               wonamount = bet.winning_amnt
               gwallet=UserWallet.objects.get(user=bet.player.id)
               curbalance=gwallet.w_balance
               pointwins=gwallet.w_betwins
               if gfight.f_winner == 'MERON' or gfight.f_winner == 'WALA':
                    if gfight.f_winner == bet.category:
                         betstat = 'WIN'
                         newbal=float(curbalance) + float(wonamount)
                         newpoint=int(pointwins) + float(wonamount)
                         
                         gwallet.w_balance=newbal
                         gwallet.w_betwins=newpoint
                         gwallet.save() 
                         Bet.objects.filter(id=bet.id, status='PENDING').update(won_amnt = wonamount, status=betstat, winStat=1, result=gfight.f_winner)
                    else:
                         betstat = 'LOSE'
                         Bet.objects.filter(id=bet.id, status='PENDING').update(won_amnt = 0, status=betstat, winStat=2, result=gfight.f_winner)                  

                    # AGENT COMMISSION DISTRIBUTION 101824  
                    user_account = UserAccount.objects.get(user_id=bet.player.id) 
                    user_agent = user_account.user_agent.id  
                    agent_up = bet.player.id

                    commi_distrib = distribute_commission_upward(user_agent, agent_up, bet.amount)
                    for commission_data in commi_distrib:
                         if commission_data['user_id'] == bet.player.id or bet.category == "DRAW" or commission_data['commission'] <= 0:
                              continue
                         if gfight.f_winner:
                              try:
                                   with transaction.atomic():
                                        pwallet = UserWallet.objects.select_for_update().get(user=commission_data['user_id'])
                                        combalance = float(pwallet.w_commission) 
                                        newcom = combalance + float(commission_data['commission'])
                                        pwallet.w_commission = newcom
                                        pwallet.save()

                                        commission = Commission(
                                        c_fight=gfight,
                                        c_fnumber=gfight.f_number,
                                        c_player=bet.player.id,
                                        c_betamnt=bet.amount,
                                        c_winner=gfight.f_winner,
                                        c_commission=commission_data['commission'],
                                        c_agent=commission_data['user_id'],
                                        c_event=bet.event,
                                        c_eventid=bet.eventid,
                                        c_bet=bet.id,
                                        c_level=commission_data['comm_level'],
                                   )
                                   commission.save()
                                   data = 'ok'
                              except ObjectDoesNotExist:
                                   print(f"UserWallet for user {commission_data['user_id']} does not exist.")
                              except Exception as e:
                                   print(f"An error occurred while updating UserWallet: {e}")
                                   data = 'ok'
                         # AGENT COMMISSION DISTRIBUTION 101824
               elif gfight.f_winner == 'DRAW':
                    if gfight.f_winner == bet.category:
                         betstat = 'WIN'
                         newbal=float(curbalance) + float(wonamount)
                         newpoint=int(pointwins) + float(wonamount)
                         
                         gwallet.w_balance=newbal
                         gwallet.w_betwins=newpoint
                         gwallet.save() 
                         Bet.objects.filter(id=bet.id, status='PENDING').update(won_amnt = wonamount, status=betstat, winStat=1, result=gfight.f_winner)
                    else:
                         betstat = 'DRAW'
                         refundamnt = bet.amount
                         Bet.objects.filter(id=bet.id).update(won_amnt = 0, status=betstat, winStat=3, result=gfight.f_winner)

                         clwallet=UserWallet.objects.get(user=bet.player.id)
                         curbal=clwallet.w_balance
                         newbals=float(curbal) + float(refundamnt)
                         clwallet.w_balance=newbals
                         clwallet.save()

               else:
                    refundamnt = bet.amount
                    betstat = 'CANCELLED'
                    Bet.objects.filter(id=bet.id).update(won_amnt = 0, status=betstat, winStat=4, result=gfight.f_winner)

                    clwallet=UserWallet.objects.get(user=bet.player.id)
                    curbal=clwallet.w_balance

                    newbals=float(curbal) + float(refundamnt)
                    clwallet.w_balance=newbals
                    clwallet.save()

          data = 'ok'
    except Exception as e:
        data = f"Error: {e}"
    return JsonResponse({'data': data})


def distribute_commission_upward(user_agent, agent_up, bet_amount): 
    commi_distrib = []
    visited = set()
    distribute_upward(user_agent, agent_up, bet_amount, commi_distrib, visited, count=0)
    return commi_distrib

def distribute_upward(user_agent, agent_up, bet_amount, commi_distrib, visited, count):
    if user_agent in visited:
          return
    visited.add(user_agent)

    try:
          count += 1
          user_account = UserAccount.objects.get(user_id=user_agent)
          user_agentup = UserAccount.objects.get(user_id=agent_up)

          user_wallet = UserWallet.objects.get(user=user_account.user)
          agent_commrate1 = float(user_wallet.commission_rate)

          agentwallet = UserWallet.objects.get(user=user_agentup.user)
          agent_commrate2 = float(agentwallet.commission_rate)

          if count == 1:
               user_commission = bet_amount * agent_commrate1
          else:
               indirectcomm = agent_commrate1 - agent_commrate2
               user_commission = bet_amount * indirectcomm

          commi_distrib.append({
               'user_id': user_agent,
               'commission': user_commission,
               'comm_level': count
          })
          print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
          print(f" {count} - Direct:{agent_up} - Upline:{user_agent} - {agent_commrate1} - {agent_commrate2} = {user_commission}")
          print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')

          if user_account.user_agent_id:
               distribute_upward(user_account.user_agent_id, user_agentup.user_agent_id, bet_amount, commi_distrib, visited, count)
    except UserAccount.DoesNotExist:
        commi_distrib.append({'user_id': user_agent, 'commission': 0})
    except UserWallet.DoesNotExist:
        commi_distrib.append({'user_id': user_agent, 'commission': 0})











# DECLA UPDATE FIGHT STATUS /////////
@csrf_exempt
def fight_stat(request):
    fid = request.POST.get('fid')
    typ = request.POST.get('typ')
    game_id=request.POST.get('game')
    data = 0
    mymeronbet = 0
    mywalabet = 0
    try:
        fight = Fight.objects.get(f_id=fid)
        fight.f_status = typ
     #    fight.f_status = 'LAST CALL'
        fight.save()
        if typ == 'CLOSING':
            bets = Bet.objects.filter(fight=fight.f_id,eventid=game_id)
            if not bets.exists():
                raise ValueError("No bets found for this fight")

            try:
                cgame = Games.objects.get(g_id=game_id)
                plasada = cgame.g_plasada
                
            except Exception as e:
                print(e)
                plasada = 0
            

            try:
                gf = Fight.objects.filter(f_game=game_id).latest('f_created')
                fid = gf.f_id
                fmulti = gf.f_multiplier
                status = gf.f_status
                game_num = gf.f_number
                winner = gf.f_winner
            except Exception as e:
                fid = 0
                status = ''
                game_num = 0
                fmulti = 0
                winner = ''

            try:
                meron = Bet.objects.filter(fight=fid,eventid=game_id, category='MERON').aggregate(total=Sum('amount'))['total']
                if meron is None:
                    meron = 0
            except Exception as e:
                meron = 0

            try:
                wala = Bet.objects.filter(fight=fid,eventid=game_id, category='WALA').aggregate(total=Sum('amount'))['total']
                if wala is None:
                    wala = 0
            except Exception as e:
                wala = 0

            # COMPUTATION
            totmw = meron + wala
            # PLASADA
            totpla = float(plasada) * float(totmw)
            lesspla = totmw - totpla

            if meron > 0:
                meronlesspla = lesspla / meron
                meronpayout = meronlesspla * 100
            else:
                meronlesspla = lesspla
                meronpayout = meronlesspla * 100

            if wala > 0:
                walalesspla = lesspla / wala
                walapayout = walalesspla * 100
            else:
                walalesspla = lesspla
                walapayout = walalesspla * 100

            # odds
            meronodds = meronpayout * 0.01
            walaodds = walapayout * 0.01
         
            for bet in bets:
                try:
                    mymeronbet = Bet.objects.filter(id=bet.id, fight=fid, eventid=game_id,status='PENDING', category='MERON', player=bet.player.id).aggregate(total=Sum('amount'))['total']
                    if mymeronbet is None:
                        mymeronbet = 0
                except Exception as e:
                    mymeronbet = 0

                try:
                    mywalabet = Bet.objects.filter(id=bet.id, fight=fid, eventid=game_id, status='PENDING', category='WALA', player=bet.player.id).aggregate(total=Sum('amount'))['total']
                    if mywalabet is None:
                        mywalabet = 0
                except Exception as e:
                    mywalabet = 0

                try:
                    mydrawbet = Bet.objects.filter(id=bet.id, fight=fid, eventid=game_id, status='PENDING', category='DRAW', player=bet.player.id).aggregate(total=Sum('amount'))['total']
                    if mydrawbet is None:
                        mydrawbet = 0
                except Exception as e:
                    mydrawbet = 0

                # Calculate the winnings
                merontowin = meronodds * mymeronbet
                walatowin = walaodds * mywalabet
                # player dummy total bet
                dmeron = fmulti * meron
                dwala = fmulti * wala

                if bet.category == 'MERON':
                     winning_bet = merontowin
                elif  bet.category == 'WALA':
                     winning_bet = walatowin
                elif  bet.category == 'LONGEST':
                     winning_bet = 0
                elif  bet.category == 'DRAW':
                     winning_bet = mydrawbet*8

                value_str = str(winning_bet)

                if '.' in value_str:
                    integer_part, decimal_part = value_str.split('.')
                    integer_part = int(integer_part)
                    decimal_part = float(f"0.{decimal_part}")
                else:
                    integer_part = int(value_str)
                    decimal_part = 0.0 

                print(integer_part)  # 44
                print(decimal_part)  # 0.67

               #  print(f"Bet ID: {bet.id}, Bettor ID: {bet.player.id}, Bettor: {bet.player.username}, Player bet amount: {mymeronbet}, Bet: {bet.category}, Payout : {winning_bet}")
               #  SAVE WINNING BET AMOUNT
                Bet.objects.filter(id=bet.id, winStat=0).update(winning_amnt = integer_part, decimal=decimal_part)
               #  SAVE WINNING BET AMOUNT

            fight.f_mpout = meronpayout
            fight.f_wpout = walapayout
            fight.save()
        data = 1     
    except Fight.DoesNotExist:
        data = 0
     #    print(f"Fight with ID {fid} does not exist.")

    except Exception as e:
     #    print(f"Error: {e}")
        data = 0

    return JsonResponse({'data': data})










@csrf_exempt
def updatewallet(request):
    amount = request.POST.get('amount')
    ttrans = request.POST.get('ttype')
    fid = request.POST.get('fid')
    betin = request.POST.get('betin')
    response = 'bad00'
    
    try:
        with transaction.atomic():
          gwallet = UserWallet.objects.get(user=request.user)
          curbalance = gwallet.w_balance
          amount = Decimal(amount) if amount else 0
          if amount>=1 and amount <= curbalance:
               newbal = curbalance - amount
               try:
                    fight = Fight.objects.get(f_id=fid)
                    fstatus = fight.f_status
                    eventname = fight.f_game.g_name
                    eventnid = fight.f_game.g_id

                    try:
                         fdrawbet = Bet.objects.filter(fight=fid, eventid=eventnid, status='PENDING', category='DRAW').aggregate(total=Sum('amount'))['total']
                         if fdrawbet is None:
                              fdrawbet = 0
                    except Exception as e:
                              fdrawbet = 0
                              
                    if fstatus in ["OPEN", "LAST CALL"]:
                         # try:
                              if betin == 'LONGEST':
                                   bet = Longestfight.objects.create(
                                        l_fight=fight,
                                        l_amount=amount,
                                        l_category=betin,
                                        l_player=request.user,
                                        l_fightno=fight.f_number,
                                        l_event=eventname,
                                        l_walletbal=curbalance,
                                        l_eventid=eventnid
                                   )
                                   gwallet.w_balance = newbal
                                   gwallet.save()
                                   response = 'success'

                              elif betin == 'DRAW':
                                   totaldraw = fdrawbet+amount
                                   if totaldraw <=1000:
                                        Bet.objects.create(
                                             fight=fight,
                                             amount=amount,
                                             category=betin,
                                             player=request.user,
                                             fightno=fight.f_number,
                                             event=eventname,
                                             walletbal=curbalance,
                                             waltotal=newbal,
                                             eventid=eventnid
                                        )
                                        gwallet.w_balance = newbal
                                        gwallet.save()
                                        response = 'success'  
                                   else:
                                        response = 'drawlimit'  
                              else:
                                   bet = Bet.objects.create(
                                        fight=fight,
                                        amount=amount,
                                        category=betin,
                                        player=request.user,
                                        fightno=fight.f_number,
                                        event=eventname,
                                        walletbal=curbalance,
                                        waltotal=newbal,
                                        eventid=eventnid
                                   )
                                   gwallet.w_balance = newbal
                                   gwallet.save()
                                   response = 'success'
                         # except Exception as e:
                         #      print(f"Error creating bet: {e}")
                         # response = 'bad06'
                    else:
                         response = 'bad05'
                         
               except ObjectDoesNotExist:
                    print(f"Fight with ID {fid} does not exist.")
                    response = 'bad02'
          else:
               response = 'insufficient'

    except ObjectDoesNotExist:
        print(f"User wallet for {request.user} does not exist.")
        response = 'bad01'
    except Exception as e:
        print(f"Unexpected error: {e}")
        response = 'bad01'

    data = gwallet.w_balance
    return JsonResponse({'response': response, 'data': data})



# DECLARATOR
@csrf_exempt
def delgame(request):
     did=request.POST.get('did')
     dgames=Games.objects.get(g_id=did).delete()
     if dgames:
          data='ok'
     else:
          data='Failed'
     return JsonResponse({'data':data})



@csrf_exempt
def gfight(request):
     gid=request.POST.get('gfid')
     game=Games.objects.get(g_id=gid)
     try:
          gf=Fight.objects.filter(f_game=game).latest('f_created')
          fid=gf.f_id
          fnum=gf.f_number
          fmulti=gf.f_multiplier
          fstat=gf.f_status
          fwin=gf.f_winner
          flong=gf.f_longest
     except Exception as e:
          fid=0
          fnum=0
          fmulti=0
          fwin=''
          flong=0
          fstat='CLOSED'
 
     data={
          'game':game.g_id,
          'fight':fid,
          'fnum':fnum,
          'fmulti':fmulti,
          'fstat':fstat,
          'fwin':fwin,
          'flong':flong
     }
     
     return JsonResponse({'data':data})




@csrf_exempt
def addfight(request):
     fform=FightForm(request.POST or None)
     gid=request.POST.get('fgame')
     f_id=request.POST.get('f_id')
     typ=request.POST.get('f_type')
     code=get_random_string(6)
     fnum=request.POST.get('f_number')
     
     if typ is None:
          try:
               ckfight=Fight.objects.get(f_id=f_id,f_number=fnum)
               data='exist'
          except Exception as e:
           if fform.is_valid():
               nf = fform.save(commit=False)
               print(nf)
               nf.f_code=code
               nf.f_status='CLOSED'
               nf.save()
               data='insert'
           else:
               data='Invalid Form'
     else:
          try:
               gf=Fight.objects.get(f_id=f_id)
               gf.f_number=request.POST.get('f_number')
               gf.f_multiplier=request.POST.get('f_multiplier')
               gf.save()
               data='update'
          except Exception as e:
               print(e)
               data='Not Found'
     print(data)
     return JsonResponse({'data':data})












@login_required(login_url='/')
def decla_games(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'DECLARATOR':
          games=Games.objects.all().order_by('-g_created')
          for g in games:
               g.g_created = g.g_created.strftime("%Y-%m-%d %I:%M %p")
          context={
               'page':'DECLA GAMES',
               'game_frm':GameForm(),
               'games':list(games)
          }
          return render(request,'ugs_app/homepage/decla_games.html',context)
     else:
         return redirect(reverse('homepage'))

@login_required(login_url='/')
def imprt_newgame(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'DECLARATOR':
          games=Games.objects.all().order_by('-g_created')
          for g in games:
               g.g_created = g.g_created.strftime("%Y-%m-%d %I:%M %p")
          context={
               'page':'DECLA GAMES',
               'game_frm':GameForm(),
               'games':list(games)
          }
          html_content = render_to_string('ugs_app/homepage/imprt_new_game.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))


@csrf_exempt
def duplicate_game(request):
     gid=request.POST.get('gid')
     ggames=Games.objects.get(g_id=gid)
     
     img=str(ggames.g_image).split('/')
     data={
          'gname':ggames.g_name,
          'meron':ggames.g_redname,
          'wala':ggames.g_bluename,
          'plasada':ggames.g_plasada,
          'desc':ggames.g_desc,
          'link':ggames.g_link,
          'img':img[1],
          'cat':ggames.g_category,
          'timezone':''
     }
     return JsonResponse({'data':data})


@csrf_exempt
def load_games(request):
     ggames=Games.objects.all().order_by('-g_created').reverse()
     # for g in ggames:
     #      g.g_created = g.g_created.strftime("%Y-%m-%d %I:%M %p")
     ldata=serialize('json',ggames)
     gdata=json.loads(ldata)
     print(gdata)
     return JsonResponse(gdata,safe=False)


@csrf_exempt
def getgame(request):
     gid=request.POST.get('gid')
     upgames=Games.objects.get(g_id=gid)
     # data=upgames
     # ldata=serialize('json',upgames)
     # data=json.loads(ldata)
     data={
          'gname':upgames.g_name,
          'meron':upgames.g_redname,
          'wala':upgames.g_bluename,
          'plasada':upgames.g_plasada,
          'desc':upgames.g_desc,
          'category':upgames.g_category,
          'link':upgames.g_link,
          'image':str(upgames.g_image),
          'status':upgames.g_status    
     }
     return JsonResponse({'data':data})

# declarator
@csrf_exempt
def add_games(request):
     if request.method =='POST':
          gform=GameForm(request.POST, request.FILES)
          if gform.is_valid():
               games = gform.save(commit=False)
               # games.g_created=datetime.datetime.now()
               games.g_by=request.user.id
               games.save()
               data='ok'
          else:
               dform=Games()
               dform.g_name=request.POST.get('g_name')
               dform.g_redname=request.POST.get('g_redname')
               dform.g_bluename=request.POST.get('g_bluename')
               dform.g_plasada=request.POST.get('g_plasada')
               dform.g_desc=request.POST.get('g_desc')
               dform.g_category=request.POST.get('g_category')
               dform.g_link=request.POST.get('g_link')
               dform.g_image='uploads/'+request.POST.get('tg_image')
               dform.g_col=1
               dform.g_by=request.user
               dform.save()
               print(dform)
               data='copy'
        
     return JsonResponse({'data':str(data)})

# declarator
@csrf_exempt
def update_games(request):
     if request.method =='POST':
          gform=GameForm(request.POST, request.FILES)
          games=Games.objects.get(g_id=request.POST.get('g_id'))
          if request.FILES.get('g_image') is None:
               games.g_name=request.POST.get('g_name')
               games.g_redname=request.POST.get('g_redname')
               games.g_bluename=request.POST.get('g_bluename')
               games.g_plasada=request.POST.get('g_plasada')
               games.g_desc=request.POST.get('g_desc')
               games.g_category=request.POST.get('g_category')
               games.g_link=request.POST.get('g_link')
               games.g_status=request.POST.get('g_status')
               games.g_update=datetime.now()
               games.save()
               data='ok'
          else:
               if gform.is_valid():
                    games.g_image=request.FILES.get('g_image')
                    games.g_name=request.POST.get('g_name')
                    games.g_redname=request.POST.get('g_redname')
                    games.g_bluename=request.POST.get('g_bluename')
                    games.g_plasada=request.POST.get('g_plasada')
                    games.g_desc=request.POST.get('g_desc')
                    games.g_category=request.POST.get('g_category')
                    games.g_link=request.POST.get('g_link')
                    games.g_status=request.POST.get('g_status')
                    games.g_update=datetime.now()
                    games.save()
                    data='ok'
               else:
                    data='Not Valid'
     print(data)
     return JsonResponse({'data':str(data)})

@csrf_exempt
def auth_user(request):
     form = LoginForm(request.POST or None)
     msg=''
     if request.method == 'POST':
          if form.is_valid():
               username=form.cleaned_data.get('username')
               password=form.cleaned_data.get('password')
               user=authenticate(username=username, password=password)
               if user is not None:
                    if user.useraccount.status == 'INACTIVE':
                         msg='inactive'
                    else:
                         request.session['usertype'] = user.useraccount.usertype
                         msg='login'
                         login(request,user)
                         status=1
               else:
                    status=0
                    msg='err'
          else:
              status=0
              msg='not valid'

     return JsonResponse({'data':msg})


def signout(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def account_reg(request):
    code=get_random_string(10)
    referral_link=request.META['HTTP_HOST']+'/registration/'+code
    token=get_random_string(6)
    form=SignUpForm()
    userform=UserForm()
    walletform=WalletForm()
    if request.method=='POST':
       account = SignUpForm(data=request.POST)
       userinfo = UserForm(data=request.POST)
     #   wallet=WalletForm(data=request.POST)
     #   print(request.POST.get('contact_no'))
       if account.is_valid() and userinfo.is_valid() :
            user = account.save()
            user.set_password(user.password)
            user.save()
            info = userinfo.save(commit = False)
            info.user = user
            info.usertype=request.POST.get('usertype')
            info.relpass=request.POST.get('password')
            info.referral_code=code
            info.referral_link=referral_link
            info.user_agent=request.user
            info.status='INACTIVE'
            info.save()
            wall=walletform.save(commit = False)
            wall.user=user
            wall.w_balance=0
            wall.w_points=0
            wall.w_commission=0
            wall.w_status='ACTIVE'
            wall.save()
            data='ok'
           
       else:
            data='Error Validating'
    else:
          data=request
    print(data)
    return JsonResponse({'data':data})




@csrf_exempt
def lastcall(request):
     gfid=request.POST.get('gfight')
     # print(gfid)
     cfight=Fight.objects.get(f_id=gfid)
     cfight.f_status='LAST CALL'
     cfight.save()
     data=cfight.f_status
     return JsonResponse({'data':data})

@csrf_exempt
def closebet(request):
     gfid=request.POST.get('cfight')
 
     cfight=Fight.objects.get(f_id=gfid)
     cfight.f_status='CLOSE'
     cfight.save()
     data=cfight.f_status
     return JsonResponse({'data':data})

@csrf_exempt
def openbet(request):
     ofid=request.POST.get('ofight')

     cfight=Fight.objects.get(f_id=ofid)
     cfight.f_status='DONE'
     cfight.save()
     game=cfight.f_game
     fnum=cfight.f_number
     addf=Fight(f_number=fnum +1,f_game=game,f_winner='',f_status='OPEN').save()
     
     data=cfight.f_status
     return JsonResponse({'data':data})






@csrf_exempt
def revert(request):
     fid=request.POST.get('fight')
     try:
          gfight=Fight.objects.get(f_id=fid)
          gfight.f_winner=''
          gfight.f_status='CLOSING'
          gfight.save()
          data='ok'
     except Exception as e:
          data='bad'
 
     return JsonResponse({'data':data})





@csrf_exempt
def nxtfight(request):
     fid=request.POST.get('fight')
     gid=request.POST.get('game')
     multi=request.POST.get('multi')
     code=get_random_string(6)
     fform=FightForm()
     try:
          ggame=Games.objects.get(g_id=gid)
          try:
               gfight=Fight.objects.get(f_id=fid)
               fnum=gfight.f_number
               # data=fnum
               nwf = fform
               if nwf.is_valid:
                    nf = fform.save(commit=False)   
                    nf.f_game=ggame 
                    nf.f_number=fnum + 1
                    nf.f_multiplier=multi
                    nf.f_code=code
                    nf.f_status='CLOSED'
                    nf.f_update=datetime.now()
                    nf.save()
                    data='ok'
          except Exception as e:
               data='bad fight'
     except Exception as e:
          data='bad'
     return JsonResponse({'data':data})

# ////////////////////////////////



def registration(request,code):
     agent=UserAccount.objects.get(referral_code=code)
     context={
          'page':'REGISTRATION',
          'code':code,
          'signup_frm':SignUpForm(),
          'user_frm':UserForm()
     
     }
     return render(request,'ugs_app/auth/registration.html',context)

@csrf_exempt
def player_reg(request):
     code=get_random_string(6)
     referral_link=request.META['HTTP_HOST']+'/registration/'+code
     walletform=WalletForm()
     account = SignUpForm(data=request.POST)
     userinfo=UserForm()

     aid=request.POST.get('code')
     try:
          agent=UserAccount.objects.get(referral_code=aid)
          if agent is not None:
               data='Exist'
               if account.is_valid():
                    user = account.save()
                    user.set_password(user.password)
                    user.save()
                    info = userinfo.save(commit = False)
                    info.user = user
                    info.contact_no=request.POST.get('contact_no')
                    info.usertype='PLAYER'
                    info.relpass=request.POST.get('password')
                    info.referral_code=code
                    info.referral_link=referral_link
                    info.user_agent=agent.user
                    info.status='INACTIVE'
                    info.save()
                    wall=walletform.save(commit = False)
                    wall.user=user
                    wall.w_balance=0
                    wall.w_points=0
                    wall.w_commission=0
                    wall.w_status='ACTIVE'
                    wall.save()
                    data='ok'
               else:
                    data='Form Not Valid'

     except Exception as e:
          data='Referral Agent Not Found!'

     

     return JsonResponse({'data':data})

@csrf_exempt
def uppass(request):
     account = SignUpForm(request.POST, instance=request.user)
     curpassword=request.POST.get('curpass')
     password=request.POST.get('password')
     nuser=request.POST.get('username')

     

     useracc=authenticate(username=request.user.username, password=curpassword)
     if useracc is not None:
          try:
               acc=UserAccount.objects.get(user=request.user)
               acc.relpass=password
               acc.save()
          except Exception as e:
               print('error')
          try:
               guser=UserProfile.objects.get(id=request.user.id)
               guser.username=nuser.upper()
               guser.password=password
               guser.set_password(password)
               guser.save()
               login(request,guser)
               data='ok'
          except Exception as e:
               data='Failed'
     else:
          data='Invalid Password'
     # useracc=authenticate(username=request.user.username, password=curpassword)
     # if useracc is not None:
     #      if account.is_valid():
     #           user = account.save()
     #           user.set_password(user.password)  
     #           user.save()
     #           login(request,user)
     #           data='ok'
     #      else:
     #           data='Invalid Form'
     # else:
     #      data='Invalid Password'
     
     return JsonResponse({'data':data})


def timer(request):
     return render(request,'ugs_app/timer.html')


# SUPER ADMIN
@login_required(login_url='/')
def mydownlines(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'SUPER ADMIN':
          myagent=UserProfile.objects.all().exclude(useraccount__usertype='SUPER ADMIN')
          for u in myagent:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100 
               else:
                    comrate = 0 
               u.comrate = comrate 
          context={
               'page':'DOWNLINES',
               'signup_frm':SignUpForm(),
               'user_frm':UserForm(),
               'users':myagent
          }
          return render(request,'ugs_app/homepage/mydownline.html',context)
     else:
         return redirect(reverse('homepage'))
     






















# -------------------mmmmmmmm---------------------------
@login_required(login_url='/')
def admin_points(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
         user_id = request.user.id
         adminPointsList = Points.objects.select_related('p_sender').filter(p_sender=user_id).order_by('-p_id')

         context = {
            'page': 'adminloadPoints',
            'adminPointsList': adminPointsList,
            
            'SendPoint': SendPoint(),
        }
         return render(request, 'ugs_app/homepage/admin_load_points.html', context)
    else:
         return redirect(reverse('homepage'))
    
      

@csrf_exempt
def loadAdminPoints(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_points = code_point.upper()
        pointsend = request.POST.get('load_amount')
        receiver=UserProfile.objects.get(id=request.POST.get('user_agent'))

        if float(pointsend) >0:
               form = SendPoint(request.POST)
               if form.is_valid():
                    try:
                         points = form.save(commit=False)
                         points.p_sender=request.user
                         points.p_receiver=receiver
                         points.p_code=code_points
                         points.p_amount=request.POST.get('load_amount')
                         points.p_update=datetime.now()
                         points.save()
                         data='ok'
                    except Exception as e:
                         data='Error'

                    try:
                         pwallet=UserWallet.objects.get(user=receiver)
                         curbalance=pwallet.w_balance
                         pointbal=pwallet.w_points
                         newbal=float(curbalance) + float(pointsend)
                         newpoint=float(pointbal) + float(pointsend)
                         pwallet.w_balance=newbal
                         pwallet.w_points=newpoint
                         pwallet.w_dateupdate=datetime.now()
                         pwallet.save() 
                         data='ok'
                    except Exception as e:
                         data='Error'

                    return JsonResponse({'data': data})
               else: 
                    return JsonResponse({'data': 'error', 'errors': form.errors})
        else:
             return JsonResponse({'data': 'invalid'})
    return JsonResponse({'data': 'invalid method'})

@login_required(login_url='/')
def load_adpoints_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
          user_id = request.user.id
          adminPointsList = Points.objects.select_related('p_sender').filter(p_sender=user_id)
          context = {
               'page': 'adminloadPoints',
               'adminPointsList': adminPointsList,
               'SendPoint': SendPoint(),
          }
          html_content = render_to_string('ugs_app/homepage/import_adminPoints.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))


@login_required(login_url='/')
def userapproval(request):
     ccommi=UserWallet.objects.get(user=request.user.id)
     curcommis = ccommi.commission_rate*100
     usertype_ss = request.session.get('usertype')
     if usertype_ss != 'PLAYER':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(
          useraccount__usertype__in=[
               'MASTER OPERATOR', 
               'INCORPORATOR', 
               'SUB ADMIN', 
               'SUB OPERATOR', 
               'MASTER AGENT', 
               'PLAYER',
          ]
          ).exclude(useraccount__status='ACTIVE')     
          for u in myusers:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100
               else:
                    comrate = 0
               
               u.comrate = comrate

               if u.useraccount.user_agent == request.user:
                    users.append(u)
               
          context={
               'comrates':curcommis,
               'mycommi':request.user,
               'page':'USER APPROVAL',
               'users':list(users)
          }
          return render(request,'ugs_app/homepage/user_approval.html',context)
     else:
          return redirect(reverse('homepage'))
     
# updated agent commission rate 100924
@login_required(login_url='/')
def active_agent(request):
     ccommi=UserWallet.objects.get(user=request.user.id)
     curcommis = ccommi.commission_rate*100
     usertype_ss = request.session.get('usertype')
     if usertype_ss != 'PLAYER':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(
          useraccount__usertype__in=['MASTER OPERATOR', 'INCORPORATOR', 'SUB ADMIN', 'SUB OPERATOR', 'MASTER AGENT'],useraccount__status='ACTIVE')
          
          for u in myusers:
               comrate = u.userwallet.commission_rate * 100 
               u.comrate = comrate
               if u.useraccount.user_agent == request.user:
                    users.append(u)
          context={
               'comrates':curcommis,
               'mycommi':request.user,
               'page':'ACTIVE AGENT',
               'users':list(users)
          }
          return render(request,'ugs_app/homepage/active_agent.html',context)
     else:
          return redirect(reverse('homepage'))
     

@login_required(login_url='/')
def active_player(request):
     ccommi=UserWallet.objects.get(user=request.user.id)
     curcommis = ccommi.commission_rate*100
     usertype_ss = request.session.get('usertype')
     if usertype_ss != 'PLAYER':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(useraccount__usertype__in=['PLAYER'],useraccount__status='ACTIVE')
          for u in myusers:
               if u.useraccount.user_agent == request.user:
                    users.append(u)
          context={
               'comrates':curcommis,
               'mycommi':request.user,
               'page':'ACTIVE PLAYER',
               'users':list(users)
          }
          return render(request,'ugs_app/homepage/active_player.html',context)
     else:
          return redirect(reverse('homepage'))
     
     



@csrf_exempt
def upplyrstat(request):
     aid=request.POST.get('acct_id')
     astat=request.POST.get('plstatus')
     comirate=request.POST.get('commirate')
     commi=request.POST.get('commission')
     agentid=request.POST.get('agentid')
     usertype=request.POST.get('usertype')

     acommi=UserWallet.objects.get(user=agentid)
     aurcommi = acommi.commission_rate

     if usertype == 'MASTER OPERATOR' or usertype == 'INCORPORATOR' or usertype == 'SUB ADMIN' or usertype == 'SUB OPERATOR' or usertype == 'MASTER AGENT':
          comms = Decimal(commi) / Decimal(100)
          aurcommif = Decimal(aurcommi)
          comminf = Decimal(comms)
          nwcommi = aurcommi
          print(comminf)
          if aurcommif>comminf: 
               try:
                    ucommi=UserAccount.objects.get(user=aid)
                    accounttype = ucommi.usertype
                    if accounttype == "PLAYER":
                         ucommi.usertype=usertype
                    ucommi.status=astat
                    ucommi.save()
          
                    wcommi=UserWallet.objects.get(user=aid)
                    ucommibal=wcommi.commission_rate
                    uplinecom = aurcommif-comminf

                    if ucommibal==0.00 and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom
                        
                    elif comminf>ucommibal and astat == "ACTIVE":
                         wcommi.commission_rate=comminf
                         wcommi.w_uplinecom=uplinecom
                    else:
                         nwcommi = aurcommi
                    
                    if wcommi.default_rate == 0.00:
                       wcommi.default_rate = comminf
                    wcommi.save()

                    data='ok'
               except Exception as e:
                   data='Error'
          else:
            data='Error'
     else:
          try:
             ucommi=UserAccount.objects.get(user=aid)
             ucommi.status=astat
             ucommi.save()
             nwcommi = aurcommi
             data='ok'
          except Exception as e:
           data='Error'
     
     return JsonResponse({'data':data, 'nwcommi':nwcommi})
# updated agent commission rate 100924









@login_required(login_url='/')
def load_new_user(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(
          useraccount__usertype__in=[
               'MASTER OPERATOR', 
               'INCORPORATOR', 
               'SUB ADMIN', 
               'SUB OPERATOR', 
               'MASTER AGENT', 
               'PLAYER'
          ]
          ).exclude(useraccount__status='ACTIVE')
          for u in myusers:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100 
               else:
                    comrate = 0
               u.comrate = comrate 
               
               if u.useraccount.user_agent == request.user:
                    users.append(u)
          context={
               'page':'USER APPROVAL',
               'users':list(users)
          }
          html_content = render_to_string('ugs_app/homepage/import_agentUser.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))
    
@login_required(login_url='/')
def load_agent_user(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(
          useraccount__usertype__in=['MASTER OPERATOR', 'INCORPORATOR', 'SUB ADMIN', 'SUB OPERATOR', 'INCORPORATOR', 'MASTER AGENT'],useraccount__status='ACTIVE')
          for u in myusers:
               if hasattr(u, 'userwallet') and u.userwallet:
                    comrate = u.userwallet.commission_rate * 100 
               else:
                    comrate = 0
               u.comrate = comrate 

               if u.useraccount.user_agent == request.user:
                    users.append(u)
          context={
               'mycommi':request.user,
               'page':'ACTIVE AGENT',
               'users':list(users)
          }
          html_content = render_to_string('ugs_app/homepage/import_activeAgent.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))
    

@login_required(login_url='/')
def load_player_user(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount').filter(useraccount__usertype='PLAYER',useraccount__status='ACTIVE')
          for u in myusers:
               if u.useraccount.user_agent == request.user:
                    users.append(u)
          context={
               'mycommi':request.user,
               'page':'ACTIVE AGENT',
               'users':list(users)
          }
          html_content = render_to_string('ugs_app/homepage/import_activePlayer.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))
 

@login_required(login_url='/')
def load_points(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          agentPointsList = Points.objects.select_related('p_sender').all()
          context = {
               'page': 'LOAD POINTS',
               'agentPointsList': agentPointsList,
               'LoadPointsForm': LoadPointsForm(user=request.user),
               'wallet':request.user.userwallet.w_balance
          }
          return render(request, 'ugs_app/homepage/load_points.html', context)
    else:
         return redirect(reverse('homepage'))
    











# fight history
def get_fight_data(request, game_id):
    try:
        fights = Fight.objects.filter(f_game=game_id).order_by('f_number').values('f_number', 'f_winner','f_tblrows')
        fight_list = list(fights)
        return JsonResponse(fight_list, safe=False)
    except Exception as e:
        print(f"Error fetching fight data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
#    fight history







# reglahan set winner
@csrf_exempt
def setwinner(request):
    fid = request.POST.get('fight')
    winner = request.POST.get('winner')
    gameid = request.POST.get('gameid')
    try:
     #    drawfight = Fight.objects.filter(f_game=gameid, f_status='DONE').exclude(f_winner='DRAW').exclude(f_winner='CANCELLED').order_by('-f_number').first()
        gfight    = Fight.objects.filter(f_game=gameid, f_status='DONE').order_by('-f_number').first()
        fightnum  = Fight.objects.filter(f_game=gameid).order_by('-f_number').first()
        if gfight:
            fnumber = gfight.f_number
            prevWinner = gfight.f_winner
            prevColumn = gfight.f_tblrows
            currentfnum = fightnum.f_number
          #   prevDrawWin  = drawfight.f_winner

            game = Games.objects.get(g_id=gameid)
            gamecol = game.g_col
            
            colhistory = prevColumn
            colControl = gamecol
            
            # update plus 5 new column
            if colhistory >= colControl:
                newColControl = colControl + 5
            else:
                newColControl = colControl

            ngame = Games.objects.get(g_id=gameid)
            ngame.g_col=newColControl
            ngame.save()
            # update plus 5 new column
          
            print(f"Fight Number {fnumber}")
            print(f"Prev Winner {prevWinner}")
          #   print(f"Prec Draw {prevDrawWin}")
            print(f"colhistory {colhistory}")
            print(f"colControl {colControl}")

            if currentfnum > 1:
               if winner == 'MERON' or winner == 'WALA':
                    if winner == 'MERON' and prevWinner == winner  or winner == 'WALA' and prevWinner == winner:
                         newColHistory = colhistory + 1
                         print('MW-1')
                    elif prevWinner == winner and  colhistory == colControl:
                         newColHistory = colhistory + 1
                         print('MW-3')
                    elif prevWinner != winner and  colhistory == colControl:
                         newColHistory = colhistory + 5
                         print('MW-4')
                    elif prevWinner != winner and  colhistory != colControl:
                         manipulate = newColControl-colhistory
                         newColHistory = manipulate + colhistory
                         print('MW-5')
                    else:
                         manipulate = newColControl-colhistory
                         newColHistory = manipulate + colhistory
                         print('MW-6')
               elif winner == 'DRAW' or winner == 'CANCELLED':
                    if winner == 'DRAW' and prevWinner == winner  or winner == 'CANCELLED' and prevWinner == winner:
                         newColHistory = colhistory + 1
                         print('MW-1')
                    elif prevWinner == winner and  colhistory == colControl:
                         newColHistory = colhistory + 1
                         print('MW-3')
                    elif prevWinner != winner and  colhistory == colControl:
                         newColHistory = colhistory + 5
                         print('MW-4')
                    elif prevWinner != winner and  colhistory != colControl:
                         manipulate = newColControl-colhistory
                         newColHistory = manipulate + colhistory
                         print('MW-5')
                    else:
                         manipulate = newColControl-colhistory
                         newColHistory = manipulate + colhistory
                         print('MW-6')
            else:
                newColHistory = 1
                print('7')


            print(f"newColHistory {newColHistory}")
            gfight = Fight.objects.get(f_id=fid)
            gfight.f_winner = winner
            gfight.f_status='DECLARED'
            gfight.f_tblrows=newColHistory
            gfight.save() 
            data = 'ok'
        else:
          gfights = Fight.objects.get(f_id=fid)
          gfights.f_winner = winner
          gfights.f_status='DECLARED'
          gfights.f_tblrows=1
          gfights.save() 
          
          data = 'ok'
    except Exception as e:
        print(e)
        data = 'bad'    
    return JsonResponse({'data': data})






@csrf_exempt
def setlongwin(request):
    fid = request.POST.get('fight')
    winner = request.POST.get('winner')
    gameid = request.POST.get('gameid')
    fightnum = int(request.POST.get('fightnum', 0))

    try:
        longwinner = Longestfight.objects.filter(
            l_status='WAITING', 
            l_category='LONGEST'
        ).aggregate(total=Sum('l_amount'))['total'] or 0

        countlong = Longestfight.objects.filter(
            l_status='WAITING', 
            l_category='LONGEST'
        ).aggregate(total=Count('id'))['total'] or 0

        if longwinner > 0 and countlong > 0:
            longDivide = longwinner / countlong
            lbets = Longestfight.objects.filter(
                l_won_amnt=0, 
                l_status='WAITING',
                l_fightno__lte=fightnum
            )

            if not lbets.exists():
                raise ValueError("No bets found for this fight")

            with transaction.atomic():
                for lbet in lbets:
                    if longDivide > 0:
                        try:
                            clwallet = UserWallet.objects.get(user=lbet.l_player.id)
                            clwallet.w_balance += longDivide
                            clwallet.w_betlong += longDivide
                            clwallet.save()

                            lbet.l_won_amnt = longDivide
                            lbet.l_status = 'CLAIMED'
                            lbet.l_waltotal=clwallet.w_balance
                            lbet.save()
                            data = 'ok'
                   
                        except UserWallet.DoesNotExist:
                            data = 'bad'
                          
                    else:
                        data = 'bad'
        else:
            data = 'bad'
    except Exception as e:
        data = 'bad'

    return JsonResponse({'data': data})


@login_required(login_url='/')
def adstaking(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
          adstakelist = Stakefund.objects.all().order_by('-s_id')
          users=UserProfile.objects.all().order_by('-date_joined').exclude(useraccount__usertype='DECLARATOR').exclude(useraccount__usertype='SUPER ADMIN').exclude(useraccount__usertype='ADMIN')
     
          try:
               stkactive = UserWallet.objects.all().aggregate(total=Sum('w_stake_active'))['total']
               if stkactive is None:
                    stkactive = 0
          except Exception as e:
               stkactive = 0

          try:
               stkcomm = UserWallet.objects.all().aggregate(total=Sum('w_stakecom'))['total']
               if stkcomm is None:
                    stkcomm = 0
          except Exception as e:
               stkcomm = 0

          try:
               stkwithdraw = UserWallet.objects.all().aggregate(total=Sum('w_stake_out'))['total']
               if stkwithdraw is None:
                    stkwithdraw = 0
          except Exception as e:
               stkwithdraw = 0

          try:
               stkbal = UserWallet.objects.all().aggregate(total=Sum('w_stakebal'))['total']
               stakefund = float(stkbal) + float(stkactive)
               if stakefund is None:
                    stakefund = 0
          except Exception as e:
               stakefund = 0
          
          try:
               stkcocoms = UserWallet.objects.all().aggregate(total=Sum('w_stakecom_claim'))['total']
               if stkcocoms is None:
                    stkcocoms = 0
          except Exception as e:
               stkcocoms = 0

          try:
               stkearning = UserWallet.objects.all().aggregate(total=Sum('w_stake_earning'))['total']
               if stkearning is None:
                    stkearning = 0
          except Exception as e:
               stkearning = 0

          context = {
               'page': 'LOAD STAKING',
               'adstakelist': adstakelist,
               'users':list(users),

               'stkactive': stkactive,
               'stkcomm': stkcomm,
               'stkwithdraw': stkwithdraw,
               'stakefund': stakefund,
               'stkcocoms': stkcocoms,
               'stkearning': stkearning,

          }
          return render(request, 'ugs_app/homepage/admin_staking.html', context)
    else:
          return redirect(reverse('homepage'))
    


@csrf_exempt
def loadStaking(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_stake = code_point.upper()
        stakeamnt = request.POST.get('valstakeamnt')
        user_id = request.POST.get('userId')

        try:
            stakeamnt = Decimal(stakeamnt)
        except (ValueError, TypeError):
            return JsonResponse({'data': 'error1'})

        try:
            receiver = UserProfile.objects.get(id=user_id)
            sender = UserProfile.objects.get(id=request.user.id)
        except UserProfile.DoesNotExist:
            return JsonResponse({'data': 'error2'})

        try:
            with transaction.atomic():
                stakefund = Stakefund.objects.create(
                    s_code=code_stake,
                    s_amount=stakeamnt,
                    s_user=receiver,
                    s_sender=sender
                )
                
                stkwallet = UserWallet.objects.get(user=receiver.id)
                stkwallet.w_stakebal += stakeamnt
                stkwallet.save()

            data = 'ok'
        except Exception as e:
            data = 'error'

        return JsonResponse({'data': data})

    return JsonResponse({'data': 'error3'})



@login_required(login_url='/')
def load_stake_tbl(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
          adstakelist = Stakefund.objects.all().order_by('-s_id')
          users=UserProfile.objects.all().order_by('-date_joined')
          context = {
            'page': 'staking',
            'adstakelist': adstakelist,
            'users':list(users)
        }
          html_content = render_to_string('ugs_app/homepage/load_stake_tbl.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))






@login_required(login_url='/')
def cashoutapproval(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT' or usertype_ss == 'ADMIN':
          couthwallet = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).select_related('cw_player').order_by('-cw_id')
          total_approved = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=1).aggregate(Sum('cw_out'))['cw_out__sum']
          total_declined = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=2).aggregate(Sum('cw_out'))['cw_out__sum']
          total_current = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).aggregate(Sum('cw_out'))['cw_out__sum']

          if total_approved is None:
               total_approved = 0
          if total_declined is None:
               total_declined = 0
          if total_current is None:
               total_current = 0
          context = {
               'page': 'CASHOUT APPROVAL',
               'couttransact': couthwallet,
               'total_approved': total_approved,
               'total_declined': total_declined,
               'total_current': total_current,
               }
          return render(request, 'ugs_app/homepage/cashout_approval.html', context)
    else:
       return redirect(reverse('homepage'))
    






    




@login_required(login_url='/')
def loadagentcOut(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'AGENT' or usertype_ss == 'ADMIN':
          couthwallet = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).select_related('cw_player').order_by('-cw_id')
          context = {
               'page': 'CASHOUT APPROVAL',
               'couttransact': couthwallet,
               }
          html_content = render_to_string('ugs_app/homepage/import_agentcOut.html', context)
          return HttpResponse(html_content)
     else:
        return redirect(reverse('homepage'))






# UPDATED 102024
@login_required(login_url='/')
def loadingstation(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss != 'PLAYER':
          # agentPointsList = Points.objects.filter(p_processby=request.user.id, p_receiver=request.user.id).order_by('-p_created').all()
          agentPointsList = Points.objects.filter(Q(p_sender=request.user.id) | Q(p_receiver=request.user.id)).order_by('-p_created')
          
          try:
               psent = Points.objects.filter(p_sender=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if psent is None:
                    psent = 0
          except Exception as e:
               psent = 0

          try:
               preceived = Points.objects.filter(p_receiver=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if preceived is None:
                    preceived = 0
          except Exception as e:
               preceived = 0

          ccommi=UserWallet.objects.get(user=request.user.id)
          curcommis = ccommi.commission_rate*100
          pointbal = float(preceived) - float(psent)

          print(curcommis)
          context = {
               'page': 'LOADING STATION',
               'agentPointsList': agentPointsList,
               'comrates':curcommis,
               'wallet':request.user.userwallet.w_balance,

               'pointbal':pointbal,
               'psent':psent,
               'preceived':preceived,
          }
          return render(request, 'ugs_app/homepage/loading_station.html', context)
     else:
          return redirect(reverse('homepage'))
# UPDATED 102024


@login_required(login_url='/')
def transactions(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'PLAYER':
          agentPointsList = Points.objects.filter(Q(p_sender=request.user.id) | Q(p_receiver=request.user.id)).order_by('-p_created')
          
          try:
               psent = Points.objects.filter(p_sender=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if psent is None:
                    psent = 0
          except Exception as e:
               psent = 0

          try:
               preceived = Points.objects.filter(p_receiver=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if preceived is None:
                    preceived = 0
          except Exception as e:
               preceived = 0

          try:
               aggregates = Bet.objects.filter(player=request.user.id).exclude(winStat='3').exclude(winStat='4').aggregate(betamount=Sum('amount'))
               betamount = aggregates.get('betamount') or 0
          except Exception as e:
               betamount = 0
          
          try:
               aggregates = Bet.objects.filter(player=request.user.id).aggregate(betwon=Sum('won_amnt'))
               betwon = aggregates.get('betwon') or 0
          except Exception as e:
               betwon = 0

          ccommi=UserWallet.objects.get(user=request.user.id)
          curcommis = ccommi.commission_rate*100
          pointbal = float(preceived) - float(psent)

          print(curcommis)
          context = {
               'page': 'POINTS TRNSACTIONS',
               'agentPointsList': agentPointsList,
               'comrates':curcommis,
               'wallet':request.user.userwallet.w_balance,

               'pointbal':pointbal,
               'psent':psent,
               'preceived':preceived,
               'betamount':betamount,
               'betwon':betwon,
          }
          return render(request, 'ugs_app/homepage/player_transactions.html', context)
     else:
          return redirect(reverse('homepage'))





# UPDATED 102024
@csrf_exempt
def pointsTransaction(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss in ['MASTER OPERATOR', 'INCORPORATOR', 'SUB ADMIN', 'SUB OPERATOR', 'MASTER AGENT', 'ADMIN']:
        if request.method == 'POST':
            transacval = request.POST.get('transacval')
            agent_id = request.user.id
            users = []

            try:
                if transacval == "DEPOSIT":
                    uwallet=UserWallet.objects.get(user=agent_id)
                    walletbal = uwallet.w_balance
                    agent_us  = request.user.username
                    myusers = UserProfile.objects.select_related('useraccount').filter(useraccount__status='ACTIVE')
                    for u in myusers:
                        if u.useraccount.user_agent == request.user:
                            users.append(u)
                            
                elif transacval == "WITHDRAW":
                    walletbal = 0.00
                    agent_us  = ""
                    myusers = UserProfile.objects.select_related('useraccount').filter(useraccount__status='ACTIVE')
                    for u in myusers:
                        if u.useraccount.user_agent == request.user:
                            users.append(u)

                context = {
                    'mycommi': request.user,
                    'page': 'WALLET',
                    'transtype': transacval,
                    'uwallet': walletbal,
                    'agent_us': agent_us,
                    'users': list(users)
                    
                }
                html_content = render_to_string('ugs_app/homepage/pointsTransactions.html', context)
                return HttpResponse(html_content)

            except UserProfile.DoesNotExist:
                return HttpResponse("User not found", status=404)
    else:
        return redirect(reverse('homepage'))
    






@csrf_exempt
def withdrawal_accnt(request):
    if request.method == 'POST':
          acntid = request.POST.get('withdrawacnt')
          transtype = request.POST.get('transtype')
          agent_id = request.user.id

          if transtype == "DEPOSIT":
               try:
                    uwallet=UserWallet.objects.get(user=agent_id)
                    walletbal = uwallet.w_balance
                    if walletbal>0:
                         walletbal = walletbal
                    else:
                         walletbal = 0
               except Exception as e:
                    walletbal = 0
               
          elif transtype == "WITHDRAW":
               try:
                    uwallet=UserWallet.objects.get(user=acntid)
                    walletbal = uwallet.w_balance
                    if walletbal>0:
                         walletbal = walletbal
                    else:
                         walletbal = 0
               except Exception as e:
                    walletbal = 0
          else:
               walletbal = 0
    return JsonResponse({'walletbal': walletbal})

















@csrf_exempt
def points_transactions(request):
    if request.method == 'POST':
          try:
             with transaction.atomic():
               code_point = get_random_string(6)
               code_points = code_point.upper()

               userid = request.POST.get('userid')
               load_point = request.POST.get('load_point')
               transtype = request.POST.get('transtype')
               
               newBalance = 0.00
               newtotalout = 0.00
               data = 'bad'
               status = "invalid" 

               if transtype == "DEPOSIT":
                    accounId = request.user
               elif transtype =="WITHDRAW":
                    accounId = userid

               try:
                    uwallet=UserWallet.objects.get(user=accounId)
                    walletbal = uwallet.w_balance
                    totalpoint = uwallet.w_points
                    if walletbal>=1:
                         walletbal = walletbal
                    else:
                         walletbal = 0
               except UserWallet.DoesNotExist:
                    walletbal = 0
                    totalpoint = 0
               
               walletbal = float(walletbal)
               point_amount = float(load_point)
               if walletbal >=1:
                    if point_amount>=1 and walletbal>=point_amount:
                         try:
                              transPoints = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').first()
                              if transPoints:
                                   lastdate = transPoints.p_created
                              else:
                                   lastdate = 'NotExist'
                         except UserWallet.DoesNotExist:
                                   lastdate = 'NotExist'
                         print(lastdate)
                         if lastdate !='NotExist':
                              if lastdate.tzinfo is None:
                                   date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                              else:
                                   date1 = lastdate
                                   date2 = timezone.now()
                                   time_difference = date2 - date1
                                   difference_in_seconds = time_difference.total_seconds()
                                   if difference_in_seconds > 3:
                                        status = "valid"
                                   else:
                                        status = "invalid"
                         else:
                              status = "valid"
                         



                         if  status == "valid":
                              if transtype == "DEPOSIT":
                                   # RECEIVER WALLET DEPOSIT UPDATE
                                   try:
                                        receiver=UserProfile.objects.get(id=request.POST.get('userid'))
                                        upwallet=UserWallet.objects.get(user=userid)
                                        curbalance=upwallet.w_balance
                                        pointbal=upwallet.w_points
                                        newbal=float(curbalance) + float(point_amount)
                                        newpoint=float(pointbal) + float(point_amount) 
                                        upwallet.w_balance=newbal
                                        upwallet.w_points=newpoint
                                        upwallet.save()
                                        data='success'
                                   except Exception as e:
                                        data='error'
                                   # RECEIVER WALLET DEPOSIT UPDATE

                                   # SENDER WALLET DEPOSIT UPDATE
                                   try:
                                        apwallet=UserWallet.objects.get(user=request.user)
                                        acurbalance=apwallet.w_balance
                                        anewbal=float(acurbalance) - float(point_amount)
                                        apwallet.w_balance=anewbal
                                        apwallet.save() 
                                        data='success'
                                   except Exception as e:
                                        data='error'
                                   # SENDER WALLET DEPOSIT UPDATE

                                   # SAVE POINTS DEPOSIT HISTORY
                                   savePoints=Points(
                                        p_receiver=receiver,
                                        p_sender=request.user,
                                        p_code=code_points,
                                        p_amount=point_amount,
                                        p_transtype=transtype,
                                        p_processby=request.user.id,
                                        p_balance=newbal,
                                        p_agentbal=anewbal
                                        ).save()
                                   if savePoints:
                                        data='success'
                                   # SAVE POINTS DEPOSIT HISTORY
                                   newBalance = walletbal = apwallet.w_balance






                              elif transtype =="WITHDRAW":
                                   # SENDER WALLET WITHDRAW UPDATE
                                   try:
                                        receiver=UserProfile.objects.get(id=request.POST.get('userid'))
                                        upwallet=UserWallet.objects.get(user=userid)
                                        curbalance=upwallet.w_balance
                                        coutbal=upwallet.wallet_out

                                        newbal=float(curbalance) - float(point_amount)
                                        newpoint=float(coutbal) + float(point_amount) 
                                        upwallet.w_balance=newbal
                                        upwallet.wallet_out=newpoint
                                        upwallet.save()
                                        data='success'
                                   except Exception as e:
                                        data='error'
                                   # SENDER WALLET WITHDRAW UPDATE
                                   # RECEIVER WALLET WITHDRAW UPDATE
                                   try:
                                        apwallet=UserWallet.objects.get(user=request.user)
                                        acurbalance=apwallet.w_balance
                                        apointbal=apwallet.w_points

                                        anewbal=float(acurbalance) + float(point_amount)
                                        anewpoint=float(apointbal) + float(point_amount)

                                        apwallet.w_balance=anewbal
                                        apwallet.w_points=anewpoint
                                        apwallet.save() 
                                        data='success'
                                   except Exception as e:
                                        data='error'
                                   # RECEIVER WALLET WITHDRAW UPDATE
                                   # SAVE POINTS DEPOSIT HISTORY
                                   savePoints=Points(
                                        p_receiver=request.user,
                                        p_sender=receiver,
                                        p_code=code_points,
                                        p_amount=point_amount,
                                        p_transtype=transtype,
                                        p_processby=request.user.id,
                                        p_balance=anewbal,
                                        p_agentbal=newbal
                                        ).save()
                                   if savePoints:
                                        data='success'
                                   # SAVE POINTS DEPOSIT HISTORY
                                   newBalance = walletbal = apwallet.w_balance

                         else:
                              newBalance = walletbal
                              newtotalout = totalpoint
                              data = 'tryagain'


                    else:
                         newBalance = walletbal
                         newtotalout = totalpoint
                         data = 'invalid'
               else:
                    newBalance = walletbal
                    newtotalout = totalpoint
                    data = 'insufficient'
          except Exception as e:
               print(e)
               data='Error'   
          return JsonResponse({'data': data, 'newPoints':newBalance, 'newtotalout':newtotalout})  


@login_required(login_url='/')
def load_points_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          agentPointsList = Points.objects.filter(Q(p_sender=request.user.id) | Q(p_receiver=request.user.id)).order_by('-p_created')
          context = {
               'user': request.user, 
               'page': 'WALLET',
               'agentPointsList': agentPointsList,
          }
          html_content = render_to_string('ugs_app/homepage/import_agentPoints_tbl.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))
# UPDATED 102024













@login_required(login_url='/')
def adloadingstation(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN':
          agentPointsList = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').all()

          try:
               psent = Points.objects.filter(p_sender=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if psent is None:
                    psent = 0
          except Exception as e:
               psent = 0

          try:
               preceived = Points.objects.filter(p_receiver=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if preceived is None:
                    preceived = 0
          except Exception as e:
               preceived = 0

          ccommi=UserWallet.objects.get(user=request.user.id)
          curcommis = ccommi.commission_rate*100
          pointbal = float(preceived) - float(psent)


          context = {
               'page': 'LOADING STATION',
               'agentPointsList': agentPointsList,
               'wallet':request.user.userwallet.w_balance,
               
               'comrates':curcommis,
               'pointbal':pointbal,
               'psent':psent,
               'preceived':preceived,

          }
          return render(request, 'ugs_app/homepage/admin_loading_station.html', context)
     else:
          return redirect(reverse('homepage'))
     



@login_required(login_url='/')
def sadminPoint(request):
     usertype_ss = request.user.useraccount.usertype
     if usertype_ss == 'SUPER ADMIN':
          agentPointsList = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').all()
          users=UserProfile.objects.all().filter(useraccount__usertype='ADMIN')
          try:
               psent = Points.objects.filter(p_sender=request.user.id).aggregate(total=Sum('p_amount'))['total']
               if psent is None:
                    psent = 0
          except Exception as e:
               psent = 0

          context = {
               'page': 'LOADING POINTS',
               'agentPointsList': agentPointsList,               
               'psent':psent,
               'users': list(users)
          }
          return render(request, 'ugs_app/homepage/spadmin_loading.html', context)
     else:
          return redirect(reverse('homepage'))
     

@login_required(login_url='/')
def import_spadload(request):
    usertype_ss = request.user.useraccount.usertype
    if usertype_ss == 'SUPER ADMIN':
          
          agentPointsList = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').all()
          context = {
               'page': 'WALLET',
               'agentPointsList': agentPointsList,
          }
          html_content = render_to_string('ugs_app/homepage/imprt_spadpoint.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))

@csrf_exempt
def spadminloading(request):
    if request.method == 'POST':
          code_point = get_random_string(6)
          code_points = code_point.upper()

          userid = request.POST.get('userid')
          load_point = request.POST.get('load_point')
          transtype = request.POST.get('transtype')
          
          newBalance = 0.00
          newtotalout = 0.00
          data = 'bad'
          status = "invalid" 
          walletbal = 1
          totalpoint = 1

          walletbal = float(walletbal)
          point_amount = float(load_point)
          if walletbal >0:
               if point_amount>0:
                    try:
                         transPoints = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').first()
                         if transPoints:
                              lastdate = transPoints.p_created
                         else:
                              lastdate = 'NotExist'
                    except UserWallet.DoesNotExist:
                              lastdate = 'NotExist'

                    if lastdate !='NotExist':
                         if lastdate.tzinfo is None:
                              date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                         else:
                              date1 = lastdate
                              date2 = timezone.now()
                              time_difference = date2 - date1
                              difference_in_seconds = time_difference.total_seconds()
                              if difference_in_seconds > 3:
                                   status = "valid"
                              else:
                                   status = "invalid"
                    else:
                         status = "valid"
                    
                    if  status == "valid":
                         if transtype == "DEPOSIT":
                              # RECEIVER WALLET DEPOSIT UPDATE
                              try:
                                   receiver=UserProfile.objects.get(id=request.POST.get('userid'))
                                   upwallet=UserWallet.objects.get(user=userid)
                                   curbalance=upwallet.w_balance
                                   pointbal=upwallet.w_points

                                   newbal=float(curbalance) + float(point_amount)
                                   newpoint=float(pointbal) + float(point_amount) 
                                   upwallet.w_balance=newbal
                                   upwallet.w_points=newpoint
                                   upwallet.save()
                                   data='success'
                              except Exception as e:
                                   data='error'
                              # RECEIVER WALLET DEPOSIT UPDATE
                              
                              # SAVE POINTS DEPOSIT HISTORY
                              savePoints=Points(
                                   p_receiver=receiver,
                                   p_sender=request.user,
                                   p_code=code_points,
                                   p_amount=point_amount,
                                   p_transtype=transtype,
                                   p_processby=request.user.id,
                                   p_balance=0.00
                                   ).save()
                              if savePoints:
                                   data='success'
                              # SAVE POINTS DEPOSIT HISTORY
                              newBalance = 1
                    else:
                         newBalance = walletbal
                         newtotalout = totalpoint
                         data = 'tryagain'


               else:
                    newBalance = walletbal
                    newtotalout = totalpoint
                    data = 'invalid'
          else:
               newBalance = walletbal
               newtotalout = totalpoint
               data = 'insufficient'
          return JsonResponse({'data': data, 'newPoints':newBalance, 'newtotalout':newtotalout})
    








     





@csrf_exempt
def adpointsTransaction(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss in ['ADMIN']:
        if request.method == 'POST':
            transacval = request.POST.get('transacval')
            agent_id = request.user.id
            users = []

            try:
                if transacval == "DEPOSIT":
                    uwallet=UserWallet.objects.get(user=agent_id)
                    walletbal = uwallet.w_balance
                    agent_us  = request.user.username
                    users=UserProfile.objects.all().order_by('-date_joined').exclude(useraccount__usertype='DECLARATOR').exclude(useraccount__usertype='SUPER ADMIN').exclude(useraccount__usertype='ADMIN')
                    
                            
                elif transacval == "WITHDRAW":
                    walletbal = 0.00
                    agent_us  = ""
                    users=UserProfile.objects.all().order_by('-date_joined').exclude(useraccount__usertype='DECLARATOR').exclude(useraccount__usertype='SUPER ADMIN').exclude(useraccount__usertype='ADMIN')
                context = {
                    'mycommi': request.user,
                    'page': 'WALLET',
                    'transtype': transacval,
                    'uwallet': walletbal,
                    'agent_us': agent_us,
                    'users': list(users)
                    
                }
                html_content = render_to_string('ugs_app/homepage/admin_points_trans.html', context)
                return HttpResponse(html_content)

            except UserProfile.DoesNotExist:
                return HttpResponse("User not found", status=404)
    else:
        return redirect(reverse('homepage'))


@csrf_exempt
def adwithdrawal_accnt(request):
    if request.method == 'POST':
          acntid = request.POST.get('withdrawacnt')
          transtype = request.POST.get('transtype')
          agent_id = request.user.id

          if transtype == "DEPOSIT":
               try:
                    uwallet=UserWallet.objects.get(user=agent_id)
                    walletbal = uwallet.w_balance
                    if walletbal>0:
                         walletbal = walletbal
                    else:
                         walletbal = 0
               except Exception as e:
                    walletbal = 0
               
          elif transtype == "WITHDRAW":
               try:
                    uwallet=UserWallet.objects.get(user=acntid)
                    walletbal = uwallet.w_balance
                    if walletbal>0:
                         walletbal = walletbal
                    else:
                         walletbal = 0
               except Exception as e:
                    walletbal = 0
          else:
               walletbal = 0
    return JsonResponse({'walletbal': walletbal})












@csrf_exempt
def adpoints_transactions(request):
    if request.method == 'POST':
          code_point = get_random_string(6)
          code_points = code_point.upper()

          userid = request.POST.get('userid')
          load_point = request.POST.get('load_point')
          transtype = request.POST.get('transtype')
          
          newBalance = 0.00
          newtotalout = 0.00
          data = 'bad'
          status = "invalid" 

          if transtype == "DEPOSIT":
               accounId = request.user
          elif transtype =="WITHDRAW":
               accounId = userid

          try:
               uwallet=UserWallet.objects.get(user=accounId)
               walletbal = uwallet.w_balance
               totalpoint = uwallet.w_points
               if walletbal>=1:
                    walletbal = walletbal
               else:
                    walletbal = 0
          except UserWallet.DoesNotExist:
               walletbal = 0
               totalpoint = 0
             
          walletbal = float(walletbal)
          point_amount = float(load_point)
          if walletbal >=1:
               if point_amount>=1 and walletbal>=point_amount:
                    try:
                         transPoints = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').first()
                         if transPoints:
                              lastdate = transPoints.p_created
                         else:
                              lastdate = 'NotExist'
                    except UserWallet.DoesNotExist:
                              lastdate = 'NotExist'

                    if lastdate !='NotExist':
                         if lastdate.tzinfo is None:
                              date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                         else:
                              date1 = lastdate
                              date2 = timezone.now()
                              time_difference = date2 - date1
                              difference_in_seconds = time_difference.total_seconds()
                              if difference_in_seconds > 3:
                                   status = "valid"
                              else:
                                   status = "invalid"
                    else:
                         status = "valid"
                    



                    if  status == "valid":
                         if transtype == "DEPOSIT":
                              # RECEIVER WALLET DEPOSIT UPDATE
                              try:
                                   receiver=UserProfile.objects.get(id=request.POST.get('userid'))
                                   upwallet=UserWallet.objects.get(user=userid)
                                   curbalance=upwallet.w_balance
                                   pointbal=upwallet.w_points

                                   newbal=float(curbalance) + float(point_amount)
                                   newpoint=float(pointbal) + float(point_amount) 
                                   upwallet.w_balance=newbal
                                   upwallet.w_points=newpoint
                                   upwallet.save()
                                   data='success'
                              except Exception as e:
                                   data='error'
                              # RECEIVER WALLET DEPOSIT UPDATE
                              # SENDER WALLET DEPOSIT UPDATE
                              try:
                                   apwallet=UserWallet.objects.get(user=request.user)
                                   acurbalance=apwallet.w_balance
                                   anewbal=float(acurbalance) - float(point_amount)
                                   apwallet.w_balance=anewbal
                                   apwallet.save() 
                                   data='success'
                              except Exception as e:
                                   data='error'
                              # SENDER WALLET DEPOSIT UPDATE
                              # SAVE POINTS DEPOSIT HISTORY
                              savePoints=Points(
                                   p_receiver=receiver,
                                   p_sender=request.user,
                                   p_code=code_points,
                                   p_amount=point_amount,
                                   p_transtype=transtype,
                                   p_processby=request.user.id,
                                   p_balance=newbal,
                                   p_agentbal=anewbal
                                   ).save()
                              if savePoints:
                                   data='success'
                              # SAVE POINTS DEPOSIT HISTORY
                              newBalance = walletbal = apwallet.w_balance






                         elif transtype =="WITHDRAW":
                              # SENDER WALLET WITHDRAW UPDATE
                              try:
                                   receiver=UserProfile.objects.get(id=request.POST.get('userid'))
                                   upwallet=UserWallet.objects.get(user=userid)
                                   curbalance=upwallet.w_balance
                                   coutbal=upwallet.wallet_out

                                   newbal=float(curbalance) - float(point_amount)
                                   newpoint=float(coutbal) + float(point_amount) 
                                   upwallet.w_balance=newbal
                                   upwallet.wallet_out=newpoint
                                   upwallet.save()
                                   data='success'
                              except Exception as e:
                                   data='error'
                              # SENDER WALLET WITHDRAW UPDATE
                              # RECEIVER WALLET WITHDRAW UPDATE
                              try:
                                   apwallet=UserWallet.objects.get(user=request.user)
                                   acurbalance=apwallet.w_balance
                                   apointbal=apwallet.w_points
                                   anewbal=float(acurbalance) + float(point_amount)
                                   anewpoint=float(apointbal) + float(point_amount)

                                   apwallet.w_balance=anewbal
                                   apwallet.w_points=anewpoint
                                   apwallet.save() 
                                   data='success'
                              except Exception as e:
                                   data='error'
                              # RECEIVER WALLET WITHDRAW UPDATE
                              # SAVE POINTS DEPOSIT HISTORY
                              savePoints=Points(
                                   p_receiver=request.user,
                                   p_sender=receiver,
                                   p_code=code_points,
                                   p_amount=point_amount,
                                   p_transtype=transtype,
                                   p_processby=request.user.id,
                                   p_balance=anewbal,
                                   p_agentbal=newbal
                                   ).save()
                              if savePoints:
                                   data='success'
                              # SAVE POINTS DEPOSIT HISTORY
                              newBalance = walletbal = apwallet.w_balance

                    else:
                         newBalance = walletbal
                         newtotalout = totalpoint
                         data = 'tryagain'


               else:
                    newBalance = walletbal
                    newtotalout = totalpoint
                    data = 'invalid'
          else:
               newBalance = walletbal
               newtotalout = totalpoint
               data = 'insufficient'
          return JsonResponse({'data': data, 'newPoints':newBalance, 'newtotalout':newtotalout})
    

@login_required(login_url='/')
def adload_points_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
          
          agentPointsList = Points.objects.filter(p_processby=request.user.id).order_by('-p_created').all()
          context = {
               'user': request.user,
               'page': 'WALLET',
               'agentPointsList': agentPointsList,
          }
          html_content = render_to_string('ugs_app/homepage/imprt_adpointstrans.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))


















# MANUAL GETTING DATA PLAYER
def betdata(request, game_id):
     fstatus=''
     fid=''
     meron=0
     wala=0
     fnum=0
     mymeronbet=0
     mywalabet=0
     mydrawbet=0
     mylongbet=0
     reglastat=0
     meronpayout=0
     walapayout=0
     walatowin=0
     merontowin=0

     try:
          gfight  = Fight.objects.filter(f_game=game_id).order_by('-f_number').first()
          tblrows = gfight.f_tblrows
          fstatus = gfight.f_status
          frevert = gfight.f_revert
          # if tblrows>0 and fstatus == "DECLARED" or frevert !== Null:
          if (tblrows > 0 and fstatus == "DECLARED") or frevert is not None:
               reglastat=1
          else:
               reglastat=0 
     except Exception as e:
          reglastat=0

     try:
          g_arena=Games.objects.get(g_id=game_id)
          gname=g_arena.g_name
          gid=g_arena.g_id
          meron_name=g_arena.g_redname
          wala_name=g_arena.g_bluename
          video=g_arena.g_link

          try:
             cgame=Games.objects.get(g_id=game_id)
             plasada=cgame.g_plasada
          except Exception as e:
             plasada=0

          try:
               g_fight=Fight.objects.filter(f_game=g_arena).latest('f_created')
               fid=g_fight.f_id
               status=g_fight.f_status
               fnum=g_fight.f_number
               fmulti=g_fight.f_multiplier
               fwin=g_fight.f_winner
               flong=g_fight.f_longest
               try:
                    mymeronbet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='MERON',player=request.user).aggregate(total=Sum('amount'))['total']
                    if mymeronbet is None:
                         mymeronbet=0
               except Exception as e:
                    mymeronbet=0
               try:
                    mywalabet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='WALA',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    if mywalabet is None:
                         mywalabet=0
               except Exception as e:
                    mywalabet=0
               try:
                    mydrawbet=Bet.objects.filter(fight=g_fight,eventid=game_id,status='PENDING',category='DRAW',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    if mydrawbet is None:
                         mydrawbet=0
               except Exception as e:
                    mydrawbet=0
               try:
                    mylongbet=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST',l_player=request.user).aggregate(total=Sum('l_amount'))['total'] 
                    if mylongbet is None:
                         mylongbet=0
               except Exception as e:
                    mylongbet=0
               try:
                    meron=Bet.objects.filter(fight=fid,eventid=game_id,category='MERON').aggregate(total=Sum('amount'))['total']
                    if meron is None:
                         meron=0
               except Exception as e:
                    meron=0
               try:
                    wala=Bet.objects.filter(fight=fid,eventid=game_id,category='WALA').aggregate(total=Sum('amount'))['total'] 
                    if wala is None:
                         wala=0
               except Exception as e:
                    wala=0

               totmw=meron + wala

               # PLASADA
               totpla=float(plasada) * float(totmw) 
               
               lesspla=totmw - totpla

               if meron > 0:    
                         meronlesspla=lesspla/meron
               else:
                    meronlesspla=lesspla
               
               if wala > 0:    
                         walalesspla=lesspla/wala
                         walapayout=walalesspla * 100
               else:
                    walalesspla=lesspla
               
               walapayout=walalesspla * 100
               meronpayout=meronlesspla * 100
               
               # odds
               meronodds=meronpayout * .01
               walaodds=walapayout * .01
               
               # topay=odds*player bet
               merontowin=meronodds * mymeronbet
               walatowin=walaodds * mywalabet

               # player dummy total bet
               dmeron=fmulti*meron
               dwala=fmulti*wala
               
          except Exception as e:
               status='CLOSED'
               fnum=0
               fmulti=0
               fwin=0
               flong=0
               fid=0
     except Exception as e:
          print(e)

     dmeron=float(meron)*float(fmulti)
     dwala=float(wala)*float(fmulti)
     wallet=UserWallet.objects.get(user=request.user)
     wbalance=wallet.w_balance
     data={
          'page':'ARENA',
          'game':game_id,
          'game_name':gname,
          'betstat':status,
          'fight_id':fid,
          'fnumber':fnum,
          'mybetmeron':mymeronbet,
          'myWalaBet':mywalabet,
          'mydrawbet':mydrawbet,
          'mylongbet':mylongbet,
          'dmeron':dmeron,
          'dwala':dwala,
          'nmeron':meron_name,
          'nwala':wala_name,
          'video':video,
          'fwin':fwin,
          'meronpayout':meronpayout,
          'merontowin':merontowin,
          'walapayout':walapayout,
          'walatowin':walatowin,
          'myWalaBet':mywalabet,
          'mywallet':int(wbalance),
          'reglastat':reglastat
     }
     return JsonResponse(data)
     # PLAYER MANUAL GETTING DATA 






# DECLA GETTING DATA MANUALLY
def decladata(request, game_room):
     user=request.user.id
     wbalance=0
     try:
          cgame=Games.objects.get(g_id=game_room)
          plasada=cgame.g_plasada
     except Exception as e:
          plasada=0
          
     try:
          gf=Fight.objects.filter(f_game=game_room).latest('f_created')
          fid=gf.f_id
          fmulti=gf.f_multiplier
          status=gf.f_status
          game_num=gf.f_number
          winner=gf.f_winner
     except Exception as e:
          fid=0
          status=''
          game_num=0
          fmulti=0
          winner=''

     try:
         meron=Bet.objects.filter(fight=fid,category='MERON').aggregate(total=Sum('amount'))['total']
         if meron is None:
            meron=0
     except Exception as e:
          meron=0
    
     try:
          wala=Bet.objects.filter(fight=fid,category='WALA').aggregate(total=Sum('amount'))['total'] 
          if wala is None:
              wala=0
     except Exception as e:
          wala=0
     
     try:
          draw=Bet.objects.filter(fight=fid,category='DRAW').aggregate(total=Sum('amount'))['total'] 
          longest=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST').aggregate(total=Sum('l_amount'))['total']
          if draw is None:
               draw=0
          if longest is None: 
               longest=0
     except Exception as e:
          draw=0
          longest=0

     try:
          mymeronbet=Bet.objects.filter(fight=fid,status='PENDING',category='MERON').aggregate(total=Sum('amount'))['total']
          if mymeronbet is None:
              mymeronbet=0
     except Exception as e:
        mymeronbet=0

     try:
          mywalabet=Bet.objects.filter(fight=fid,status='PENDING',category='WALA').aggregate(total=Sum('amount'))['total'] 
          if mywalabet is None:
              mywalabet=0
     except Exception as e:
          mywalabet=0

     try:
          mydrawbet=Bet.objects.filter(fight=fid,status='PENDING',category='DRAW').aggregate(total=Sum('amount'))['total'] 
          if mydrawbet is None:
              mydrawbet=0
     except Exception as e:
          mydrawbet=0
        
     try:
          mylongbet=Longestfight.objects.filter(l_status='PENDING',l_category='LONGEST').aggregate(total=Sum('l_amount'))['total'] 
          if mylongbet is None:
             mylongbet=0
     except Exception as e:
          mylongbet=0

     totmw=meron + wala
     totpla=float(plasada) * float(totmw) 
     lesspla=totmw - totpla
     if meron > 0:    
          meronlesspla=lesspla/meron
     else:
          meronlesspla=lesspla

     if wala > 0:    
          walalesspla=lesspla/wala
          walapayout=walalesspla * 100
     else:
          walalesspla=lesspla

     walapayout=walalesspla * 100
     meronpayout=meronlesspla * 100
     # odds
     meronodds=meronpayout * .01
     walaodds=walapayout * .01
     # topay=odds*player bet
     merontowin=meronodds * mymeronbet
     walatowin=walaodds * mywalabet
     # player dummy total bet
     dmeron=fmulti*meron
     dwala=fmulti*wala

     data={
             'game_id':game_room,
              'fightnum':game_num,
              'fightid':str(fid),
              'multi':str(fmulti),
              'bet_status':status,
              'winner':winner,
              'dmeron':dmeron,
              'dwala':str(dwala),
              'meron':meron,
              'wala':wala,
              'draw':draw,
              'longest':longest,
              'myMeronBet':mymeronbet,
              'myWalaBet':mywalabet,
              'mydrawbet':mydrawbet,
              'mylongbet':mylongbet,
              'totmw':totmw,
              'totpla':totpla,
              'lesspla':lesspla,
              'meronlesspla':meronlesspla,
              'walalesspla':walalesspla,
              'meronpayout':meronpayout,
              'walapayout':walapayout,
              'meronodds':meronodds,
              'walaodss':walaodds,
              'merontowin':merontowin,
              'walatowin':walatowin,
              'mywallet':int(wbalance)

        }
     return JsonResponse(data)


@login_required(login_url='/')
def bethistory(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'PLAYER':
          current_date = datetime.now().date()
          gevents = []

          gevents=Games.objects.all().order_by('-g_created')
          bethistory = Bet.objects.filter(player=request.user.id, created__date=current_date).order_by('-id')
          context={
               'page':'BET HISTORY',
               'bethistorys': bethistory,
               'gevents': list(gevents)
          }
          return render(request,'ugs_app/homepage/betting_history.html',context)
     else:
          return redirect(reverse('homepage'))
     

############ SUBSCRIPTION

def movie_arena(request,movie):
     mv=Games.objects.get(g_id=movie)
     context={
          'page':'MOVIES',
          'movie':mv.g_name,
          'link':mv.g_link,

     }
     return render(request,'ugs_app/homepage/movie_arena.html',context)

@csrf_exempt
def chk_subscibe(request):
     mid=request.POST.get('movie')
     try:
          chk=Subcription.objects.get(s_movie=mid,s_by=request.user)
          data='ok'
     except Exception as e:
          data='bad'
          print(e)
     return JsonResponse({'data':data})

@csrf_exempt
def add_subscribe(request):

     wallet=request.user.userwallet.w_balance
     
     if float(wallet) >= float(10):
          cw=UserWallet.objects.get(user=request.user)
          cw.w_balance = float(cw.w_balance) - float(10)
          cw.save()
          movie=request.POST.get('movie')
          gmovie=Games.objects.get(g_id=movie)
          add_sub=Subcription(s_movie=gmovie,s_by=request.user).save()
          data='ok'
     else:
          data='Insufficient Balance!'
     return JsonResponse({'data':data})

#########################

@login_required(login_url='/')
def betcomms(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN' or usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          current_date = datetime.now().date()
          gevents = []
          gevents=Games.objects.all().order_by('-g_created')
          
          betcomms = Commission.objects.filter(c_agent=request.user.id, created=current_date).order_by('-c_id')
          ccommi=UserWallet.objects.get(user=request.user.id)
          curcommis = ccommi.commission_rate*100
          
          # player = UserProfile.objects.get(id=betcomms.c_player)
          # username = player.username
          context={
               'page':'BET COMMISSION',
               'betcomms': betcomms,
               'comrates':curcommis,
               'gevents': list(gevents)
          }
          return render(request,'ugs_app/homepage/betting_commis.html',context)
     else:
          return redirect(reverse('homepage'))
     









@login_required(login_url='/')
def convertcomms(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          agent_id = request.user.id
          betcomms = ConvertRewards.objects.filter(r_user=request.user.id).order_by('-r_id')
          try:
               current_date_str = datetime.now().strftime('%Y-%m-%d')
               mydailycoms = Commission.objects.filter(c_agent=request.user.id,created__date=current_date_str).aggregate(total=Sum('c_commission'))['total']
               if mydailycoms is None:
                    mydailycoms = 0
          except Exception as e:
               mydailycoms = 0

          try:
               uwallet=UserWallet.objects.get(user=agent_id)
               curcommis = uwallet.commission_rate*100
               commsbal = uwallet.w_commission
               cliambal = uwallet.comms_claimed
               newcomsbal=float(commsbal) - float(cliambal)
               if newcomsbal>0:
                    newcomsbal = newcomsbal
               else:
                    newcomsbal = 0
          except Exception as e:
               newcomsbal = 0

          context={
               'comrates':curcommis,
               'page':'CONVERT REWARDS',
               'betcomms': betcomms,
               'mydailycoms': mydailycoms,
               'newcomsbal': newcomsbal,
          }
          return render(request,'ugs_app/homepage/convert_comms.html',context)
     else:
          return redirect(reverse('homepage'))
     




@csrf_exempt
def convertProcess(request):
    if request.method == 'POST':
          code_point = get_random_string(6)
          code_points = code_point.upper()
          agent_id = request.user.id
          pointsend = request.POST.get('convertpoint')
          status = "invalid"

          try:
               uwallet=UserWallet.objects.get(user=agent_id)
               uwalbalance = uwallet.w_balance
               commsbal = uwallet.w_commission
               cliambal = uwallet.comms_claimed
               newcomsbals=float(commsbal) - float(cliambal)
               if newcomsbals>=1:
                    newcomsbals = newcomsbals
               else:
                    newcomsbals = 0
          except Exception as e:
               newcomsbals = 0
               uwalbalance = 0

          walletcomms = float(newcomsbals)
          pointsends = float(pointsend)
          newwalbal = uwalbalance
          newcomms = walletcomms
          if  pointsends>=1:
               if walletcomms>=1 and walletcomms>=pointsends:
                    try:
                         try:
                              claimcoms = ConvertRewards.objects.filter(r_user=request.user.id).order_by('-r_date').first()
                              if claimcoms:
                                   lastdate = claimcoms.r_date
                              else:
                                   lastdate = 'NotExist'
                         except UserWallet.DoesNotExist:
                                   lastdate = 'NotExist'

                         if lastdate !='NotExist':
                              if lastdate.tzinfo is None:
                                   date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                              else:
                                   date1 = lastdate
                                   date2 = timezone.now()
                                   time_difference = date2 - date1
                                   difference_in_seconds = time_difference.total_seconds()
                                   if difference_in_seconds > 3:
                                        status = "valid"
                                   else:
                                        status = "invalid"
                         else:
                              status = "valid"
                         

                         if status == "valid":
                              with transaction.atomic():
                                   awallet=UserWallet.objects.get(user=agent_id)
                                   curbalance=awallet.w_balance
                                   curcommsbal=awallet.w_comms_bal
                                   commsbal = awallet.w_commission
                                   comsclaim = awallet.comms_claimed

                                   newcalimbal=float(comsclaim) + float(pointsends) 
                                   newpoints=float(curbalance) + float(pointsends)
                                   newcomsbal=float(commsbal) - float(newcalimbal)
                                   
                                   awallet.comms_claimed=newcalimbal
                                   awallet.w_comms_bal=newcomsbal
                                   awallet.w_balance=newpoints
                                   awallet.save()

                                   receiver=UserProfile.objects.get(id=agent_id)
                                   ConvertRewards(
                                   r_code=code_points,
                                   r_amount=pointsends,
                                   r_balance=newcomsbal,
                                   r_user=receiver
                                   ).save()

                                   Points(
                                   p_receiver=receiver,
                                   p_sender=receiver,
                                   p_code=code_points,
                                   p_amount=pointsends,
                                   p_transtype='CONVERT',
                                   p_processby=request.user.id,
                                   p_balance=newpoints
                                   ).save()
                                                                      
                                   data='ok'
                                   newcomms = newcomsbal
                                   newwalbal = newpoints
                         else:
                              data = 'tryagain'
                              
                    except Exception as e:
                         print(e)
                         data='Error'
               else:
                    data='insufficient'
          else:
               data='invalid'

    return JsonResponse({'data': data,'newcomms': newcomms,'newwalbal': newwalbal})


@login_required(login_url='/')
def load_converted_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          betcomms = ConvertRewards.objects.filter(r_user=request.user.id).order_by('-r_id')
          context={
               'page':'CONVERT REWARDS',
               'betcomms': betcomms,
          }
          html_content = render_to_string('ugs_app/homepage/imprt_convertPoints.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))








@csrf_exempt
def stakerewardsWithdraw(request):
    if request.method == 'POST':
          code_point = get_random_string(6)
          code_points = code_point.upper()
          agent_id = request.user.id
          mop = request.POST.get('mop')
          acct_name = request.POST.get('acct_name')
          acct_number = request.POST.get('acct_number')
          pointsend = request.POST.get('rewardsamount')
          status = "valid"

          try:
               ucommi=UserAccount.objects.get(user=agent_id)
               withdrawal = ucommi.coutstat
          except Exception as e:
               withdrawal = 0

          try:
               uwallet=UserWallet.objects.get(user=agent_id)
               commsbal = uwallet.w_stakecom
               cliambal = uwallet.w_stakecom_claim
               newcomsbals=float(commsbal) - float(cliambal)
               if newcomsbals>=1:
                    newcomsbals = newcomsbals
               else:
                    newcomsbals = 0
          except Exception as e:
               newcomsbals = 0

          walletcomms = float(newcomsbals)
          pointsends = float(pointsend)
          newcalimedbal = cliambal
          newcomms = walletcomms
          if pointsends>=1 and withdrawal == 0:
               if walletcomms>=1 and walletcomms>=pointsends:
                    try:
                         try:
                              claimcoms = Stake_claimed_comms.objects.filter(sr_user=request.user.id).order_by('-sr_date').first()
                              if claimcoms:
                                   lastdate = claimcoms.sr_date
                              else:
                                   lastdate = 'NotExist'
                         except UserWallet.DoesNotExist:
                                   lastdate = 'NotExist'

                         if lastdate !='NotExist':
                              if lastdate.tzinfo is None:
                                   date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                              else:
                                   date1 = lastdate
                                   date2 = timezone.now()
                                   time_difference = date2 - date1
                                   difference_in_seconds = time_difference.total_seconds()
                                   if difference_in_seconds > 3:
                                        status = "valid"
                                   else:
                                        status = "invalid"
                         else:
                              status = "valid"



                         if status == "valid":
                              with transaction.atomic():
                                   awallet=UserWallet.objects.get(user=agent_id)
                                   commsbal = awallet.w_stakecom
                                   comsclaim = awallet.w_stakecom_claim

                                   newcalimbal=float(comsclaim) + float(pointsends) 
                                   newcomsbal=float(commsbal) - float(newcalimbal)
                                   
                                   receiver=UserProfile.objects.get(id=agent_id)
                                   Stake_claimed_comms(
                                   sr_code=code_points,
                                   sr_mop=mop,
                                   sr_ac_name=acct_name,
                                   sr_ac_number=acct_number,
                                   sr_amount=pointsends,
                                   sr_balance=newcomsbal,
                                   sr_user=receiver
                                   ).save()

                                   awallet.w_stakecom_claim=newcalimbal
                                   awallet.w_stakecom_bal=newcomsbal
                                   awallet.save()

                                   data='ok'
                                   newcomms = newcomsbal
                                   newcalimedbal = newcalimbal
                         else:
                              data = 'tryagain'
                    except Exception as e:
                         print(e)
                         data='Error'
               else:
                    data='insufficient'
          else:
               data='invalid'

    return JsonResponse({'data': data,'newcomms': newcomms,'newcalimbal': newcalimedbal})





























@csrf_exempt
def revertwinner(request):
     gameid=request.POST.get('gameid')
     fightNum=request.POST.get('fightNum')
     setwinner=request.POST.get('fwinner')
     data = ''
     current_date_str = datetime.now()
     try:
          with transaction.atomic():
               gfights   = Fight.objects.filter(f_number=fightNum, f_game=gameid).order_by('-f_number').first()
               fid = gfights.f_id
               fgwinner = gfights.f_winner
          
               if fgwinner != setwinner:
                    Fight.objects.filter(f_number=fightNum, f_game=gameid).update(f_winner = setwinner, f_revert=current_date_str, f_prevwin=fgwinner)
                    bets = Bet.objects.filter(fight=fid, eventid=gameid)
                    if not bets.exists():
                         data = 'notfound'

                    for bet in bets:
                         wonamount = bet.winning_amnt
                         gwallet=UserWallet.objects.get(user=bet.player.id)
                         
                         if bet.winStat == '1':
                              if gwallet.w_balance - Decimal(wonamount) >= 0:
                                   gwallet.w_balance -= Decimal(wonamount)
                                   gwallet.save()
                              elif gwallet.w_betwins - Decimal(wonamount) >= 0:
                                   gwallet.w_betwins -= Decimal(wonamount)
                                   gwallet.save()
                              else:
                                   gwallet.w_balance=0
                                   gwallet.w_betwins=0
                                   gwallet.save()

                         

                         if setwinner == 'MERON' or setwinner == 'WALA':
                              if setwinner == bet.category:
                                   print('win')
                                   if bet.winStat == '3' or bet.winStat == '4':
                                        deductrefund = bet.amount
                                        if gwallet.w_balance - Decimal(deductrefund) >= 0:
                                             gwallet.w_balance -= Decimal(deductrefund)
                                             gwallet.save()
                                        elif gwallet.w_betwins - Decimal(deductrefund) >= 0:
                                             gwallet.w_betwins -= Decimal(deductrefund)
                                             gwallet.save()
                                        else:
                                             gwallet.w_balance=0
                                             gwallet.w_betwins=0
                                             gwallet.save() 

                                   gwallet.w_balance += Decimal(wonamount)
                                   gwallet.w_betwins += Decimal(wonamount)
                                   gwallet.save()
                                   Bet.objects.filter(id=bet.id).update(won_amnt = wonamount, status='WIN', winStat=1 , result=setwinner)
                              else:
                                   print('lose')
                                   if bet.winStat == '3' or bet.winStat == '4':
                                        deductrefund = bet.amount
                                        if gwallet.w_balance - Decimal(deductrefund) >= 0:
                                             gwallet.w_balance -= Decimal(deductrefund)
                                             gwallet.save()
                                        elif gwallet.w_betwins - Decimal(deductrefund) >= 0:
                                             gwallet.w_betwins -= Decimal(deductrefund)
                                             gwallet.save()
                                        else:
                                             gwallet.w_balance=0
                                             gwallet.w_betwins=0
                                             gwallet.save() 
                                             
                                   Bet.objects.filter(id=bet.id).update(won_amnt = 0, status='LOSE', winStat=2, result=setwinner)

                              if bet.winStat == '3' or bet.winStat == '4':
                                   # AGENT COMMISSION DISTRIBUTION 101824  
                                   user_account = UserAccount.objects.get(user_id=bet.player.id) 
                                   user_agent = user_account.user_agent.id  
                                   agent_up = bet.player.id

                                   commi_distrib = distribute_commission_upward(user_agent, agent_up, bet.amount)
                                   for commission_data in commi_distrib:
                                        if commission_data['user_id'] == bet.player.id or bet.category == "DRAW" or commission_data['commission'] <= 0:
                                             continue
                                        if gfights.f_winner:
                                             try:
                                                  with transaction.atomic():
                                                       pwallet = UserWallet.objects.select_for_update().get(user=commission_data['user_id'])
                                                       combalance = float(pwallet.w_commission) 
                                                       newcom = combalance + float(commission_data['commission'])
                                                       pwallet.w_commission = newcom
                                                       pwallet.save()

                                                       commission = Commission(
                                                       c_fight=gfights,
                                                       c_fnumber=gfights.f_number,
                                                       c_player=bet.player.id,
                                                       c_betamnt=bet.amount,
                                                       c_winner=setwinner,
                                                       c_commission=commission_data['commission'],
                                                       c_agent=commission_data['user_id'],
                                                       c_event=bet.event,
                                                       c_eventid=bet.eventid,
                                                       c_bet=bet.id,
                                                       c_level=commission_data['comm_level'],
                                                  )
                                                  commission.save()
                                             except ObjectDoesNotExist:
                                                  print(f"UserWallet for user {commission_data['user_id']} does not exist.")
                                             except Exception as e:
                                                  print(f"An error occurred while updating UserWallet: {e}")
                                        # AGENT COMMISSION DISTRIBUTION 101824
                              
                         elif setwinner == 'DRAW':
                              if setwinner == bet.category:
                                   print('draw win')
                                   if bet.winStat == '3' or bet.winStat == '4':
                                        deductrefund = bet.amount
                                        if gwallet.w_balance - Decimal(deductrefund) >= 0:
                                             gwallet.w_balance -= Decimal(deductrefund)
                                             gwallet.save()
                                        elif gwallet.w_betwins - Decimal(deductrefund) >= 0:
                                             gwallet.w_betwins -= Decimal(deductrefund)
                                             gwallet.save()
                                        else:
                                             gwallet.w_balance=0
                                             gwallet.w_betwins=0
                                             gwallet.save() 

                                   gwallet.w_balance += Decimal(wonamount)
                                   gwallet.w_betwins += Decimal(wonamount)
                                   gwallet.save() 
                                   Bet.objects.filter(id=bet.id).update(won_amnt = wonamount, status='WIN', winStat=1, result=setwinner)
                              else:
                                   print('draw lose')
                                   refundamnt = bet.amount
                                   gwallet.w_balance += Decimal(refundamnt)
                                   gwallet.save()
                                   Bet.objects.filter(id=bet.id).update(won_amnt = 0, status='DRAW', winStat=3, result=setwinner)

                         else:
                              print('cancelled')
                              refundamnt = bet.amount
                              gwallet.w_balance += Decimal(refundamnt)
                              gwallet.save()
                              Bet.objects.filter(id=bet.id).update(won_amnt = 0, status='CANCELLED', winStat=4, result=setwinner)

                         data = 'success'

                         if setwinner == 'DRAW' or setwinner == 'CANCELLED':
                              # AGENT COMMISSION  REVERT 101824  
                              user_account = UserAccount.objects.get(user_id=bet.player.id) 
                              user_agent = user_account.user_agent.id  
                              agent_up = bet.player.id

                              commi_distrib = distribute_commission_upward(user_agent, agent_up, bet.amount)
                              for commission_data in commi_distrib:
                                   if commission_data['user_id'] == bet.player.id or bet.category == "DRAW" or commission_data['commission'] <= 0:
                                        continue
                                   if gfights.f_winner:
                                        try:
                                             with transaction.atomic():
                                                  pwallet = UserWallet.objects.select_for_update().get(user=commission_data['user_id'])
                                                  combalance = float(pwallet.w_commission) 
                                                  newcom = combalance - float(commission_data['commission'])
                                                  pwallet.w_commission = newcom
                                                  pwallet.save()

                                                  Commission.objects.filter(c_agent=commission_data['user_id'], c_fight=gfights, c_eventid=bet.eventid).update(c_commission = 0, c_winner=setwinner)

                                             data = 'success'
                                        except ObjectDoesNotExist:
                                             print(f"UserWallet for user {commission_data['user_id']} does not exist.")
                                        except Exception as e:
                                             print(f"An error occurred while updating UserWallet: {e}")
                                             data = 'success'
                                   # AGENT COMMISSION  REVERT 101824
               else:
                    data = 'invalid'
     except IntegrityError as e:
          data = 'dataerror'

     except Exception as e:
          data = 'bad'
     
          print(e)
     return JsonResponse({'data':data})




















@login_required(login_url='/')
def fightlogs(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN':
          current_date = datetime.now().date()
          gevents = []

          gevents=Games.objects.all().order_by('-g_created')
          bethistory = Bet.objects.filter(created__date=current_date).order_by('-id')[:500]
          context={
               'page':'FIGHT LOGS',
               'bethistorys': bethistory,
               'gevents': list(gevents)
          }
          return render(request,'ugs_app/homepage/admin_fightlogs.html',context)
     else:
          return redirect(reverse('homepage'))
     

@csrf_exempt
def gamefight(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss in ['ADMIN']:
        if request.method == 'POST':
            geventval = request.POST.get('geventval')
            fightnum = []
            try:
                fightnum=Fight.objects.filter(f_game=geventval)
                context = {
                    'page':'FIGHT LOGS',
                    'fightnum': list(fightnum)
                }
                html_content = render_to_string('ugs_app/homepage/imprt_flogsnum.html', context)
                return HttpResponse(html_content)

            except UserProfile.DoesNotExist:
                return HttpResponse("User not found", status=404)
    else:
        return redirect(reverse('homepage'))
     



@csrf_exempt
def gamefightlogs(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss in ['ADMIN']:
        if request.method == 'POST':
               eventid = request.POST.get('eventid')
               fgnum = request.POST.get('fgnum')
               print(eventid)
               print(fgnum)
               try:
                    try:
                         totalbet=Bet.objects.filter(eventid=eventid, fightno=fgnum).aggregate(total=Sum('amount'))['total']
                         if totalbet is None:
                              totalbet=0
                    except Exception as e:
                         totalbet=0
    
                    bethistory = Bet.objects.filter(eventid=eventid, fightno=fgnum).order_by('-id')
                    context = {
                         'page':'FIGHT LOGS',
                         'bethistorys': bethistory,
                         'totalbet': totalbet,
                    }
                    html_content = render_to_string('ugs_app/homepage/imprt_fbetlogs.html', context)
                    return HttpResponse(html_content)

               except UserProfile.DoesNotExist:
                    return HttpResponse("User not found", status=404)
    else:
        return redirect(reverse('homepage'))
    










@csrf_exempt
def uchangepass(request):
     newpassword = request.POST.get('newpass')
     user_id = request.POST.get('usrid')
     usupdate = 0

     try:
          user_profile = UserProfile.objects.get(id=user_id)
          if user_profile:
               usupdate = 1
          else:
               usupdate = 0
     except Exception as e:
               usupdate = 0

     if usupdate == 1:
          try:
               account = UserAccount.objects.get(user=user_id)
               account.relpass = newpassword
               account.save()

               user_profile = UserProfile.objects.get(id=user_id)
               user_profile.set_password(newpassword)
               user_profile.save()
               
               return JsonResponse({'status': 'success'})
          except UserAccount.DoesNotExist:
               return JsonResponse({'status': 'error', 'message': 'Account does not exist'})
          except UserProfile.DoesNotExist:
               return JsonResponse({'status': 'error', 'message': 'User does not exist'})
          except Exception as e:
               return JsonResponse({'status': 'error', 'message': str(e)})
     else:
        return JsonResponse({'status': 'error', 'message': 'Invalid current password'})



@csrf_exempt
def bettingevent(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss in ['PLAYER']:
        if request.method == 'POST':
            geventval = request.POST.get('geventval')
            try:
               bethistory = Bet.objects.filter(player=request.user.id, eventid=geventval).order_by('-id')
               context={
                    'page':'BET HISTORY',
                    'bethistorys': bethistory,
               }
               html_content = render_to_string('ugs_app/homepage/imprt_betlogs.html', context)
               return HttpResponse(html_content)

            except UserProfile.DoesNotExist:
                return HttpResponse("User not found", status=404)
    else:
        return redirect(reverse('homepage'))
    


@csrf_exempt
def bettingcomms(request):
     if request.method == 'POST':
          geventval = request.POST.get('geventval')
          try:
              betcomms = Commission.objects.filter(c_agent=request.user.id, c_eventid=geventval).order_by('-c_id')
              context={
              'page':'BET COMMISSION',
              'betcomms': betcomms,
              }
              html_content = render_to_string('ugs_app/homepage/imprt_betcommslogs.html', context)
              return HttpResponse(html_content)

          except UserProfile.DoesNotExist:
               return HttpResponse("User not found", status=404)
    











@csrf_exempt
def resetFightNo(request):
     game=request.POST.get('gname')
     gid=request.POST.get('gid')
     with transaction.atomic():
        fights = Fight.objects.all() 
     #    for fight in fights:
     #        FightHistory.objects.create(
     #            f_id=fight.f_id,
     #            f_code=fight.f_code,
     #            f_number=fight.f_number,
     #            f_multiplier=fight.f_multiplier,
     #            f_game=fight.f_game,
     #            f_winner=fight.f_winner,
     #            f_longest=fight.f_longest,
     #            f_status=fight.f_status,
     #            f_update=fight.f_update,
     #            f_created=fight.f_created,
     #            f_tblrows=fight.f_tblrows
     #        )
     #        fight.delete()
     return JsonResponse({'data':game,'id':gid})



