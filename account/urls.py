from django.urls import path
from .views import register, dashboard, edit_account, users_list, get_user, user_follow
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # old login view
    #path('login/', sign_in, name='sign_in')
    path('login/', views.LoginView.as_view(), name='sign_in'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('change_password/done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password_rest', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register', register, name='register'),
    path('edit', edit_account, name='edit_account'),
    path('users', users_list, name='users_list'),
    path('users/<username>', get_user, name='user_details'),
    path('users/follow', user_follow, name='user_follow')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)