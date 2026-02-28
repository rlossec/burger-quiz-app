from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer

from ..models import BurgerQuiz, Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger
from .base import AuthorSerializer
from .nugget import NuggetsSerializer
from .salt_or_pepper import SaltOrPepperSerializer
from .menus import MenusSerializer
from .addition import AdditionSerializer
from .deadly_burger import DeadlyBurgerSerializer
from .burger_quiz_element import BurgerQuizElementReadSerializer


class BurgerQuizSerializer(TaggitSerializer, ModelSerializer):
    nuggets_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    salt_or_pepper_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    menus_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    addition_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    deadly_burger_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    nuggets = NuggetsSerializer(read_only=True)
    salt_or_pepper = SaltOrPepperSerializer(read_only=True)
    menus = MenusSerializer(read_only=True)
    addition = AdditionSerializer(read_only=True)
    deadly_burger = DeadlyBurgerSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)
    structure = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BurgerQuiz
        fields = [
            "id",
            "title",
            "toss",
            "author",
            "tags",
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
            "structure",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "updated_at",
            "nuggets",
            "salt_or_pepper",
            "menus",
            "addition",
            "deadly_burger",
            "structure",
        ]
        extra_kwargs = {
            "toss": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    @extend_schema_field(BurgerQuizElementReadSerializer(many=True))
    def get_structure(self, obj):
        """Retourne la structure ordonnée du Burger Quiz."""
        elements = obj.structure_elements.all().order_by("order")
        return BurgerQuizElementReadSerializer(elements, many=True).data

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
        tags = validated_data.pop("tags", None)

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

        if tags is not None:
            instance.tags.set(tags)

        return instance
