from rest_framework import serializers
from .models import User, MediaFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'storage_limit', 'used_storage']
        read_only_fields = ['storage_limit', 'used_storage']

class MediaFileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MediaFile
        fields = ['id', 'owner', 'file', 'title', 'description', 'size', 'created_at', 'is_public']
        read_only_fields = ['owner', 'size', 'created_at']

    def validate_file(self, value):
        user = self.context['request'].user

        if user.used_storage + value.size > user.storage_limit:
            raise serializers.ValidationError(
                f"Not enough space. Available: {(user.storage_limit - user.used_storage) / 1024 / 1024:.2f} MB"
            )
        return value

class MediaFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['title', 'description', 'is_public']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'storage_limit', 'used_storage', 'is_staff']
        read_only_fields = ['id', 'storage_limit', 'used_storage']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user