from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from app_users.forms import ExtendedProfileForm, RegisterForm, UserProfileForm
from app_users.models import CustomUser
from app_users.utils.activation_token_generator import activation_token_generator


# Create your views here.
# ฟังก์ชันนี้ใช้ในการจัดการการลงทะเบียนผู้ใช้ใหม่. หากมีคำขอ POST, จะตรวจสอบแบบฟอร์ม RegisterForm และหากแบบฟอร์มถูกต้อง (valid),
# จะสร้างบัญชีผู้ใช้ใหม่และส่งอีเมลยืนยันการลงทะเบียนไปยังผู้ใช้ โดยใช้การสร้าง token และ URL สำหรับการยืนยันการลงทะเบียน

def register(request: HttpRequest):
    # POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Register and wait for activation
            user: CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()

            # Build email body
            context = {
                "protocol": request.scheme,
                "host": request.get_host(),
                "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
                "token": activation_token_generator.make_token(user),
            }
            email_body = render_to_string(
                "app_users/activate_email.html", context=context
            )

            # Send email
            email = EmailMessage(
                to=[user.email],
                subject="Activate account หน่อยครับ",
                body=email_body,
            )
            email.send()

            # Change redirect to register thank you
            return HttpResponseRedirect(reverse("register_thankyou"))
    else:
        form = RegisterForm()

    # GET
    context = {"form": form}
    return render(request, "app_users/register.html", context)

# ฟังก์ชันนี้ใช้ในการแสดงหน้าขอบคุณหลังจากผู้ใช้ทำการลงทะเบียนเรียบร้อย
def register_thankyou(request: HttpRequest):
    return render(request, "app_users/register_thankyou.html")

# ฟังก์ชันนี้ใช้ในการเปิดใช้งานบัญชีผู้ใช้โดยตรวจสอบ token และ uidb64 ที่ถูกสร้างขึ้นในการลงทะเบียน.
# ถ้า token ถูกต้องและไม่หมดอายุ บัญชีผู้ใช้จะถูกเปิดใช้งาน
def activate(request: HttpRequest, uidb64: str, token: str):
    title = "Activate account เรียบร้อย"
    content = "คุณสามารถเข้าสู่ระบบได้เลย"
    id = urlsafe_base64_decode(uidb64).decode()
    try:
        user = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user, token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("Activate ไม่ผ่าน")
        title = "Activate account ไม่ผ่าน"
        content = "เป็นไปได้ว่าลิ้งค์ไม่ถูกต้อง หรือหมดอายุไปแล้ว"

    context = {"title": title, "content": content}
    return render(request, "app_users/activate.html", context)

# ฟังก์ชันนี้ใช้ในการแสดงหน้าแดชบอร์ด (dashboard) ของผู้ใช้ที่ลงทะเบียนและเข้าสู่ระบบ โดยแสดงรายการเมนูโปรดของผู้ใช้
@login_required
def dashboard(request: HttpRequest):
    favorite_food_pivots = request.user.favorite_food_pivot_set.order_by("-level")
    context = {"favorite_food_pivots": favorite_food_pivots}
    return render(request, "app_users/dashboard.html", context)

# ฟังก์ชันนี้ใช้ในการจัดการโปรไฟล์ของผู้ใช้. หากมีคำขอ POST, ฟังก์ชันนี้จะอัปเดตหรือสร้างโปรไฟล์ของผู้ใช้โดยใช้แบบฟอร์ม 
# UserProfileForm และ ExtendedProfileForm. ถ้าคำขอสำเร็จ, 
# ฟังก์ชันจะสร้างหรืออัปเดตโปรไฟล์และส่งกลับไปยังหน้าโปรไฟล์ และตั้งค่าคุกกี้เพื่อแสดงข้อความบันทึกสำเร็จ.
@login_required
def profile(request: HttpRequest):
    user = request.user

    # POST
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False
        try:
            # Will be updated profile
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            # Will be created profile
            is_new_profile = True
            extended_form = ExtendedProfileForm(request.POST)

        if form.is_valid() and extended_form.is_valid():
            form.save()
            if is_new_profile:
                # Create profile
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                # Update profile
                extended_form.save()
            response = HttpResponseRedirect(reverse("profile"))
            response.set_cookie("is_saved", "1")
            return response
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()

    # GET
    is_saved = request.COOKIES.get("is_saved") == "1"
    flash_message = "บันทึกเรียบร้อย" if is_saved else None
    context = {
        "form": form,
        "extended_form": extended_form,
        "flash_message": flash_message,
    }
    response = render(request, "app_users/profile.html", context)
    if is_saved:
        response.delete_cookie("is_saved")
    return response
