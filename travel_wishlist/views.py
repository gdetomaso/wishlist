from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

def place_list(request):

    """
    View to show all places in the wishlist. If the request is a POST, 
    it means the user has submitted a new place, so validate the form, save it, 
    and redirect back to this view.
    """
    if request.method == 'POST':
        form = NewPlaceForm (request.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(visited=False).order_by("name")
    new_place_form = NewPlaceForm()
    return render(request, "travel_wishlist/wishlist.html" , {"places": places, "new_place_form": new_place_form}) 


def places_visited(request):
    
    """
    View to display all places that have been visited. 
    Retrieves places marked as visited from the database 
    and renders them in the 'visited.html' template.
    """
    visited = Place.objects.filter(visited=True)
    return render(request, "travel_wishlist/visited.html", {"visited": visited})

def place_was_visited(request, place_pk):
    """
    View to mark a place as visited. If the request is a POST 
    the user has marked a place as visited so update the place in the
    database and redirect back to the "place_list" view.
    """
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    
    return redirect("place_list")

def about(request):
    author = "Giovanni"
    about = "Travel Wishlist website for learning Django"
    return render(request, "travel_wishlist/about.html", {"author": author, "about": about})