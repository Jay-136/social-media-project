from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'post',views.Postview)
router.register(r'like',views.Likeview)
router.register(r'comment',views.Commentview)


urlpatterns = [
    
    path("register/",views.Register.as_view(),name="Register"),
    path("login/",views.LogIn.as_view(),name="login"),
    path("logout/",views.Logout.as_view(),name="Logout"),
    path('unlike/', views.remove_like, name='unlike'),
    path('',include(router.urls))
    
]

