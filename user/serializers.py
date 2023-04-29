from rest_framework import serializers

from user.models import User, UserFollowing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_staff', 'avatar', 'bio')
        read_only_fields = ('is_staff', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creating user with encrypted password"""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updating user with correct changing of password"""
        password = validated_data.pop('password', None)
        user = super(UserSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('following', 'follower')


class UserFollowerListSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ('follower', )


class UserFollowingListSerializer(serializers.ModelSerializer):
    following = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ('following', )
