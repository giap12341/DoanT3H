from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from . forms import CustomLoginForm,MypasswordResetForm
urlpatterns = [
    path('',views.home.as_view(),name ="home"), # Trang chủ
    # path('danh-sach-san-pham/<str:val>/',views.product,name = 'product'),
    path('san-pham/<str:val>',views.product_detail.as_view(),name="product_detail"), # Một sản phẩm
    path('danh-sach-san-pham/<str:val>/',views.PaginationViewProduct.as_view(),name='pagination_product'), #Danh sách sản phẩm theo loại
    path('profile/',views.ProfileView.as_view(),name = 'profile'),
    path('adress/',views.Adress.as_view(),name = 'adress'),
    
    
    # ******************************************************************************************************
    path('dang-ki/',views.CustomRegister.as_view(),name='CustomRegisterView'), # Đăng kí
   
    path('dang-nhap/',auth_view.LoginView.as_view(template_name = 'myapp/login.html',authentication_form = CustomLoginForm),name='login'), # Đăng nhập
    path('reset-mat-khau/',auth_view.LoginView.as_view(template_name = 'myapp/resetpassword.html',authentication_form = MypasswordResetForm),name='resetpassword'), # Quên mật khẩu
    
    # path('dang-xuat/',views.LogoutView.as_view(),name='logout') # Đăng xuất
]
