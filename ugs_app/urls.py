
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


# from .views import load_new_user,load_points_table


urlpatterns = [
    # admin
    # path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('homepage',views.homepage,name='homepage'),
    path('registration/<str:code>',views.registration,name='registration'),
    path('upstat',views.upstat,name='upstat'),
    path('getusers',views.getusers,name='getusers'),
    path('admin-accounts',views.mydownlines,name='mydownlines'),
    path('adminActivateUser',views.adminActivateUser,name='adminActivateUser'),
    path('supradmiactiveuser',views.supradmiactiveuser,name='supradmiactiveuser'),
    path('import_adminUser', views.import_adminUser, name='import_adminUser'),
    path('import_super_adminuser', views.import_super_adminuser, name='import_super_adminuser'),
    path('sadminPoint', views.sadminPoint, name='sadminPoint'),
    path('spadminloading', views.spadminloading, name='spadminloading'),
    path('import_spadload', views.import_spadload, name='import_spadload'),
    path('fightlogs', views.fightlogs, name='fightlogs'),
    path('gamefight', views.gamefight, name='gamefight'),
    path('gamefightlogs', views.gamefightlogs, name='gamefightlogs'),
    path('uchangepass', views.uchangepass, name='uchangepass'),
    
    
    # declarator
    path('duplicate_game',views.duplicate_game,name='duplicate_game'),
    path('decla_games',views.decla_games,name='decla_games'),
    path('load_games',views.load_games,name='load_games'),
    path('add_games',views.add_games,name='add_games'),
    path('imprt_newgame', views.imprt_newgame, name='imprt_newgame'),
    path('update_games',views.update_games,name='update_games'),
    path('getgame',views.getgame,name='getgame'),
    path('gfight',views.gfight,name='gfight'),
    path('addfight',views.addfight,name='addfight'),
    path('decla/arena/<str:game_id>',views.decla_arena,name='decla_arena'),
    path('delgame',views.delgame,name='delgame'),
    path('resetFightNo',views.resetFightNo,name='resetFightNo'),
    # path('fight_logs',views.fight_logs,name='fight_logs'),

    # path('fight_stat',views.fight_stat,name='fight_stat'),
    # path('setwinner',views.setwinner,name='setwinner'),
    path('revert',views.revert,name='revert'),
    path('disburse',views.disburse,name='disburse'),
    path('nxtfight',views.nxtfight,name='nxtfight'),

    # PLAYER
    path('movie_arena/<str:movie>',views.movie_arena,name='movie_arena'),
    path('chk_subscibe',views.chk_subscibe,name='chk_subscibe'),
    path('add_subscribe',views.add_subscribe,name='add_subscribe'),

    path('player_games/<str:gamecat>',views.player_games,name='player_games'),
    path('player_reg',views.player_reg,name='player_reg'),
    path('games',views.games,name='games'),
    path('setting',views.setting,name='setting'),
    path('users',views.users,name='users'),
    path('player/arena/<str:game_id>',views.arena,name='arena'),
    path('auth_user',views.auth_user,name='auth_user'),
    path('signout',views.signout,name='signout'),
    path('account_reg',views.account_reg,name='account_reg'),
    #betting
    path('lastcall',views.lastcall,name='lastcall'),
    path('closebet',views.closebet,name='closebet'),
    path('openbet',views.openbet,name='openbet'),
    path('updatewallet',views.updatewallet,name='updatewallet'),
    #settings
    path('uppass',views.uppass,name='uppass'),
    path('timer',views.timer,name='timer'),
    
    
    
    # -------mmmmmmmm-------------
    path('admin_points', views.admin_points, name='admin_points'),
    path('loadAdminPoints',views.loadAdminPoints,name='loadAdminPoints'),
    path('load_adpoints_table', views.load_adpoints_table, name='load_adpoints_table'),
    path('userapproval',views.userapproval,name='userapproval'),
    path('activeagent',views.active_agent,name='activeagent'),
    path('activeplayer',views.active_player,name='activeplayer'),
    path('upplyrstat',views.upplyrstat,name='upplyrstat'),
    path('load_new_user', views.load_new_user, name='load_new_user'),
    path('load_agent_user', views.load_agent_user, name='load_agent_user'),
    path('load_player_user', views.load_player_user, name='load_player_user'),
    
    path('load_points', views.load_points, name='load_points'),
    path('load_points_table', views.load_points_table, name='load_points_table'),
    
    path('fight_stat',views.fight_stat,name='fight_stat'),
    path('loadingstation', views.loadingstation, name='loadingstation'),
    path('points_transactions', views.points_transactions, name='points_transactions'),
    path('pointsTransaction', views.pointsTransaction, name='pointsTransaction'),
    path('withdrawal_accnt', views.withdrawal_accnt, name='withdrawal_accnt'),
    path('convertProcess',views.convertProcess,name='convertProcess'),
    path('load_converted_table', views.load_converted_table, name='load_converted_table'),
    
    path('setwinner',views.setwinner,name='setwinner'),
    path('setlongwin',views.setlongwin,name='setlongwin'),
    path('adstaking',views.adstaking,name='adstaking'),
    path('loadStaking',views.loadStaking,name='loadStaking'),
    path('load_stake_tbl', views.load_stake_tbl, name='load_stake_tbl'),
    path('cashoutapproval', views.cashoutapproval, name='cashoutapproval'),
    path('loadagentcOut', views.loadagentcOut, name='loadagentcOut'),
    path('bethistory',views.bethistory,name='bethistory'),
    path('bettingevent', views.bettingevent, name='bettingevent'),

    path('betcomms',views.betcomms,name='betcomms'),
    path('bettingcomms',views.bettingcomms,name='bettingcomms'),
    path('convertcomms',views.convertcomms,name='convertcomms'),
    path('adloadingstation', views.adloadingstation, name='adloadingstation'),
    path('adpointsTransaction', views.adpointsTransaction, name='adpointsTransaction'),
    path('adwithdrawal_accnt', views.adwithdrawal_accnt, name='adwithdrawal_accnt'),
    path('adpoints_transactions', views.adpoints_transactions, name='adpoints_transactions'),
    path('adload_points_table', views.adload_points_table, name='adload_points_table'),
    
    path('stakerewardsWithdraw',views.stakerewardsWithdraw,name='stakerewardsWithdraw'),
    path('transactions', views.transactions, name='transactions'),
    path('revertwinner', views.revertwinner, name='revertwinner'),
    
    # path('get-fight-data/', views.get_fight_data, name='get_fight_data'),
    path('get-fight-data/<str:game_id>/', views.get_fight_data, name='get_fight_data'),
    path('betdata/<str:game_id>/', views.betdata, name='betdata'),

    path('decladata/<str:game_room>/', views.decladata, name='decladata'),
    # path('appstaking', views.appstaking, name='appstaking'),
    # ------mmmmmmmmm-------------- 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)
