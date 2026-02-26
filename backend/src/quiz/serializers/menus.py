from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Menus, MenuTheme


class MenusSerializer(ModelSerializer):
    menu_1_id = serializers.UUIDField(write_only=True, required=False)
    menu_2_id = serializers.UUIDField(write_only=True, required=False)
    menu_troll_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Menus
        fields = ["id", "title", "description", "original", "menu_1", "menu_2", "menu_troll", "menu_1_id", "menu_2_id", "menu_troll_id"]
        read_only_fields = ["id", "menu_1", "menu_2", "menu_troll"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    def validate_menu_1_id(self, value):
        if value is None:
            return value
        try:
            theme = MenuTheme.objects.get(id=value)
        except MenuTheme.DoesNotExist:
            raise serializers.ValidationError("Ce thème de menu n'existe pas.")
        if theme.type != "CL":
            raise serializers.ValidationError("menu_1 doit être un thème classique (CL).")
        return value

    def validate_menu_2_id(self, value):
        if value is None:
            return value
        try:
            theme = MenuTheme.objects.get(id=value)
        except MenuTheme.DoesNotExist:
            raise serializers.ValidationError("Ce thème de menu n'existe pas.")
        if theme.type != "CL":
            raise serializers.ValidationError("menu_2 doit être un thème classique (CL).")
        return value

    def validate_menu_troll_id(self, value):
        if value is None:
            return value
        try:
            theme = MenuTheme.objects.get(id=value)
        except MenuTheme.DoesNotExist:
            raise serializers.ValidationError("Ce thème de menu n'existe pas.")
        if theme.type != "TR":
            raise serializers.ValidationError("menu_troll doit être un thème troll (TR).")
        return value

    def validate(self, attrs):
        menu_1_id = attrs.get("menu_1_id")
        menu_2_id = attrs.get("menu_2_id")
        menu_troll_id = attrs.get("menu_troll_id")

        # Vérifier que les 3 IDs sont distincts (si fournis)
        ids = [mid for mid in [menu_1_id, menu_2_id, menu_troll_id] if mid is not None]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError("Les trois thèmes de menu doivent être distincts.")

        return attrs

    def create(self, validated_data):
        menu_1_id = validated_data.pop("menu_1_id", None)
        menu_2_id = validated_data.pop("menu_2_id", None)
        menu_troll_id = validated_data.pop("menu_troll_id", None)

        if menu_1_id:
            validated_data["menu_1_id"] = menu_1_id
        if menu_2_id:
            validated_data["menu_2_id"] = menu_2_id
        if menu_troll_id:
            validated_data["menu_troll_id"] = menu_troll_id

        return Menus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        menu_1_id = validated_data.pop("menu_1_id", None)
        menu_2_id = validated_data.pop("menu_2_id", None)
        menu_troll_id = validated_data.pop("menu_troll_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if menu_1_id is not None:
            instance.menu_1_id = menu_1_id
        if menu_2_id is not None:
            instance.menu_2_id = menu_2_id
        if menu_troll_id is not None:
            instance.menu_troll_id = menu_troll_id

        instance.save()
        return instance
