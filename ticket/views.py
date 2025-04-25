from django.shortcuts import render, redirect, get_object_or_404
from ticket import forms, models
from authentication import models as auth_models
from follower import models as follower_models
from review.forms import ReviewForm
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


def get_tickets(request):
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
#    users = get_users(request)
    tickets = models.Ticket.objects.filter(author=request.user,delete=False) 
    context = {'tickets': tickets}
    return render(request, 'ticket/posts.html', context)


def delete(request, id):
    ticket = ticket.objects.get(id=id)
    return render(request,
           'ticket/posts.html',{'band': band})



"""def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id) 
    if request.method == 'POST':

        ticket.delete()
        return redirect('posts')

    return render(request,
                    'ticket/posts.html',
                    {'ticket': ticket})"""
def ticket_delete(request, id):
    ticket = get_object_or_404(models.Ticket, id=id)

    if request.method == 'POST':
        ticket.delete = True  
        ticket.save()
        return redirect('posts')  

    return render(request, 'ticket/confirm_delete.html', {'ticket': ticket})


def ticket_update(request, id):
    ticket = models.Ticket.objects.get(id=id)
    form = TicketForm(instance=band) 
    return render(request,'listings/band_update.html',{'form': form})

def ticket_update(request, id):
    ticket = models.Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request,
                'ticket/ticket_update.html',
                {'form': form})
