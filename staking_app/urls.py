
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from staking_app import views 

# from .views import load_new_user,load_points_table


urlpatterns = [
    # admin
    path('', views.home_stake,name='home_stake'),
    path('save_stake',views.save_stake,name='save_stake'),
    path('stakecommis',views.stakecommis,name='stakecommis'),
    path('activeStakingSlot',views.activeStakingSlot,name='activeStakingSlot'),
    path('claimstake',views.claimstake,name='claimstake'),
    path('withdarwStake',views.withdarwStake,name='withdarwStake'),
    path('importswithdraw', views.importswithdraw, name='importswithdraw'),
    path('adstakewithdraw', views.adstakewithdraw, name='adstakewithdraw'),
    path('adstakewtdrawconfirm', views.adstakewtdrawconfirm, name='adstakewtdrawconfirm'),
    path('ad_withdraw_confirmed', views.ad_withdraw_confirmed, name='ad_withdraw_confirmed'),
    path('adstwithdrawhistory', views.adstwithdrawhistory, name='adstwithdrawhistory'),

    path('stakecommclaim',views.stakecommclaim,name='stakecommclaim'),
    path('import_stakecom_withdrw', views.import_stakecom_withdrw, name='import_stakecom_withdrw'),

    path('adstkcomscout', views.adstkcomscout, name='adstkcomscout'),
    path('confirmcocoms', views.confirmcocoms, name='confirmcocoms'),
    path('ad_comco_tbl', views.ad_comco_tbl, name='ad_comco_tbl'),
    path('stkcomscouthstory', views.stkcomscouthstory, name='stkcomscouthstory'),
    path('stakecoutstatus', views.stakecoutstatus, name='stakecoutstatus'),
    path('stakeearningscout', views.stakeearningscout, name='stakeearningscout'),
    # ------mmmmmmmmm-------------- 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
