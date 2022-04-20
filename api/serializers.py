from rest_framework import serializers
from .models import Profile, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    pages = serializers.SerializerMethodField()

    def get_pages(self, obj):
        page = None
        if Page.objects.filter(profile=obj).exists():
            page = PageSerializer(Page.objects.filter(profile=obj), many=True).data
        return page

    class Meta:
        model = Profile
        exclude = []


