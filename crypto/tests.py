from django.test import SimpleTestCase
from django.urls import resolve, reverse


class FeaturesUrlTests(SimpleTestCase):
    def test_features_url_resolves(self):
        url = reverse("features")
        self.assertEqual(url, "/features/")
        self.assertEqual(resolve(url).view_name, "features")
