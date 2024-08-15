from django import forms
from app_users.models import UserFavoriteFood

# เพื่อให้ผู้ใช้เลือกระดับความชอบของเมนูอาหาร
class FavoriteFoodForm(forms.ModelForm):
    class Meta:
        model = UserFavoriteFood
        fields = ["level"]
        widgets = {"level": forms.RadioSelect}
