import re
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

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

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        actual_html = self.fix_html(response.content.decode())
        self.assertEqual(actual_html, expected_html)
