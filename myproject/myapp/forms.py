from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile 
# from .models import Profile
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':"True",'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Nhập lại mật khẩu',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tên đăng nhập' 
        self.fields['password1'].label ='Mật khẩu'
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    
class MypasswordResetForm(PasswordResetForm):
    pass
class MyProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id','user','name','adress','mobile']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'adress':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
        }