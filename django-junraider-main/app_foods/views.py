from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app_foods.forms import FavoriteFoodForm
from app_foods.models import Food
from app_users.models import UserFavoriteFood

# Create your views here.
#ฟังก์ชันนี้ใช้ในการแสดงรายการเมนูอาหารทั้งหมด โดยดึงข้อมูลเมนูอาหารจากฐานข้อมูลและส่งไปยังเทมเพลต 
# "app_foods/foods.html" เพื่อแสดงผลลัพธ์.

def foods(request: HttpRequest):
    all_foods = Food.objects.order_by("-is_premium")
    context = {"foods": all_foods}
    return render(request, "app_foods/foods.html", context)

#ฟังก์ชันนี้ใช้ในการแสดงรายละเอียดของเมนูอาหารแบบรายการเดียว โดยดึงข้อมูลเมนูอาหารที่มี id 
 # ที่ระบุ และตรวจสอบว่าผู้ใช้เข้าสู่ระบบหรือไม่ และว่าเมนูนี้เป็นเมนูโปรดของผู้ใช้หรือไม่
def food(request: HttpRequest, food_id):
    one_food = None
    is_favorite_food = False
    try:
        one_food = Food.objects.get(id=food_id)
        if request.user.is_authenticated:
            user_favorite_food = UserFavoriteFood.objects.get(
                user=request.user, food=one_food
            )
            is_favorite_food = user_favorite_food is not None
    except:
        print("หาไม่เจอ หรือเธอไม่มี")

    form = FavoriteFoodForm()
    context = {"food": one_food, "form": form, "is_favorite_food": is_favorite_food}
    return render(request, "app_foods/food.html", context)

# ฟังก์ชันนี้ใช้ในการเพิ่มเมนูอาหารเป็นเมนูโปรดของผู้ใช้ที่เข้าสู่ระบบ โดยรับข้อมูลจากแบบฟอร์ม 
# FavoriteFoodForm และสร้างรายการ UserFavoriteFood ในฐานข้อมูล หรืออัปเดตรายการที่มีอยู่
@login_required
def favorite_food(request: HttpRequest, food_id):
    if request.method == "POST":
        form = FavoriteFoodForm(request.POST)
        if form.is_valid():
            obj, is_created = UserFavoriteFood.objects.update_or_create(
                user=request.user,
                food=Food(id=food_id),
                defaults={"level": form.cleaned_data.get("level")},
            )
            print("Create favorite" if is_created else "Update favorite")

    return HttpResponseRedirect(reverse("food", args=[food_id]))

# ฟังก์ชันนี้ใช้ในการลบเมนูอาหารออกจากรายการเมนูโปรดของผู้ใช้ที่เข้าสู่ระบบ
@login_required
def unfavorite_food(request: HttpRequest, food_id):
    if request.method == "POST":
        request.user.favorite_food_set.remove(Food(id=food_id))
    return HttpResponseRedirect(reverse("dashboard"))
