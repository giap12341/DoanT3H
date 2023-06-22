# from typing import Any, Dict
from django.shortcuts import redirect, render
from .models import Product, Profile
from django.views import View   
from .forms import CustomUserCreationForm,CustomLoginForm,MyProfileForm
from django.contrib import messages
from .serializers import ProductSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
# Create your views here.
# product_list = Product.objects.all()
# ***************************************************** TRANG CHỦ ****************************************************
class home(View):
    def get(self, request):
        phone_list = Product.objects.filter(category=2).order_by('id')[:3]
        laptop_list = Product.objects.filter(category=1).order_by('id')[:3]
        tablet_list = Product.objects.filter(category=4).order_by('id')[:3]
        phukien_list = Product.objects.filter(category=3).order_by('id')[:3]
        return render(request,'myapp/home.html',{"phone_list":phone_list,"laptop_list":laptop_list,"tablet_list":tablet_list,"phukien_list":phukien_list})

class product_detail(View):
    def get(self,request,val):
        product = Product.objects.filter(id=val).first()
        serializer_product = ProductSerializer(product)
        return render(request,'myapp/product_detail.html',{"product":serializer_product.data})
# ********************************************** ĐĂNG KÍ *****************************************************
class CustomRegister(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request,'myapp/customregister.html',locals())
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Đăng kí thành công. Mã xác thực đã được gửi vào mail của bạn")
            # return render(request,'myapp/login.html',{"success":True})
            # return redirect('home')
        else:
           
            messages.error(request,'Đăng kí thất bại ')
        return render(request,'myapp/customregister.html',locals())
# ********************************************** PHÂN TRANG SẢN PHẨM (product_detail) ***************************************
class MyPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
class PaginationViewProduct(APIView):
    pagination_class = MyPagination
    def get(self, request,val):
        if val == "Dien-thoai":
            queryset = Product.objects.filter(category=2).all()
        elif val == "Laptop":
            queryset = Product.objects.filter(category=1).all()
        elif val == "Tablet":
            queryset = Product.objects.filter(category=4).all()
        elif val == "Phu-kien":
            queryset = Product.objects.filter(category=3).all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_queryset, many=True)
        # page_list = paginator.get_page_number(), # danh sách các trang 
        if request.GET.get('page'):            
            current_page = int(request.GET.get('page')) # trang hiện tại 
        else:
            current_page = 1
       
        product_count = queryset.count() #Tổng số sản phẩm
        
        total_pages = (product_count//(paginator.page_size))+1 #tổng số trang 
        page_list = [] #danh sách trang 
        for i in range(1, total_pages+1, 1):
            page_list.append(i)
        page_list_sub = [] #danh sách trang hiện ra
        first_three_dots = None
        last_three_dots = None
        # thuật toán phân trang
        if (current_page+2)<total_pages:
            last_three_dots =1
        if (current_page-2)>1:
            first_three_dots = 1
        if total_pages< 5:
            for page in page_list:
                page_list_sub.append(page)
        else:
            if current_page<4:
                for page in page_list:
                    if page<=5:
                        page_list_sub.append(page)
            else:   
                if (current_page+2)>total_pages:
                    for page in page_list:
                        if page>(total_pages-4):
                            page_list_sub.append(page)                      
                else:
                    if (current_page+2)<total_pages:
                        for page in page_list:
                            if page>=(current_page-2)and page<=(current_page+2):
                                page_list_sub.append(page)
        print(page_list_sub)

        context = {
            'product_list': serializer.data,
            'previous_page_url': paginator.get_previous_link(),
            'page_list': page_list_sub, # danh sách các trang 
            'current_page': paginator.page.number, # trang hiện tại 
            'next_page_url': paginator.get_next_link(),
            'total_pages':total_pages, #Tổng số trang
            'category':val,
            'first_three_dots':first_three_dots,
            'last_three_dots':last_three_dots,
            
        }
        
        return render(request, 'myapp/product.html', context)
#***************************************************** PROFILES ********************************************************
class ProfileView(View):
    active_profile = 1
    active_adress = None
    def get(self, request, *args, **kwargs):
        active_profile = 1
        active_adress = None
        form = MyProfileForm()
        return render(request,'myapp/profile.html',locals())
        pass
    def post(self, request, *args, **kwargs):
        active_profile = 1
        active_adress = None
        form = MyProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            adress = form.cleaned_data['adress']
            mobile = form.cleaned_data['mobile']
            check = Profile.objects.filter(user=user).first()
            if check:
                check.name = name
                check.adress = adress
                check.mobile = mobile
                check.save()
            else:
                reg = Profile(user=user,name=name,adress=adress,mobile=mobile)
                reg.save()
        return render(request,'myapp/profile.html',locals())
class Adress(View):
    def get(self, request):
        user = request.user
        active_adress = 1
        active_profile = None
        
        if user:  
            check = Profile.objects.filter(user=user).first()
            if check:
                name = check.name
                adress = check.adress
                mobile = check.mobile
                info ={'name':name,'adress':adress,'mobile':mobile}
            
        else:
            messages_info = 'Chưa nhập thông tin'
            return render(request,'myapp/adress.html',locals())
        return render(request,'myapp/adress.html',locals())
    
    
# ************************************************** XỬ LÝ ĐĂNG NHẬP ************************************************************************
# class LoginView(TokenObtainPairView):
#     def get(self, request):
#         form = CustomLoginForm
#         return render(request,'myapp/login.html',locals())
#     def post(self, request, *args, **kwargs):
#         form = CustomLoginForm(request,data = request.data)
#         if form.is_valid():
#             # Xử lý xác thực người dùng và cấp token
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             # Tạo dữ liệu để gửi cho TokenObtainPairSerializer
#             data = {
#                 'username': username,
#                 'password': password
#             }

#             # Gọi TokenObtainPairSerializer để xác thực và cấp token
#             serializer = self.get_serializer(data=data)
#             if serializer.is_valid():   
#                 token = serializer.validated_data.get('access')
#                 refresh_token = serializer.validated_data.get('r')
#                 login_active = 1
#                 print(token)
#                 return redirect('home')
#             else:
#                 return redirect('login')
            
# # ************************************************************ XỬ LÍ ĐĂNG XUẤT *****************************************************
# class LogoutView(View):
#     def get(self, request):
#         refresh_token = request.META.get('HTTP_AUTHORIZATION')
#         print(refresh_token)
#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         return redirect('home')