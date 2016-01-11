from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    """Returns home.html when an HttpRequest object is received."""
    return render(request, 'home.html')


def view_list(request, list_id):
    """Returns list.html showing the list corresponding to list_id."""
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """Creates a new list with one item and redirects to that list view."""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


def add_item(request, list_id):
    """Adds item to an existing list and redirects to that list view."""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
