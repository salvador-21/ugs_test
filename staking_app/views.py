from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
# from django.utils import timezone
from datetime import timedelta
import datetime,time
import uuid
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.core import serializers
from django.core.serializers import serialize
import json
from django.db.models import Sum,Count
from .models import StakeSlot, StakeLogs, stake_commission, Stake_withdrawal, Controls 
from django_minify_html.middleware import MinifyHtmlMiddleware
from django.http import HttpRequest, HttpResponse

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from django.urls import reverse
from datetime import datetime
from ugs_app.views import *
from staking_app.views import *
from staking_app.forms import *







def home_stake(request):
    stakewithdarws = Stake_withdrawal.objects.filter(user=request.user.id).order_by('-sw_date')
    stkwallet = UserWallet.objects.get(user=request.user.id)
    earnings = stkwallet.w_stake_earning
    withdraw = stkwallet.w_stake_out
    available = earnings - withdraw 
    stkwallet.w_stake_available = Decimal(available)
    stkwallet.save() 

    current_date_str = datetime.now()
    current_time = timezone.now()
    print(current_time)  

    costakewithdraw = Controls.objects.filter(c_name="STAKE EARNINGS WITHDRAWAL").first()
    context = {
        'page': 'STAKING',
        'stakebalance': available,
        'stakewithdarws': stakewithdarws,
        'costakewithdraw': costakewithdraw,
        'wallet': request.user.userwallet.w_balance,
    }
    return render(request, 'staking/index.html', context)






@csrf_exempt
def save_stake(request):
    if request.method == 'POST':
        code_point = get_random_string(8)
        code_stake = code_point.upper()
        s_type = request.POST.get('s_type')
        s_rate = request.POST.get('s_rate')
        current_date_str = datetime.now()
        status = "invalid" 
        stakeActive = 0
        remaining = 0
        
        if s_type=='1':
            s_amnt = 500
            s_comm = s_amnt*0.08
            name = "SAND CLOCK"
        elif s_type=='2':
            s_amnt = 1000
            s_comm = s_amnt*0.10
            name = "REGULAR CLOCK"
        elif s_type=='3':
            s_amnt = 2000
            s_comm = s_amnt*0.15
            name = "MODERN CLOCK"
        elif s_type=='4':
            s_amnt = 5000
            s_comm = s_amnt*0.20
            name = "TECHNO CLOCK"
        elif s_type=='5':
            s_amnt = 10000
            s_comm = s_amnt*0.25
            name = "ROLEX CLOCK"
        else:
            s_amnt = 0
            s_comm = 0
            name = ""
        
        if s_amnt>0 and s_comm>0:
            try:
                stakehistory = StakeSlot.objects.filter(user=request.user.id).order_by('-sl_date').first()
                if stakehistory:
                    lastdate = stakehistory.sl_date
                else:
                    lastdate = 'NotExist'
            except StakeSlot.DoesNotExist:
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
                        
            if status == 'valid':
                total_income = float(s_amnt) + float(s_comm)
                daily_income = total_income/90

                try:
                    clwallet = UserWallet.objects.get(user=request.user.id)
                    stake_bal=clwallet.w_stakebal
                    stakeActive = clwallet.w_stake_active
                except UserWallet.DoesNotExist:
                    stake_bal = 0

                if stake_bal > 0 and s_amnt <= stake_bal:
                    try:
                        with transaction.atomic():
                            remaining = float(stake_bal) - float(s_amnt)
                            transactions = StakeSlot(
                                user=request.user,
                                sl_name=name,
                                sl_rate=s_rate,
                                sl_amount=Decimal(s_amnt),
                                sl_type=s_type,
                                sl_status='ACTIVE',
                                sl_duration=90,
                                sl_daily=Decimal(daily_income),
                                sl_earnings=Decimal(0.00),
                                sl_total=Decimal(total_income),
                                sl_code=code_stake,
                                # sl_date=current_date_str
                            )
                            transactions.save()
                            clwallet.w_stakebal = remaining
                            clwallet.w_stake_active += Decimal(s_amnt)
                            clwallet.save() 

                            user_account = UserAccount.objects.get(user=request.user.id)
                            agent_id = user_account.user_agent.id 
                            palyer_user_id = request.user.id
                            stakeCode = code_stake
                            stake_amount = s_amnt
                            staketype = s_type
                            

                            results = function_upward(agent_id, palyer_user_id, stakeCode,stake_amount,staketype)
                            
                            data = "success"
                            stakeActive = clwallet.w_stake_active
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        data = "error05"
                        remaining = 0
                else:
                    data = "error01"
                    remaining = 0
            else:
                data="error02"
                remaining = 0
        else:
            data="error03"
            remaining = 0
    else:
        data="error04"
        remaining = 0

    return JsonResponse({'data':data,'stakebalance':remaining,'stakeActive':stakeActive})
    


















