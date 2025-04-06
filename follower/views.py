from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from follower import forms
from follower import models
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
def follows(request):
    form = forms.UserFollowsForm()
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    follows = models.UserFollows.objects.filter(user=request.user)
    error = None
    
    if request.method == 'POST':
        form = forms.UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            if username != request.user.username:
                try:
                    followed_user = User.objects.get(username=username)
                    
                    existing = models.UserFollows.objects.filter(
                        user=request.user, 
                        followed_user=followed_user
                    ).exists()
                    
                    if existing:
                        error = "Vous suivez déjà cet utilisateur"
                    else:
                        add_follower = models.UserFollows(
                            user=request.user, 
                            followed_user=followed_user
                        )
                        add_follower.save()
                        return redirect('follows')
                except User.DoesNotExist:
                    error = "Désolé ce compte utilisateur n'existe pas"
            else:
                error = 'Désolé vous ne pouvez pas vous auto-abonner'
    
    context = {
        'form': form, 
        'followers': followers,
        'follows': follows, 
        'page_name': 'Abonnements', 
        'error': error
    }
    return render(request, 'follower/follows.html', context=context)




@login_required
def unfollow(request, link_id):
    link = models.UserFollows.objects.get(id=link_id)
    link.delete()
    return redirect('follows')

