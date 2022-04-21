import logging

import requests
from django.conf import settings
from .models import Profile, Page


BASE_URL = settings.FACBOOK_BASE_URL
FIELDS = settings.FACEBOOK_USER_DETAIL_FIELDS
TRANSPORT = 'cors'


def log_request(*args):
    for arg in args:
        logging.info(arg)


def get_user_detail(uid, access_token):
    url = f'{BASE_URL}/{uid}?fields={FIELDS}&transport={TRANSPORT}&access_token={access_token}'

    response = requests.request('GET', url).json()
    log_request(url, response)
    return response


def update_user_profile(response, user):
    user.first_name = response['first_name']
    user.last_name = response['last_name']
    user.email = response['email']
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.uid = response['id']
    profile.dob = response['birthday']
    profile.gender = response['gender']
    profile.middle_name = response['middle_name']
    profile.hometown = response['hometown']['name']
    profile.profile_picture = response['picture']['data']['url']
    profile.location = response['location']['name']
    profile.save()

    account = response['accounts']['data']
    for data in account:
        page, _ = Page.objects.get_or_create(profile=profile, page_uid=data['id'])
        page.name = data['name']
        page.about = data['about']
        page.page_token = data['access_token']
        page.page_picture = data['picture']['data']['url']
        page.category = data['category']
        page.followers = data['followers_count']
        page.fans = data['fan_count']
        page.likes = data['new_like_count']
        page.has_whatsapp_number = data['has_whatsapp_number']
        page.whatsapp_number = data['whatsapp_number']
        page.page_link = data['link']
        page.save()

    return True