def function_upward(agent_ids, player_user_id, stakeCode, stake_amount, staketype, results=None, visited=None, count=0, limit=3):
    if results is None:
        results = []
    if visited is None:
        visited = set()

    if count >= limit or agent_ids in visited:
        return results
    visited.add(agent_ids)
    
    try:
        count += 1
        user_account = UserAccount.objects.get(user_id=agent_ids)
        agent_wallet = UserWallet.objects.get(user=user_account.user.id)

        if count == 1:
            commrate = 0.10
        elif count == 2:
            commrate = 0.03
        elif count == 3:
            commrate = 0.02
        commval = Decimal(stake_amount) * Decimal(commrate)

       
        if user_account.user_agent.id:
            user_agent_id = UserProfile.objects.get(id=agent_ids)
            commission = stake_commission(
                sc_code=stakeCode, 
                sc_player=player_user_id,
                sc_agent=user_agent_id,
                sc_level=count,
                sc_percent=commrate,
                sc_type=staketype,
                sc_amount=stake_amount,
                sc_commission=commval,
            )
            commission.save()
            agent_wallet.w_stakecom += commval
            agent_wallet.save()
            print(player_user_id)
            print(agent_ids)
        
        results.append(f"{count}. {agent_ids} - Commission Rate: {commrate} - {stakeCode} - {player_user_id}")
        
        if user_account.user_agent.id:
                return function_upward(user_account.user_agent.id, player_user_id, stakeCode, stake_amount, staketype, results, visited, count, limit)
        else:
            results.append(f"User account with user_id {agent_ids} has no agent.")

    except UserAccount.DoesNotExist:
        results.append(f"User account with user_id {agent_ids} does not exist.")
    except UserWallet.DoesNotExist:
        results.append(f"User wallet with user_id {agent_ids} does not exist.")
    
    return results, count






