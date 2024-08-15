from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_users.models import CustomUser, Profile

#นี่เป็นแบบฟอร์มสำหรับการลงทะเบียนผู้ใช้ใหม่ โดยสืบทอด (extends) มาจาก UserCreationForm ซึ่งเป็นแบบฟอร์มเดิมของ 
# Django สำหรับการสร้างผู้ใช้. สิ่งที่ทำเพิ่มเติมคือการเพิ่มฟิลด์ email เข้าไปในแบบฟอร์มผ่าน Meta class.

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email",)

#แบบฟอร์มนี้ใช้ในการแก้ไขข้อมูลพื้นฐานของผู้ใช้ เช่น ชื่อและนามสกุล โดยใช้ข้อมูลจาก
# CustomUser และปรับแก้แค่ฟิลด์ first_name และ last_name.

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")

#แบบฟอร์มนี้ใช้ในการแก้ไขข้อมูลขยายของโปรไฟล์ผู้ใช้ เช่น ที่อยู่และหมายเลขโทรศัพท์ โดยใช้ข้อมูลจากโมเดล Profile. 
# แบบฟอร์มนี้ถูกกำหนดให้ใช้โพรพเพอร์ตีชื่อ extended และมีฟิลด์ address 
# และ phone รวมถึงปรับแต่งข้อความภายในแบบฟอร์มและใช้ Textarea สำหรับฟิลด์ address.
class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"

    class Meta:
        model = Profile
        fields = ("address", "phone")
        labels = {
            "address": "ที่อยู่",
            "phone": "เบอร์โทรศัพท์",
        }
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}
