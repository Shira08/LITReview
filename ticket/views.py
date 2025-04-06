from django.shortcuts import render,redirect
from ticket import forms
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'ticket/flux.html')

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.photo = photo
            ticket.save()
            return redirect('flux')
    context = {'ticket_form': ticket_form,
               'photo_form': photo_form, 
               'page_name': 'Créer un ticket'}
    return render(request, 'ticket/create_ticket.html', context=context)


@login_required
def posts(request):
    users = get_users(request)
    tickets = get_tickets(request, users)
    #reviews = get_reviews(request, users)
    #posts = sorted_posts(request, tickets, reviews)
    message = "Vous n'avez pas encore de publications"
    for post in posts:
        try:
            if post.user == request.user:
                message = None
        except Exception:
            pass
        try:
            if post.author == request.user:
                message = None
        except Exception:
            pass
    context = {'posts': posts, 'message': message, 'page_name': 'Posts'}
    return render(request, 'ticket/posts.html', context)