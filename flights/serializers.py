from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date
from .models import Flight, Booking, Profile


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
    flight= serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='destination'
     )

    class Meta:
        model = Booking
        fields =  ['flight','date', 'id',]


class BookingDetailsSerializer(serializers.ModelSerializer):
    total=serializers.SerializerMethodField()
    flight=FlightSerializer()
    

    class Meta:
        model = Booking
        fields = [ 'total', 'flight', 'date', 'id', 'passengers',]
    def get_total (self, obj):
        total= obj.passengers * obj.flight.price
        return total



class AdminUpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name',]

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    past_bookings=serializers.SerializerMethodField()
    tier=serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user', 'miles', 'past_bookings', 'tier',]
    def get_past_bookings(self, obj):
        flights=obj.user.bookings.filter(date__lt=date.today())
        flights= BookingSerializer(flights, many=True).data
        return flights
    def get_tier(self,obj):
        tier= obj.miles
        if tier>=0 or tier<=9999:
            return "Blue"
        elif tier>=10000 or tier<=59999:
            return "Silver"
        elif tier>=60000 or tier<=99999:
            return "Gold"
        else: 
            return "Platinum"
     

