
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

from rest_framework import serializers

from djoser.serializers import UserCreatePasswordRetypeSerializer as DjoserUserCreatePasswordRetypeSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer

User = get_user_model()


class CustomUserCreateSerializer(DjoserUserCreatePasswordRetypeSerializer):
    """Inscription avec email obligatoire et unique."""

    class Meta(DjoserUserCreatePasswordRetypeSerializer.Meta):
        model = User
        # re_password est ajouté par UserCreatePasswordRetypeSerializer.__init__
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [EmailValidator(message='Enter a valid email address.')],
            },
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("L'email est obligatoire.")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("user with this email already exists.")
        return value


class CustomUserSerializer(DjoserUserSerializer):

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar')
        read_only_fields = ('id', 'username')
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [EmailValidator(message='Enter a valid email address.')],
            },
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("L'email est obligatoire.")
        # Exclure l'utilisateur courant lors de la mise à jour
        queryset = User.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("user with this email already exists.")
        return value
