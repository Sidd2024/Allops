from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('/Allops/images/favico.ico'))),
    path('', views.index, name="index"),
    path('signup',views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout',views.signout, name="signout"),
    path('Type/<str:type>',views.get_opportunities, name="get_opportunities"),
    path('opportunity/<int:item_id>', views.activity, name="activity"),
    path('save_it/<int:item_id>', views.save_it, name="save_it"),
    path('saved',views.saved,name="saved"),
    path('share',views.share,name="share"),
    path('profile',views.profile,name="profile"),
    path('mails',views.activate_mails,name="mails"),
    path('validate',views.validate_mail,name="validate")

]
