from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()


class UserSerializer(ModelSerializer):
    profile_image = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'profile_image',
            'username',
            'email',
        )

    def get_profile_image(self, obj):
        if (profile_image := obj.profile_image):
            return profile_image.url
        else:
            return None


class CustomUserDetailSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            'id',
            'profile_image',
            'username',
            'email',
        )

    def update(self, instance, validated_data):
        """
        Note:
            change this method if you want to update user model.
            in the case of this application this is not needed because
            it already uses CustomUser. However it is worth keeping memo.
        """
        return super().update(instance, validated_data)
