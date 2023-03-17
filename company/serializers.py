from rest_framework import serializers
from .models import Company, Product
from accounts.models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'phone', 'name', 'email', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone.isnumeric() or len(phone) > 12:
            raise serializers.ValidationError('Your phone number has not numeric symbols or it is short')
        return attrs

    def create(self, validated_data):
        # print(validated_data)
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'company_id', 'price', 'description', 'image', 'created_at']

    # def create(self, validated_data):
    #     return super().create(validated_data)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name')


# class CompanyySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = 'name',
