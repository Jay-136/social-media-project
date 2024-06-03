from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'post',views.uploadORupdate)
router.register(r'like',views.Likeview)
router.register(r'comment',views.Commentview)


urlpatterns = [
    
    path("register/",views.Register.as_view(),name="Register"),
    path("login/",obtain_auth_token,name="login"),
    path("logout/",views.Logout,name="Logout"),
    path('',include(router.urls))
    
]

