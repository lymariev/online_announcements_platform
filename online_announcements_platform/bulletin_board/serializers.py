from rest_framework import serializers
from .models import Announcement, AnnouncementImage, Category
from django.conf import settings


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    parent_category = ParentCategorySerializer(source='parent')

    class Meta:
        model = Category
        fields = ('parent_category', 'id', 'name')


class AnnouncementImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = AnnouncementImage
        fields = ('id', 'image')


class AnnouncementSerializer(serializers.ModelSerializer):
    images = AnnouncementImageSerializer(source='announcementimage_set', many=True, required=False)
    author_username = serializers.SlugRelatedField(source='author', slug_field='username', read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Announcement
        fields = ('id', 'name', 'description', 'price', 'price_is_negotiable',
                  'category', 'images', 'author_username', 'author')

    def validate(self, data):
        images = list(self.context.get('view').request.FILES.values())
        if len(images) > settings.MAX_ANNOUNCEMENT_IMAGES:
            raise serializers.ValidationError("Invalid number of images")
        return data

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        announcement = Announcement.objects.create(
            name=validated_data.pop('name'), description=validated_data.pop('description'),
            price=validated_data.pop('price'), price_is_negotiable=validated_data.pop('price_is_negotiable'),
            category=validated_data.pop('category'), author=validated_data.pop('author')
        )
        for image_data in images_data.values():
            announcement_image = AnnouncementImage.objects.create(announcement=announcement)
            announcement_image.image.save(image_data.name, image_data)
        return announcement

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.description)
        instance.price_is_negotiable = validated_data.get('price_is_negotiable', instance.price_is_negotiable)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        AnnouncementImage.objects.filter(announcement=instance).delete()
        for image_data in images_data.values():
            announcement_image = AnnouncementImage.objects.create(announcement=instance)
            announcement_image.image.save(image_data.name, image_data)
        return instance
