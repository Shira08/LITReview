from django.shortcuts import render,redirect
from ticket import forms
from authentication import models
from follower import models
#from review.forms import ReviewForm
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

def get_users(request):
    """We collect all the users to whom the user is subscribed"""
    users = []
    users_follows = models.UserFollows.objects.filter(user=request.user)
    for user in users_follows:
        users.append(user.followed_user)
    users.append(request.user)
    return users

def get_reviews(request, users):
    """we collect all the reveiws of the users to whom we are subscribed"""
    reviews = []
    for user in users:
        review_by_user = models.Review.objects.filter(user=user).order_by('-time_created')
        for review in review_by_user:
            reviews.append(review)
    reviews = sorted(reviews, key=lambda k: k.time_created, reverse=True)
    return reviews


def get_tickets(request, users):
    """we collect all the tickets of the users to whom we are subscribed"""
    tickets = []
    for user in users:
        tickets_by_user = models.Ticket.objects.filter(author=user)
        for ticket in tickets_by_user:
            tickets.append(ticket)
    tickets = sorted(tickets, key=lambda k: k.time_created, reverse=True)
    return tickets

def sorted_posts(request, tickets, reviews):
    posts = []
    for ticket in tickets:
        posts.append(ticket)
    for review in reviews:
        posts.append(review)
    posts = sorted(posts, key=lambda k: k.time_created, reverse=True)
    return posts

@login_required
def posts(request):
    users = get_users(request)
    tickets = get_tickets(request, users)
    reviews = get_reviews(request, users)
    posts = sorted_posts(request, tickets, reviews)
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