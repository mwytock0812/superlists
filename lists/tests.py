import re
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def fix_html(self, messy_html):
        """
        Replace input tags with type='hidden' with ''.

        Replace hidden input tags with empty string so that pages
        with csrf tokens can be compared in tests.
        """
        messy_html = re.sub(r"<input type='hidden'.*", "", messy_html)
        return messy_html

    def test_root_url_resolves_to_home_page_view(self):
        """Test that resolving root brings up home page view."""
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        Test that request to home page returns correct HTML.

        Passes an HTTP request to the home_page view. Then,
        checks that the string-rendered template matches
        the actual HTTP response.
        """
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        actual_html = self.fix_html(response.content.decode())
        self.assertEqual(actual_html, expected_html)


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        """
        Test that text can be added to item model and saved to a list.

        Creates a list and save it. Then, creates two items linked to
        the list. Finally, the test checks for expected text and
        the correct number of items in the list.
        """
        list_ = List()  # use 'list_' to avoid built-in clash
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_passes_correct_list_to_template(self):
        """
        Test that a list's ID can be used in a URL to view the list.

        The function creates two lists. Then, it uses one list's ID
        in a request to verify that the template context that is
        generated contains the correct list object.
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        """Test that a request for a list returns the correct template."""
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        """Test that a request for a list returns only that list's contents."""
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        print(response)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


class NewListTest(TestCase):

    def test_saving_a_POST_reqest(self):
        """
        Test that a POST request to '/lists/new' saves an item to a new list.

        The client posts the desired item_text to '/lists/new', which
        the URLConf parses and passes to the new_list view.
        """
        self.client.post(
            '/lists/new',  # 'action' URL, so no trailing '/'
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        Test that a redirect updates the page after making a new list.

        After the text is added to the new list, the function tests
        that the new_list view returns a redirect.
        """
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Tests that adding an item to an exist list works."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """Tests that the add_item view function returns a redirect."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
