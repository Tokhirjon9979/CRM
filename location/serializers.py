from rest_framework import serializers

from location.models import Location, LocationImages


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'company']

    # validate yoziw kerak request.user==company.owner
    def validate(self, attrs):
        company = attrs.get('company')
        if self.context['request'].user != company.owner:
            raise serializers.ValidationError(
                'If you are not owner of company, you are not allowed for adding location')
        return attrs


class LocationImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationImages
        fields = ['title', 'location', 'image']

    # validate yoziw kerak request.user==company.owner
    def validate(self, attrs):
        location = attrs.get('location')
        if self.context['request'].user != location.company.owner:
            raise serializers.ValidationError(
                'If you are not owner of company, you are not allowed for adding location image')
        return attrs
