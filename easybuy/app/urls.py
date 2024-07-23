from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm , MySetPasswordForm
from . import views

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', show_cart, name='showcart'),
    path('search/', search, name='search'),
    path('pluscart/', plus_cart, name='pluscart'),
    path('minuscart/', minus_cart, name='pluscart'),
    path('removecart/', remove_cart, name='removecart'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('wishlist/', show_wishlist, name='wishlist'),
    path('remove_wishlist/', remove_wishlist, name='remove_wishlist'),
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('orders/', orders, name='orders'),
    path('kids/', kids, name='kids'),
    path('kids/<str:data>/', kids, name='kidsdata'),
    path('womens_wear/', womens_wear, name='womens_wear'),
    path('womens_wear/<str:data>/', womens_wear, name='womens_wear_data'),
    path('mens_wear/', mens_wear, name='mens_wear'),
    path('mens_wear/<str:data>/', mens_wear, name='mens_wear_data'),
    path('account/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm, next_page='address'), name='login'),
   
    path('account/logout/',views.logout_view,name="logout"),
    path('account/passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class= MyPasswordChangeForm, success_url='/account/passwordchangedone/'), name='passwordchange'),
    path('account/passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class= MyPasswordResetForm), name='password_reset'),
    path('passwordresetconfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('passwordreset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    path('passwordreset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetconfirm.html'),name='password_reset_confirm'),
    path('registration/', CustumerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', checkout, name='checkout'),
    path('paymentdone/', paymentdone, name='paymentdone'),

]   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
