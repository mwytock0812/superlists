import re
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.models import Item

from lists.views import home_page

class HomePageTest(TestCase):

    def fix_html(self, messy_html):
        messy_html = re.sub(r"<input type='hidden'.*", "", messy_html)
        return messy_html


    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  # check site root
        self.assertEqual(found.func, home_page)  # find home_page fxn


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        actual_html = self.fix_html(response.content.decode())
        self.assertEqual(actual_html, expected_html)


    def test_home_page_can_save_a_POST_reqest(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertEqual(response.status_code, 302)  # HTTP redirect
        self.assertEqual(response['location'], '/')


    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
