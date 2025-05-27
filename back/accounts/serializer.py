import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserSubscription, UserSavingSubscription
from products.serializers import DepositProductsSerializer, SavingProductsSerializer

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


class UserCombinedSubscriptionSerializer(serializers.Serializer):
    """
    deposit + saving 구독을 통합하여 반환할 때 사용합니다.
    """
    type = serializers.CharField()        # 'deposit' or 'saving'
    fin_prdt_cd = serializers.CharField()
    product_name = serializers.CharField()
    bank_name = serializers.CharField()
    term_months = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    remaining_days = serializers.IntegerField()

    def to_representation(self, instance):
        return super().to_representation(instance)


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """
    정기예금(UserSubscription) 구독 정보를 직렬화합니다.
    """
    fin_prdt_cd = serializers.CharField(source='product.fin_prdt_cd', read_only=True)
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'fin_prdt_cd',
            'product_name',
            'bank_name',
            'term_months',
            'start_date',
            'end_date',
            'remaining_days',
        ]

    def get_remaining_days(self, obj):
        now = timezone.now()
        return max(0, (obj.end_date - now).days)


class UserSavingSubscriptionSerializer(serializers.ModelSerializer):
    """
    정기적금(UserSavingSubscription) 구독 정보를 직렬화합니다.
    """
    fin_prdt_cd = serializers.CharField(source='product.fin_prdt_cd', read_only=True)
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = UserSavingSubscription
        fields = [
            'id',
            'fin_prdt_cd',
            'product_name',
            'bank_name',
            'term_months',
            'start_date',
            'end_date',
            'remaining_days',
        ]

    def get_remaining_days(self, obj):
        now = timezone.now()
        return max(0, (obj.end_date - now).days)


class ProfileSerializer(serializers.ModelSerializer):
    """
    내 프로필 조회/수정 전용 Serializer.
    읽기 전용 필드: id, membership_number, date_joined, followers/following counts
    구독 정보는 중간 모델 직렬화기를 이용해 제공합니다.
    """
    id = serializers.ReadOnlyField()
    membership_number = serializers.ReadOnlyField()
    date_joined = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    active_deposit_subscriptions = UserSubscriptionSerializer(
        source='subscriptions', many=True, read_only=True
    )
    active_saving_subscriptions = UserSavingSubscriptionSerializer(
        source='saving_subscriptions', many=True, read_only=True
    )

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
            'active_deposit_subscriptions',
            'active_saving_subscriptions',
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
    다른 사용자의 프로필 조회 전용.
    is_following 필드를 추가하여 로그인 사용자와의
    팔로우 관계 여부를 제공합니다.
    """
    is_following = serializers.SerializerMethodField()

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ['is_following']
        read_only_fields = ProfileSerializer.Meta.read_only_fields + ['is_following']

    def get_is_following(self, obj):
        request_user = self.context['request'].user
        if not request_user.is_authenticated:
            return False
        return request_user.following.filter(pk=obj.pk).exists()
