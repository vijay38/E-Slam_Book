from django.urls import path,re_path

from . import views

urlpatterns = [
    # path("fillupform",views.home,name="home"),
    path("nextstep/<str:id>",views.thanks,name="thanks"),
    path('fillupform/<str:id>/',views.homes,name='redirect')
]
