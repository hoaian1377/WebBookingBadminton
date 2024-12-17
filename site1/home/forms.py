from django import forms 
from .models import RegisterUser

class RegisterForm(forms.ModelForm):
    Comfirm_password = forms.CharField(widget=forms.PasswordInput(), label="Nhập lại mật khẩu")
    class Meta:
        model = RegisterUser
        fields = ['Email','Username','Password']
        widgets={
            'Password':forms.PasswordInput(),
        }
    
    def clean(self):
        cleaned_data=super().clean()
        Password=cleaned_data.get('Password')
        Comfirm_password=cleaned_data.get('Comfirm_password')
        
        if Password != Comfirm_password:
            raise forms.ValidationError("Mật Khẩu Không Khớp . Vui Lòng Nhập Lại!")
        return cleaned_data 