@login_required(login_url='/')
def stakecommis(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN' or usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          stakecomms = stake_commission.objects.filter(sc_agent=request.user.id).order_by('-sc_id')
          agent_id = request.user.id

          try:
               uwallet=UserWallet.objects.get(user=agent_id)
               commsbal = uwallet.w_stakecom
               cliambal = uwallet.w_stakecom_claim
               newcomsbal=float(commsbal) - float(cliambal)
               if newcomsbal>0:
                    newcomsbal = newcomsbal
               else:
                    newcomsbal = 0
          except Exception as e:
               newcomsbal = 0

          context={
               'page':'STAKE COMMS',
               'stakecomms': stakecomms,
               'newcomsbal': newcomsbal,
          }
          return render(request,'staking/stake_comms.html',context)
     else:
          return redirect(reverse('homepage'))
     


@login_required(login_url='/')
def stakecommclaim(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          stakecommswithdraw = Stake_claimed_comms.objects.filter(sr_user=request.user.id).order_by('-sr_id')
          agent_id = request.user.id

          try:
               uwallet=UserWallet.objects.get(user=agent_id)
               commsbal = uwallet.w_stakecom
               cliambal = uwallet.w_stakecom_claim
               newcomsbal=float(commsbal) - float(cliambal)
               if newcomsbal>0:
                    newcomsbal = newcomsbal
               else:
                    newcomsbal = 0
          except Exception as e:
               newcomsbal = 0

          context={
               'page':'WITHDRAWAL REWARDS',
               'stakecommswithdraw': stakecommswithdraw,
               'newcomsbal': newcomsbal,
          }
          return render(request,'staking/stake_comms_withdraw.html',context)
     else:
          return redirect(reverse('homepage'))
     




@login_required(login_url='/')
def import_stakecom_withdrw(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'MASTER OPERATOR' or usertype_ss == 'INCORPORATOR' or usertype_ss == 'SUB ADMIN' or usertype_ss == 'SUB OPERATOR' or usertype_ss == 'MASTER AGENT':
          stakecommswithdraw = Stake_claimed_comms.objects.filter(sr_user=request.user.id).order_by('-sr_id')
          context={
               'page':'WITHDRAWAL REWARDS',
               'stakecommswithdraw': stakecommswithdraw,
          }
          html_content = render_to_string('staking/imprt_stake_comwithdraw.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))







@csrf_exempt
def activeStakingSlot(request):
    if request.method == 'POST':
        stakingtype = request.POST.get('stakingtype')
        myuserid = request.user
        mystake = StakeSlot.objects.filter(user=myuserid, sl_type=stakingtype).order_by('-sl_date')
        current_time = timezone.now()
        print('xxxxxxxxxxxxx')
        print(current_time)
        print('xxxxxxxxxxxxx')
        

        mystakes_with_days = []
        for entry in mystake:
            days_difference = (current_time - entry.sl_date).days
            daily_income = entry.sl_daily * days_difference
            balance = daily_income - entry.sl_claimed
            
            print(days_difference)
            if days_difference<=90:
                entry.sl_daysactive = days_difference
                entry.sl_earnings = daily_income
                entry.sl_balance = balance
                entry.save(update_fields=['sl_daysactive', 'sl_earnings','sl_balance'])
            else:
                days_difference = entry.sl_daysactive
                daily_income = entry.sl_total  
                balance = daily_income - entry.sl_claimed

                entry.sl_daysactive =90
                entry.sl_earnings = daily_income
                entry.sl_balance = balance
                entry.save(update_fields=['sl_daysactive', 'sl_earnings','sl_balance'])

                
            
            if entry.sl_balance >0:
                btnaccess = ""
                btnstyle = "btn-outline-success"
                btntext = "CLAIM"
            elif days_difference>=90:
                btnaccess = "disabled"
                btnstyle = "btn-outline-secondary"
                btntext = "DONE"
            else:
                btnaccess = "disabled"
                btnstyle = "btn-outline-secondary"
                btntext = "CLAIM"
                
            mystakes_with_days.append({
                'stake': entry,
                'btnaccess': btnaccess,
                'btnstyle': btnstyle,
                'btntext': btntext,
                'dayscount': days_difference,
                'daily_income': daily_income
            })

        stakecount = StakeSlot.objects.filter(user=myuserid, sl_type=stakingtype).aggregate(total=Count('sl_id'))['total'] or 0

        staking_types = {
            '1': {'s_amnt': 500, 's_comm': 8, 'name': "SAND CLOCK"},
            '2': {'s_amnt': 1000, 's_comm': 10, 'name': "REGULAR CLOCK"},
            '3': {'s_amnt': 2000, 's_comm': 15, 'name': "MODERN CLOCK"},
            '4': {'s_amnt': 5000, 's_comm': 20, 'name': "TECHNO CLOCK"},
            '5': {'s_amnt': 10000, 's_comm': 25, 'name': "ROLEX CLOCK"},
        }
        staking_attrs = staking_types.get(stakingtype, {'s_amnt': 0, 's_comm': 0, 'name': ""})

        context = {
            'page': 'STAKING',
            'myuserid': myuserid,
            'mystakes': mystakes_with_days,
            's_amnt': staking_attrs['s_amnt'],
            's_comm': staking_attrs['s_comm'],
            'name': staking_attrs['name'],
            'stakecount': stakecount,
        }

        html_content = render_to_string('staking/active_staking_table.html', context)
        return HttpResponse(html_content)
    return HttpResponse(status=405)







@csrf_exempt
def claimstake(request):
    if request.method == 'POST':
        stakecode = request.POST.get('stakecode')
        status = "invalid" 
        earnings = 0.00
        avilearnings = 0.00
        try:
            stkwallet = UserWallet.objects.get(user=request.user.id)
            earnings = stkwallet.w_stake_earning
            withdraw = stkwallet.w_stake_out
            waccess = "ok"
        except UserWallet.DoesNotExist:
            waccess = "bad"
            earnings = 0.00

        mystake = StakeSlot.objects.filter(sl_code=stakecode).first()
        if mystake is not None:
            stkcde = mystake.sl_code
            stk_name = mystake.sl_name
            stk_type = mystake.sl_type
            earned = mystake.sl_earnings
            claimed = mystake.sl_claimed
            balance = mystake.sl_balance
        else:
            stkcde = None
            earned = 0.00
            claimed = 0.00 

        availablebal = Decimal(stkwallet.w_stake_earning) - Decimal(stkwallet.w_stake_out) 
        avilearnings = availablebal
        available = Decimal(earned) - Decimal(claimed) 

        if waccess == "ok" and stkcde != "None" and balance > 0.00 and available >0.00:
            try:
                stakehistory = StakeLogs.objects.filter(user=request.user.id).order_by('-stk_date').first()
                if stakehistory:
                    lastdate = stakehistory.stk_date
                else:
                    lastdate = 'NotExist'
            except StakeSlot.DoesNotExist:
                lastdate = 'NotExist'

            if lastdate !='NotExist':
                if lastdate.tzinfo is None:
                    date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                else:
                    date1 = lastdate
                    date2 = timezone.now()
                    time_difference = date2 - date1
                    difference_in_seconds = time_difference.total_seconds()
                    if difference_in_seconds > 2:
                        status = "valid"
                    else:
                        status = "invalid"
            else:
                status = "valid"

            if status == 'valid':
                try:
                    with transaction.atomic():
                        transactions = StakeLogs(
                        user=request.user,
                        stk_code=stakecode,
                        stk_name=stk_name,
                        stk_earnings=Decimal(balance),
                        stk_type=stk_type,
                        )
                        transactions.save()

                        new_claimed = claimed + balance
                        StakeSlot.objects.filter(sl_code=stakecode).update(
                            sl_claimed=new_claimed,
                            sl_balance=0.00
                        )

                        stkwallet.w_stake_earning += Decimal(balance)
                        availablebal = Decimal(stkwallet.w_stake_earning) - Decimal(stkwallet.w_stake_out) 
                        stkwallet.w_stake_available = Decimal(availablebal)
                        stkwallet.save() 

                        data = "success"
                        earnings = stkwallet.w_stake_earning
                        avilearnings = availablebal

                except Exception as e:
                        print(f"Error occurred: {e}")
                        data = "error"
            else:
                data="tryagain"
        else:
            data = "insufficient"
    else:
        data="invalid"

    return JsonResponse({'data':data,'earnings':earnings,'avilearnings':avilearnings})










@csrf_exempt
def withdarwStake(request):
    if request.method == 'POST':
        code_point = get_random_string(8)
        code_stake = code_point.upper()
        mop = request.POST.get('mop')
        acct_name = request.POST.get('acct_name')
        acct_number = request.POST.get('acct_number')
        cash_amnt = request.POST.get('cash_amnt')
        status = "invalid" 
        stkebalance = 0.00
        stkecoutbal = 0.00

        if mop !="" and acct_name !="" and acct_number !="" and cash_amnt !="":
            try:
                stkwallet = UserWallet.objects.get(user=request.user.id)
                earnings = stkwallet.w_stake_earning
                withdraw = stkwallet.w_stake_out
                stkecoutbal = stkwallet.w_stake_out
                waccess = "ok"
            except UserWallet.DoesNotExist:
                waccess = "bad"
                earnings = 0.00
                withdraw = 0.00

            if waccess == "ok":
                available = Decimal(earnings) - Decimal(withdraw) 
                balance = Decimal(available) - Decimal(cash_amnt)
                stkebalance = balance
                if Decimal(cash_amnt)>0:
                    if Decimal(available)>=Decimal(cash_amnt):
                        try:
                            stakehistory = Stake_withdrawal.objects.filter(user=request.user.id).order_by('-sw_date').first()
                            if stakehistory:
                                lastdate = stakehistory.sw_date
                            else:
                                lastdate = 'NotExist'
                        except StakeSlot.DoesNotExist:
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
                        
                        if status == 'valid':
                            try:
                                with transaction.atomic():
                                    transactions = Stake_withdrawal(
                                    user=request.user,
                                    sw_code=code_stake,
                                    sw_mop=mop,
                                    sw_ac_name=acct_name,
                                    sw_ac_number=acct_number,
                                    sw_available=Decimal(available),
                                    sw_withdraw=Decimal(cash_amnt),
                                    sw_balance=Decimal(balance),
                                    )
                                    transactions.save()

                                    stkwallet.w_stake_out += Decimal(cash_amnt)
                                    stkwallet.w_stake_available = Decimal(balance)
                                    stkwallet.save() 

                                    data = "success"
                                    stkebalance = stkwallet.w_stake_available
                                    stkecoutbal = stkwallet.w_stake_out

                            except Exception as e:
                                    print(f"Error occurred: {e}")
                                    data = "error"
                        else:
                            data="tryagain"
                    else:
                        data="insufficient" 
                else:
                    data="invalid" 
            else:
                data="invalid" 
        else:
            data="required" 
    else:
        data="invalid"

    return JsonResponse({'data':data,'stkebalance':stkebalance,'stkecoutbal':stkecoutbal})





@login_required(login_url='/')
def importswithdraw(request):
    stakewithdarws = Stake_withdrawal.objects.filter(user=request.user.id).order_by('-sw_date')
    context = {
        'page': 'STAKING',
        'stakewithdarws': stakewithdarws,
    }
    html_content = render_to_string('staking/import_stake_withdraw.html', context)    
    return HttpResponse(html_content)





@login_required(login_url='/')
def adstakewithdraw(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
        stakewithdarws = Stake_withdrawal.objects.filter(sw_status="PENDING").order_by('-sw_date')
        costakewithdraw = Controls.objects.filter(c_name="STAKE EARNINGS WITHDRAWAL").first()
        context = {
            'page': 'STAKING WITHDRAWAL',
            'stakewithdarws': stakewithdarws,
            'costakewithdraw': costakewithdraw,
        }
        return render(request, 'staking/ad_stake_withdrawal.html', context)
    else:
          return redirect(reverse('homepage'))
    






@csrf_exempt
def adstakewtdrawconfirm(request):
    data = "error"
    if request.method == 'POST':
        adminid = request.user.id
        rowid = request.POST.get('rwid')
        current_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            Stake_withdrawal.objects.filter(sw_id=rowid).update(
                sw_status="APPROVED",
                sw_confirmed=adminid,
                sw_dateconfirm=current_date_str
            )
            data = "success"
        except Exception as e:
            data="error"

    return JsonResponse({'data': data})


@login_required(login_url='/')
def ad_withdraw_confirmed(request):
    stakewithdarws = Stake_withdrawal.objects.filter(sw_status="PENDING").order_by('-sw_date')
    context = {
        'page': 'STAKING WITHDRAWAL',
        'stakewithdarws': stakewithdarws,
    }
    html_content = render_to_string('staking/import_adconfimed_withdraw.html', context)    
    return HttpResponse(html_content)







@login_required(login_url='/')
def adstwithdrawhistory(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
        stakewithdarws = Stake_withdrawal.objects.filter(sw_status="APPROVED").order_by('-sw_date')
        context = {
            'page': 'STAKE WITHDRAWAL HISTORY',
            'stakewithdarws': stakewithdarws,
        }
        return render(request, 'staking/ad_stake_withdrawal_history.html', context)
    else:
          return redirect(reverse('homepage'))
    




@login_required(login_url='/')
def adstkcomscout(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
        stakecommswithdraw = Stake_claimed_comms.objects.filter(sr_status=0).order_by('-sr_id')

        try:
          totalskcom=UserWallet.objects.all().aggregate(total=Sum('w_stakecom'))['total']
          if totalskcom is None:
               totalskcom=0
        except Exception as e:
            totalskcom=0

        try:
          skcomclaim=UserWallet.objects.all().aggregate(total=Sum('w_stakecom_claim'))['total']
          if skcomclaim is None:
               skcomclaim=0
        except Exception as e:
            skcomclaim=0

        newcomsbal=float(totalskcom) - float(skcomclaim)
        if newcomsbal>0:
            newcomsbal = newcomsbal
        else:
            newcomsbal = 0

    
        context={
            'page':'REWARDS WITHDRAWAL',
            'stakecommswithdraw': stakecommswithdraw,
            'newcomsbal': newcomsbal,
            'totalskcom': totalskcom,
            'skcomclaim': skcomclaim
        }
        return render(request, 'staking/ad_rewards_withdrawal.html', context)
    else:
          return redirect(reverse('homepage'))
    

@csrf_exempt
def confirmcocoms(request):
    data = "error"
    if request.method == 'POST':
        adminid = request.user.id
        rowid = request.POST.get('rwid')
        current_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            Stake_claimed_comms.objects.filter(sr_id=rowid).update(
                sr_status=1,
                sr_confirmed=adminid,
                sr_dateconfirm=current_date_str
            )
            data = "success"
        except Exception as e:
            data="error"

    return JsonResponse({'data': data})






@login_required(login_url='/')
def ad_comco_tbl(request):
    stakecommswithdraw = Stake_claimed_comms.objects.filter(sr_status=0).order_by('-sr_id')
    context={
        'page':'REWARDS WITHDRAWAL',
        'stakecommswithdraw': stakecommswithdraw,
    }
    html_content = render_to_string('staking/importcocoms_tbl.html', context)    
    return HttpResponse(html_content)



@login_required(login_url='/')
def stkcomscouthstory(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'ADMIN':
        stakecommswithdraw = Stake_claimed_comms.objects.filter(sr_status=1).order_by('-sr_id')
        context={
            'page':'REWARDS WITHDRAWAL HISTORY',
            'stakecommswithdraw': stakecommswithdraw,
        }
        return render(request, 'staking/ad_comsco_histry.html', context)
    else:
          return redirect(reverse('homepage'))
    

@csrf_exempt
def stakecoutstatus(request):
    data = "error"
    if request.method == 'POST':
        coutstat = request.POST.get('coutstat')
        try:
            UserAccount.objects.update(
                coutstat=coutstat
            )
            data = "success"
        except Exception as e:
            data="error"

    return JsonResponse({'data': data})




@csrf_exempt
def stakeearningscout(request):
    data = "error"
    if request.method == 'POST':
        coutstat = request.POST.get('coutstat')
        current_date_str = datetime.now()
        try:
            Controls.objects.filter(c_name="STAKE EARNINGS WITHDRAWAL").update(
                c_status=coutstat,
                c_date=current_date_str
            )
            data = "success"
        except Exception as e:
            data="error"

    return JsonResponse({'data': data})

     
    



