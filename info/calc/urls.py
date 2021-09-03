from django.urls import path

from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('onmap/',views.mapon,name='map'),
    path('efficiency/',views.home_efficiency,name='efficiency'),
    path('performance/',views.home_performance,name='performance'),
    path("management/",views.home_cap,name="home"),
    path("optimization/",views.home_opt,name="optimization"),
    path("capacity/",views.port_capacity,name="capacity"),
    path("optimise/",views.optimise,name="optimise"),
]