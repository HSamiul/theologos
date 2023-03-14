from django.test import TestCase

from accounts.models import User
from .models import Profile

import datetime

class ProfileModelFormTests(TestCase):
    def setUp(self):
        User.objects.create(
            username="johns", email="johnsmith@user.com", first_name="John",
            last_name="Smith", password="foo")
        User.objects.create(
            username="janes", email="janesmith@user.com", first_name="Jane",
            last_name="Smith", password="foo")
        User.objects.create(
            username="bobs", email="bobsmith@user.com", first_name="Bob",
            last_name="Smith", password="foo")
        Profile.objects.create(
            user=User.objects.get(id=1), dob=datetime.date(1990, 1, 1),
            faith_tradition="PENT", phone="14129999999")

    # TODO: Create tests that test the validations.
    
    # def test_modelform(self):
    #     Profile.objects.create(
    #         user=self.jane, dob=datetime.date(1991, 1, 1),
    #         faith_tradition="ABC", phone="14129999999")
    #     Profile.objects.create(
    #         user=self.bob, dob=datetime.date(1992, 1, 1),
    #         faith_tradition="PENT", phone="abc")
