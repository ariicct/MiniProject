from datetime import datetime, timedelta

from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app_general.forms import SubscriptionModelForm

# Create your views here.


def home(request: HttpRequest):
    return render(request, "app_general/home.html")


def about(request: HttpRequest):
    return render(request, "app_general/about.html")

#ฟังก์ชันนี้ใช้ในการรับข้อมูลการสมัครสมาชิกจากผู้ใช้ หากมีคำขอ POST โดยใช้แบบฟอร์ม SubscriptionModelForm
# และหากแบบฟอร์มถูกต้อง (valid) 
# จะบันทึกข้อมูลลงในฐานข้อมูลและส่งผู้ใช้ไปยังหน้าขอบคุณ "subscription_thankyou".
def subscription(request: HttpRequest):
    # POST
    if request.method == "POST":
        form = SubscriptionModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("subscription_thankyou"))
    else:
        form = SubscriptionModelForm()

    # GET
    context = {"form": form}
    return render(request, "app_general/subscription_form.html", context)

#subscription_thankyou(request: HttpRequest): ฟังก์ชันนี้ใช้ในการแสดงหน้าขอบคุณหลัง
# จากผู้ใช้ทำการสมัครสมาชิกเรียบร้อย 
# โดยใช้เทมเพลต "app_general/subscription_thankyou.html" เพื่อแสดงผลลัพธ์.
def subscription_thankyou(request: HttpRequest):
    return render(request, "app_general/subscription_thankyou.html")

#change_theme(request: HttpRequest): ฟังก์ชันนี้ใช้ในการเปลี่ยนธีม (theme) ของเว็บไซต์ โดยตรวจสอบค่า theme 
# ที่ผู้ใช้ส่งผ่านพารามิเตอร์ theme ใน URL และตั้งค่าธีมของเว็บไซต์ด้วยการกำหนดคุกกี้ (cookie) โดยใช้ response.set_cookie
# หรือลบคุกกี้ธีมโดยใช้ response.delete_cookie. 
# หลังจากนั้น ฟังก์ชันนี้จะกลับไปยังหน้าเดิมที่ผู้ใช้เคยอยู่ หากไม่มีหน้าก่อนหน้านี้จะกลับไปยังหน้าหลัก (home).

def change_theme(request: HttpRequest):
    referer = request.headers.get("referer")
    if referer is not None:
        response = HttpResponseRedirect(referer)
    else:
        response = HttpResponseRedirect(reverse("home"))

    # Theme
    theme = request.GET.get("theme")
    if theme == "dark":
        expired_date = datetime.now() + timedelta(days=365)
        response.set_cookie("theme", "dark", expires=expired_date, samesite="Lax")
    else:
        response.delete_cookie("theme")

    return response
