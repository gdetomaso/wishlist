from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request):

    """
    View to show all places in the wishlist. If the request is a POST, 
    it means the user has submitted a new place, so validate the form, save it, 
    and redirect back to this view.
    """
    if request.method == 'POST':
        form = NewPlaceForm (request.POST)
        place = form.save(commit=False)
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by("name")
    new_place_form = NewPlaceForm()
    return render(request, "travel_wishlist/wishlist.html" , {"places": places, "new_place_form": new_place_form}) 

@login_required
def places_visited(request):
    
    """
    View to display all places that have been visited. 
    Retrieves places marked as visited from the database 
    and renders them in the 'visited.html' template.
    """
    visited = Place.objects.filter(visited=True)
    return render(request, "travel_wishlist/visited.html", {"visited": visited})
@login_required
def place_was_visited(request, place_pk):
    """
    View to mark a place as visited. If the request is a POST 
    the user has marked a place as visited so update the place in the
    database and redirect back to the "place_list" view.
    """
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect("place_list")

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    #return render(request, "travel_wishlist/place_detail.html", {"place": place})

    #checks if place belongs to user
    if place.user != request.user:
        return HttpResponseForbidden()
    
    #if POST requests validate form data then update
    if request.method == "POST":
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, "Trip Information updated")
        else:
            messages.error(request, form.errors)
        return redirect("place_details", place_pk=place_pk)
    #if GET request show Place info and form
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, "travel_wishlist/place_detail.html", {"place": place, "review_form": review_form})
        else:
            return render(request, "travel_wishlist/place_detail.html", {"place": place})
        
@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect("place_list")
    else:
        return HttpResponseForbidden()
    



def about(request):
    author = "Giovanni"
    about = "Travel Wishlist website for learning Django"
    return render(request, "travel_wishlist/about.html", {"author": author, "about": about})