from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from api.models import Users, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed representation of a Users Profile.
    """

    class Meta:
        model = UserProfile
        fields = ["id", "bio", "address", "website"]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed representation of a User,
    including their Profile.
    """

    profile = ProfileSerializer()  # associated profile using ProfileSerializer.

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "email",
            "profile",
            "created_at",
            "modified_at",
            "last_login",
            "is_active",
            "is_staff",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
            "last_login",
            "is_active",
            "is_staff",
        ]

    def update(self, instance, validated_data):
        """
        Update the user instance with validated data.

        Return Type -> dict():
        # dict: The updated validated data.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        profile = UserProfile.objects.get(user=instance)

        profile_data = validated_data.get("profile", {})

        profile.bio = profile_data.get("bio", profile.bio)
        profile.address = profile_data.get("address", profile.address)
        profile.website = profile_data.get("website", profile.website)
        profile.save()

        return validated_data
