# from mvp_rcconect.users.models import User, Link

# from .models import Event, Post
# from django.conf import settings

# import requests
# from datetime import datetime


# class EventsCollector:

#     def __init__(self, partner: User, link: Link):
#         self.partner = partner
#         self.link = link
#         GET_WALL_POSTS_URL = (f'https://api.vk.com/method/wall.get?'
#                               f'domain={link.vk_domain}&'
#                               f'v={settings.VK_API_VERSION}')
#         self.request = requests.get(
#             url=GET_WALL_POSTS_URL,
#             headers={'Authorization': f'Bearer {settings.VK_TOKEN}'}
#         )

#     def create_post(self, responce):
#         post = Post.objects.create(
#             text=post['text'],
#             partner_id=self.partner.pk,
#             post_vk_id=post['id'],
#             published_date=datetime.fromtimestamp(post['date']),
#             post_vk_url='https://vk.com/wall' +
#                         str(post['from_id']) + '_' + str(post['id']),
#         )
#         post.save()
#         return post

#     def collect_all_post_pictures(self, post, event):
#         for attachment in post['attachments']:
#             if attachment['type'] == 'photo':
#                 for size in attachment['photo']['sizes']:
#                     image = Image.objects.create(
#                         height=size['height'],
#                         width=size['width'],
#                         image_type=size['type'],
#                         url=size['url'],
#                         event_id=event.id
#                     )
#                     image.save()

#     def collect_partner_events(self):
#         last_update = self.request.json()['response']['items'][0]['date']
#         for post in self.request.json()['response']['items']:
#             if self.partner.last_update is None \
#              or post['date'] > self.partner.last_update:

#                 event = self.create_event(post)
#                 self.collect_all_post_pictures(post, event)
#                 if post['date'] > last_update:
#                     last_update = post['date']
#             else:
#                 break

#         self.partner.last_update = last_update
#         self.partner.save()


# def get_partners_event(partner: Partner):
#     """Collect last events (posts absents in db) from vk group

#     Args:
#         partner (Partner): object of Partner model
#     """

#     GET_WALL_POSTS_URL = f'https://api.vk.com/method/wall.get?domain={partner.vk_group_domain}&v={settings.VK_API_VERSION}'
#     # request to VK API
#     request = requests.get(
#         url=GET_WALL_POSTS_URL,
#         headers={'Authorization': f'Bearer {settings.VK_TOKEN}'}
#     )
#     # to find last post datetime
#     print(request.text)
#     print(request.status_code)

#     last_update = request.json()['response']['items'][0]['date']
#     for post in request.json()['response']['items']:
#         # to stop on last post from wall and in db
#         if partner.last_update is None or post['date'] > partner.last_update:
#             event = Event.objects.create(
#                 text=post['text'],
#                 partner_id=partner.id,
#                 post_vk_id=post['id'],
#                 post_vk_url='https://vk.com/wall' + str(
#                     post['from_id']) + '_' + str(post['id']),
#                 published_date=datetime.fromtimestamp(post['date']),
#             )
#             event.save()
#             if post['date'] > last_update:
#                 last_update = post['date']
#         else:
#             break
#     partner.last_update = last_update
#     print(last_update)
#     partner.save()


# def get_partners_events():
#     """
#     Get all events from all partners
#     """
#     for partner in Partner.objects.all():
#         get_partners_event(partner)
