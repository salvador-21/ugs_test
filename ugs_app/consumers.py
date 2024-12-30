import json
from random import randint
from time import sleep
from django.core.serializers import serialize
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import UserAccount,UserWallet,Games,Fight,Bet,Longestfight
from .serializers import FightSerializer,GameSerializer
from django.db.models import Sum,Q
import uuid
import sys
from urllib.parse import parse_qsl




class WSArena(AsyncWebsocketConsumer):
    
    async def connect(self):
            self.player=self.scope['user']
            self.game_room=self.scope['url_route']['kwargs']['game_id']
            self.user = self.scope["user"]
            
        
             #join room
            await self.channel_layer.group_add(
                  self.game_room,
                  self.channel_name
                  
            )
        
            await self.accept()

    async def disconnect(self, close_code):
         print(f'connection closed with code:{close_code}')

    async def receive(self,text_data):
            username = self.scope["user"]
            
            data=json.loads(text_data)
            await self.channel_layer.group_send(
                        self.game_room,
                        {
                        'type':'game_details',
               
                        }
                )
            
           

    async def close_bet(self,event):
          games = await main(self.user,self.game_room)
          new_data = json.dumps(games)
          await self.send(text_data=new_data)

#     async def open_bet(self,event):
#           status='OPEN'
#           new_data = json.dumps(status)
#           await self.send(text_data=new_data)

    async def game_details(self,event):
            games = await main(self.user,self.game_room)
            new_data = json.dumps(games)
            await self.send(text_data=new_data)
  
    
#     @sync_to_async
#     def save_bet(self,player,amount,category,fight):
#          return Bet.objects.create(player=player,amount=amount,category=category,fight=fight)
    
    @sync_to_async
    def get_fight(self,game_room):
         gf=Fight.objects.filter(~Q(f_status ='DONE'),f_game=game_room)
         for f in gf:
              fid=f.f_id
         return f

@database_sync_to_async
def main(user,game_room):

        try:
             cgame=Games.objects.get(g_id=game_room)
             plasada=cgame.g_plasada
        except Exception as e:
             plasada=0
             
        wallet=UserWallet.objects.get(user=user)
        wbalance=wallet.w_balance

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

        draw=Bet.objects.filter(fight=fid,category='DRAW').aggregate(total=Sum('amount'))['total'] 
        longest=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST',l_player=user).aggregate(total=Sum('l_amount'))['total'] 

        try:
          mymeronbet=Bet.objects.filter(fight=fid,status='PENDING',category='MERON',player=user).aggregate(total=Sum('amount'))['total']
          if mymeronbet is None:
              mymeronbet=0
        except Exception as e:
          mymeronbet=0

        try:
          mywalabet=Bet.objects.filter(fight=fid,status='PENDING',category='WALA',player=user).aggregate(total=Sum('amount'))['total'] 
          if mywalabet is None:
              mywalabet=0
        except Exception as e:
          mywalabet=0

        try:
          mydrawbet=Bet.objects.filter(fight=fid,status='PENDING',category='DRAW',player=user).aggregate(total=Sum('amount'))['total'] 
          if mydrawbet is None:
              mydrawbet=0
        except Exception as e:
          mydrawbet=0
        
        try:
          mylongbet=Longestfight.objects.filter(l_status='PENDING',l_category='LONGEST',l_player=user).aggregate(total=Sum('l_amount'))['total'] 
          if mylongbet is None:
                mylongbet=0
        except Exception as e:
          mylongbet=0

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
        
        
        data={
             'game_id':game_room,
              'fightnum':game_num,
              'fightid':str(fid),
              'multi':str(fmulti),
              'bet_status':status,
              'winner':winner,
              'dmeron':str(dmeron),
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

        return data
