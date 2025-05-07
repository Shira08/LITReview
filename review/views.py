from django.shortcuts import render,redirect,get_object_or_404
from ticket import forms,models
from review import models
from review.forms import ReviewForm
from django.contrib.auth.decorators import login_required


@login_required
def create_ticket_review(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), photo_form.is_valid(),review_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.photo = photo
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')
        
    context = {
               'ticket_form': ticket_form,
               'photo_form': photo_form, 
               'review_form': review_form
               }
    return render(request, 'review/create_review.html',context = context) 


@login_required
def create_review_response(request,id):
    ticket = get_object_or_404(models.Ticket, id=id)
    review_form = ReviewForm(request.POST)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')
        
    context = {
               'ticket' : ticket,
               'review_form': review_form,
               'user': request.user
               }
    return render(request, 'review/create_review_response.html',context = context) 

@login_required
def update_review_response(request, id, review_id):
    ticket = get_object_or_404(models.Ticket, id=id)
    review = get_object_or_404(models.Review, id=review_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            updated_review = review_form.save(commit=False)
            updated_review.user = request.user
            updated_review.ticket = ticket
            updated_review.save()
            return redirect('flux')
    else:
        review_form = ReviewForm(instance=review)

    context = {
        'ticket': ticket,
        'review_form': review_form,
        'review': review,
    }
    return render(request, 'review/create_review_response.html', context)


@login_required
def review_delete(request, id):
    review = get_object_or_404(models.Review, id=id)

    if request.method == "POST":
        review.delete()
        return redirect('flux') 

    return render(request, 'ticket/flux.html', {'review': review})
