from django import forms

from app_foods.models import Food
from app_general.models import Subscription

# Custom field class
#นี่เป็นคลาสที่ถูกสร้างขึ้นสืบทอดมาจาก forms.ModelMultipleChoiceField
# เพื่อแสดงตัวเลือกรายการเมนูอาหารที่สนใจ โดยใช้ฟิลด์แบบ ModelMultipleChoiceField จากฟิลด์ food_set 
# และจัดรูปแบบข้อความที่แสดงบนตัวเลือกด้วยเมธอด label_from_instance.

class FoodMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.title


# Form class 
# นี่คือคลาสแบบฟอร์มที่ใช้ในการรับข้อมูลการสมัครโปรโมชั่น มีฟิลด์ที่ระบุชื่อ-นามสกุล, อีเมล, เมนูที่สนใจ (เมนูที่เลือก), และข้อความยอมรับ.
class SubscriptionForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="ชื่อ-นามสกุล")
    email = forms.EmailField(max_length=50, required=True, label="อีเมล")
    food_set = FoodMultipleChoiceField(
        queryset=Food.objects.order_by("-is_premium"),
        required=True,
        label="เมนูที่สนใจ",
        widget=forms.CheckboxSelectMultiple,
    )
    accepted = forms.BooleanField(
        required=True,
        label="ข้อความยาวๆที่หลายคนเคยเจอ อาจไม่ต้องอ่านก็ได้ แค่ยอมรับและเข้าใจก็พอ",
    )


# Model form class  นี่คือคลาสแบบแบบแบบฟอร์ม (Model Form) ที่ใช้ในการรับข้อมูลการสมัครสมาชิก
# เช่นเดียวกับ SubscriptionForm แต่มีคุณสมบัติเพิ่มเติมที่ใช้ในการกำหนดแบบแบบของโมเดล Subscription.
# นอกจากนี้ยังมีการกำหนดฟิลด์ที่ต้องการและฟิลด์ที่สามารถเข้าถึงผ่านแบบฟอร์มด้วยตัวกำหนด fields 
# และการกำหนดป้ายชื่อของฟิลด์ที่จะแสดงบนแบบฟอร์มด้วยตัวกำหนด labels.
class SubscriptionModelForm(forms.ModelForm):
    food_set = FoodMultipleChoiceField(
        queryset=Food.objects.order_by("-is_premium"),
        required=True,
        label="เมนูที่สนใจ",
        widget=forms.CheckboxSelectMultiple,
    )
    accepted = forms.BooleanField(
        required=True,
        label="ข้อความยาวๆที่หลายคนเคยเจอ อาจไม่ต้องอ่านก็ได้ แค่ยอมรับและเข้าใจก็พอ",
    )
#ฟิลด์ของแบบฟอร์มรวมถึง name, email, food_set, และ accepted ในทั้ง SubscriptionForm และ SubscriptionModelForm ระบุประเภทของข้อมูลที่จะรับและส่งไปยังฐานข้อมูล
# เช่น ชื่อ-นามสกุล, อีเมล, รายการเมนูที่สนใจ, และข้อความยอมรับ.
#food_set และ accepted มีการกำหนดเป็นฟิลด์แบบ CheckBox ซึ่งผู้ใช้สามารถเลือกหรือไม่เลือก ด้วยการใช้ widget=forms.CheckboxSelectMultiple.
    class Meta:
        model = Subscription
        fields = ["name", "email", "food_set", "accepted"]
        labels = {
            "name": "ชื่อ-นามสกุล",
            "email": "อีเมล",
            "food_set": "เลือกเมนูที่สนใจ",
        }
