from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import BurgerQuiz, Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger


class BurgerQuizSerializer(ModelSerializer):
    nuggets_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    salt_or_pepper_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    menus_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    addition_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    deadly_burger_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = BurgerQuiz
        fields = [
            "id",
            "title",
            "toss",
            "created_at",
            "updated_at",
            "nuggets",
            "salt_or_pepper",
            "menus",
            "addition",
            "deadly_burger",
            "nuggets_id",
            "salt_or_pepper_id",
            "menus_id",
            "addition_id",
            "deadly_burger_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "nuggets", "salt_or_pepper", "menus", "addition", "deadly_burger"]
        extra_kwargs = {
            "toss": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    def validate_nuggets_id(self, value):
        if value is None:
            return value
        if not Nuggets.objects.filter(id=value).exists():
            raise serializers.ValidationError("Cette manche Nuggets n'existe pas.")
        return value

    def validate_salt_or_pepper_id(self, value):
        if value is None:
            return value
        if not SaltOrPepper.objects.filter(id=value).exists():
            raise serializers.ValidationError("Cette manche Sel ou Poivre n'existe pas.")
        return value

    def validate_menus_id(self, value):
        if value is None:
            return value
        if not Menus.objects.filter(id=value).exists():
            raise serializers.ValidationError("Cette manche Menus n'existe pas.")
        return value

    def validate_addition_id(self, value):
        if value is None:
            return value
        if not Addition.objects.filter(id=value).exists():
            raise serializers.ValidationError("Cette manche Addition n'existe pas.")
        return value

    def validate_deadly_burger_id(self, value):
        if value is None:
            return value
        if not DeadlyBurger.objects.filter(id=value).exists():
            raise serializers.ValidationError("Cette manche Burger de la mort n'existe pas.")
        return value

    def create(self, validated_data):
        nuggets_id = validated_data.pop("nuggets_id", None)
        salt_or_pepper_id = validated_data.pop("salt_or_pepper_id", None)
        menus_id = validated_data.pop("menus_id", None)
        addition_id = validated_data.pop("addition_id", None)
        deadly_burger_id = validated_data.pop("deadly_burger_id", None)

        if nuggets_id:
            validated_data["nuggets_id"] = nuggets_id
        if salt_or_pepper_id:
            validated_data["salt_or_pepper_id"] = salt_or_pepper_id
        if menus_id:
            validated_data["menus_id"] = menus_id
        if addition_id:
            validated_data["addition_id"] = addition_id
        if deadly_burger_id:
            validated_data["deadly_burger_id"] = deadly_burger_id

        return BurgerQuiz.objects.create(**validated_data)

    def update(self, instance, validated_data):
        nuggets_id = validated_data.pop("nuggets_id", None)
        salt_or_pepper_id = validated_data.pop("salt_or_pepper_id", None)
        menus_id = validated_data.pop("menus_id", None)
        addition_id = validated_data.pop("addition_id", None)
        deadly_burger_id = validated_data.pop("deadly_burger_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if nuggets_id is not None:
            instance.nuggets_id = nuggets_id
        if salt_or_pepper_id is not None:
            instance.salt_or_pepper_id = salt_or_pepper_id
        if menus_id is not None:
            instance.menus_id = menus_id
        if addition_id is not None:
            instance.addition_id = addition_id
        if deadly_burger_id is not None:
            instance.deadly_burger_id = deadly_burger_id

        instance.save()
        return instance
