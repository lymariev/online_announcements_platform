import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Announcement, Category
from .serializers import AnnouncementSerializer


class AnnouncementListCreateAPIViewTestCase(APITestCase):
    url = reverse("bulletin_board:announcement-list")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.parent_category = Category.objects.create(name='Appliances')
        self.category = Category.objects.create(name='Refrigerators', parent=self.parent_category)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_announcement(self):
        response = self.client.post(self.url, {"name": "Whirlpool Stainless Steel Large",
                                               "description": "Great condition frost free with excellent energy rating",
                                               "price": "140.00",
                                               "price_is_negotiable": True,
                                               "category": self.category.pk})
        self.assertEqual(201, response.status_code)

    def test_user_announcements(self):
        Announcement.objects.create(name="Fridge Indesit", description='2-door fridge Indesit.',
                                    price=80.0, price_is_negotiable=False, category=self.category, author=self.user)
        response = self.client.get(self.url)
        self.assertTrue(len(response.json()['results']) == Announcement.objects.count())

    def test_user_favorites_list(self):
        announcement = Announcement.objects.create(name="Fridge Indesit", description='2-door fridge Indesit.',
                                                   price=80.0, price_is_negotiable=False, category=self.category,
                                                   author=self.user)
        announcement.in_favorites.add(self.user)
        response = self.client.get(self.url + 'favorites/')
        self.assertTrue(len(response.json()) == announcement.in_favorites.count())


class AnnouncementDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.parent_category = Category.objects.create(name='Appliances')
        self.category = Category.objects.create(name='Refrigerators', parent=self.parent_category)
        self.announcement = Announcement.objects.create(name="Fridge Indesit", description='2-door fridge Indesit.',
                                                        price="80.00", price_is_negotiable=False, category=self.category,
                                                        author=self.user)
        self.url = reverse("bulletin_board:announcement-detail", kwargs={"pk": self.announcement.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_announcement_object_bundle(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        announcement_serializer_data = AnnouncementSerializer(instance=self.announcement).data
        response_data = json.loads(response.content)
        self.assertEqual(announcement_serializer_data, response_data)

    def test_announcement_object_update_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        response = self.client.put(self.url, {"name": "Fridge Bosch"})
        self.assertEqual(403, response.status_code)

    def test_announcement_object_update(self):
        response = self.client.put(self.url, {"name": "Fridge Bosch",
                                              "description": "Great condition frost free with excellent energy rating",
                                              "price": "140.00",
                                              "price_is_negotiable": True,
                                              "category": self.category.pk})
        response_data = json.loads(response.content)
        announcement = Announcement.objects.get(id=self.announcement.id)
        self.assertEqual(response_data.get("name"), announcement.name)

    def test_announcement_object_delete_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_announcement_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_user_add_favorite(self):
        count_after_add = self.user.in_favorites.count()
        self.client.post(self.url + 'add-to-favorites/')
        self.assertEqual(count_after_add + 1, self.user.in_favorites.count())

    def test_user_delete_favorite(self):
        self.client.post(self.url + 'add-to-favorites/')
        count_after_add = self.user.in_favorites.count()
        self.client.delete(self.url + 'delete-from-favorites/')
        self.assertEqual(count_after_add - 1, self.user.in_favorites.count())
