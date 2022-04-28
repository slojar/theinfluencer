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
    if response['first_name']:
        user.first_name = response['first_name']
    if response['last_name']:
        user.last_name = response['last_name']
    if response['email']:
        user.email = response['email']
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    if response['id']:
        profile.uid = response['id']
    if response['birthday']:
        profile.dob = response['birthday']
    if response['gender']:
        profile.gender = response['gender']
    if response['middle_name']:
        profile.middle_name = response['middle_name']
    if response['hometown']['name']:
        profile.hometown = response['hometown']['name']
    if response['picture']['data']['url']:
        profile.profile_picture = response['picture']['data']['url']
    if response['location']['name']:
        profile.location = response['location']['name']
    profile.save()

    account = []
    if response['accounts']['data']:
        account = response['accounts']['data']
    for data in account:
        page, _ = Page.objects.get_or_create(profile=profile, page_uid=data['id'])
        if data['name']:
            page.name = data['name']
        if data['about']:
            page.about = data['about']
        if data['access_token']:
            page.page_token = data['access_token']
        if data['picture']['data']['url']:
            page.page_picture = data['picture']['data']['url']
        if data['category']:
            page.category = data['category']
        if data['followers_count']:
            page.followers = data['followers_count']
        if data['fan_count']:
            page.fans = data['fan_count']
        if data['new_like_count']:
            page.likes = data['new_like_count']
        if data['has_whatsapp_number']:
            page.has_whatsapp_number = data['has_whatsapp_number']
        if data['whatsapp_number']:
            page.whatsapp_number = data['whatsapp_number']
        if data['link']:
            page.page_link = data['link']
        page.save()

    return True



