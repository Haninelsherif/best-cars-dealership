from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns=[
 path("admin/",admin.site.urls),
 path("",home), path("about/",about), path("contact/",contact),
 path("loginuser/",loginuser), path("logoutuser/",logoutuser), path("register/",register),
 path("getalldealers/",getalldealers), path("getdealerbyid/<int:dealer_id>/",getdealerbyid),
 path("getdealersbyState/<str:state>/",getdealersbyState), path("getdealerreviews/<int:dealer_id>/",getdealerreviews),
 path("getallcarmakes/",getallcarmakes), path("analyzereview/<str:text>/",analyzereview),
] 
