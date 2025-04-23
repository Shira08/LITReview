from django.shortcuts import render,redirect
from ticket import forms
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