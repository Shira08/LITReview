from django.shortcuts import render, redirect, get_object_or_404
from ticket import  forms as TicketForm, models
from review import forms, models
from authentication import models as auth_models
from follower import models as follower_models
from review.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render
from django.db.models import Q



@login_required
def home(request):
    return render(request, 'ticket/flux.html')

@login_required
def create_ticket(request):
    ticket_form = TicketForm.TicketForm()
    photo_form = TicketForm.PhotoForm()
    if request.method == 'POST':
        ticket_form = TicketForm.TicketForm(request.POST)
        photo_form = TicketForm.PhotoForm(request.POST, request.FILES)
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

def get_users_viewable_tickets(user):
    followed_users = user.following.all().values_list('followed_user', flat=True)
    return models.Ticket.objects.filter(
        Q(author__in=followed_users) | Q(author=user)
    )


def get_users_viewable_reviews(user):
    followed_users = user.following.all().values_list('followed_user', flat=True)

    # billets que j'ai créés
    my_tickets = models.Ticket.objects.filter(author=user)

    return models.Review.objects.filter(
        Q(user=user) |
        Q(user__in=followed_users) |
        Q(ticket__in=my_tickets)
    )


@login_required
def feed(request): 
    user = request.user

    tickets = get_users_viewable_tickets(user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        tickets,
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'ticket/flux.html', context={'posts': posts})

@login_required
def posts(request):
#    users = get_users(request)
    tickets = models.Ticket.objects.filter(author=request.user,delete=False) 
    context = {'tickets': tickets}
    return render(request, 'ticket/posts.html', context)


def ticket_delete(request, id):
    ticket = get_object_or_404(models.Ticket, id=id)

    if request.method == 'POST':
        ticket.delete = True  
        ticket.save()
        return redirect('posts')  

    return render(request, 'ticket/confirm_delete.html', {'ticket': ticket})


@login_required
def update_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    ticket_form = TicketForm.TicketForm(instance=ticket)
    photo_form = TicketForm.PhotoForm(instance=ticket.photo)
    if request.method == 'POST':
        ticket_form = TicketForm.TicketForm(request.POST, instance=ticket)
        photo_form = TicketForm .PhotoForm(request.POST, request.FILES, instance=ticket.photo)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.photo = photo
            ticket.save()
            return redirect('posts')
    context = {'ticket_form': ticket_form, 'photo_form': photo_form,
               'page_name': 'Ticket update'}
    return render(request, 'ticket/update_ticket.html', context)
