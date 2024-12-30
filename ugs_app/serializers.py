from rest_framework import serializers
from .models import Games,Fight,Bet,UserAccount,UserProfile,UserWallet



class UserSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(many=False,read_only=True)
    class Meta:
        model = UserAccount
        fields ='__all__'

class GameSerializer(serializers.ModelSerializer):
    f_game=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Games
        fields ='__all__'

class FightSerializer(serializers.ModelSerializer):
    # fight=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Fight
        fields ='__all__'