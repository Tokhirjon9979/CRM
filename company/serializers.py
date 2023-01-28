from rest_framework import serializers
from .models import Company


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
