from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns=[
 path("admin/",admin.site.urls),
 path("",home), path("about/",about), path("contact/",contact),
 path("djangoapp/login",loginuser), path("djangoapp/logout",logoutuser),
 path("djangoapp/register",register),
 path("djangoapp/get_dealers",getalldealers),
 path("djangoapp/fetchDealer/<int:dealer_id>",getdealerbyid),
 path("djangoapp/get_dealers/<str:state>",getdealersbyState),
 path("djangoapp/reviews/dealer/<int:dealer_id>",getdealerreviews),
 path("djangoapp/add_review",addreview),
 path("djangoapp/get_cars",getallcarmakes),
 path("analyze/<str:text>",analyzereview),
 path("getallcarmakes/",getallcarmakes),
 path("analyzereview/<str:text>/",analyzereview),
]