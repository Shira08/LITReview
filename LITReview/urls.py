"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import ticket.views
import review.views
import follower.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page,name="login"),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('flux/', ticket.views.feed, name='flux'),
    path('posts/', ticket.views.posts, name='posts'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('create-ticket/', ticket.views.create_ticket, name='create-ticket'),
    path('create-ticket-review/', review.views.create_ticket_review, name='create-ticket-review'),
    path('create-review-response/<int:id>/', review.views.create_review_response, name='create-review-response'),
    path('update-review/<int:id>/<int:review_id>', review.views.create_review_response, name='update-review-response'),
    path('review/delete/<int:id>/', review.views.review_delete, name='rewiew_delete'),
    path('follows/', follower.views.follows, name='follows'),
    path('unfollow/<int:link_id>/', follower.views.unfollow, name='unfollow'),
    path('ticket/update/<int:ticket_id>/', ticket.views.update_ticket, name='ticket_update'),
    path('ticket/delete/<int:id>/', ticket.views.ticket_delete, name='ticket_delete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)