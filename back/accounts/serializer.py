from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.serializers import DepositProductsSerializer, SavingProductsSerializer
from .models import User, UserSubscription
import uuid
from django.utils import timezone

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    회원가입: username, password, email 입력받고
    membership_number를 UUID 기반으로 자동 생성합니다.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        membership_number = uuid.uuid4().hex[:20]
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        user.membership_number = membership_number
        user.save()
        return user

class UserSubscriptionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm')
    bank_name = serializers.CharField(source='product.kor_co_nm')
    remaining_days = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'product_name', 'bank_name', 'term_months',
            'start_date', 'end_date', 'remaining_days'
        ]
    
    def get_remaining_days(self, obj):
        now = timezone.now()
        if now > obj.end_date:
            return 0
        return (obj.end_date - now).days


class ProfileSerializer(serializers.ModelSerializer):
    """
    내 프로필 조회/수정 전용 Serializer.
    읽기 전용 필드: id, membership_number, date_joined
    + followers_count, following_count 추가
    """
    id = serializers.ReadOnlyField()
    membership_number = serializers.ReadOnlyField()
    date_joined = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    subscribed_deposit_products = DepositProductsSerializer(many=True, read_only=True)
    active_subscriptions = UserSubscriptionSerializer(source='subscriptions', many=True)
    subscribed_saving_products = SavingProductsSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = [
            'id',
            'membership_number',
            'username',
            'email',
            'date_joined',
            'profile_image',
            'bio',
            'age',
            'current_balance',
            'salary',
            'followers_count',
            'following_count',
            'subscribed_deposit_products',
            'subscribed_saving_products',
            'active_subscriptions',
        ]
        read_only_fields = [
            'id',
            'membership_number',
            'date_joined',
            'followers_count',
            'following_count',
        ]


class PublicProfileSerializer(ProfileSerializer):
    """
    다른 회원 프로필 조회 전용 Serializer.
    ProfileSerializer 필드 + 팔로우 정보
    """
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    is_following    = serializers.SerializerMethodField()

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [
            'followers_count',
            'following_count',
            'is_following',
        ]
        read_only_fields = ProfileSerializer.Meta.read_only_fields + [
            'followers_count',
            'following_count',
            'is_following',
        ]

    def get_is_following(self, obj):
        request_user = self.context['request'].user
        if not request_user.is_authenticated:
            return False
        return request_user.following.filter(pk=obj.pk).exists()
