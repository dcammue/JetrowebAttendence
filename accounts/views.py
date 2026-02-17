from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import TimeEntry
from django.utils import timezone
from datetime import date
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from calendar import monthrange
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from .permissions import IsUser
from django.contrib.auth import get_user_model
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from django.db.models import Sum
from datetime import date
from calendar import monthrange
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth import get_user_model
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from .models import PasswordReset
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render



from .models import WorkEntry

class PDFRenderer(BaseRenderer):
    media_type = "application/pdf"
    format = "pdf"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data



User = get_user_model()




# Login API
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_admin': user.is_staff
        })

# Logout API
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"})

# StartStop
class StartStopView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        user = request.user

        if action == "start":
            # Check if a session is already running
            if TimeEntry.objects.filter(user=user, end_time__isnull=True).exists():
                return Response({"error": "Session already running"}, status=400)

            entry = TimeEntry.objects.create(user=user, start_time=timezone.now())
            return Response({
                "message": "Work started",
                "entry_id": entry.id,
                "start_time": entry.start_time
            })

        elif action == "stop":
            # Get the last uncompleted TimeEntry
            try:
                entry = TimeEntry.objects.filter(user=user, end_time__isnull=True).latest('start_time')
            except TimeEntry.DoesNotExist:
                return Response({"error": "No active work session"}, status=400)

            entry.end_time = timezone.now()
            entry.save()
            return Response({
                "message": "Work stopped",
                "entry_id": entry.id,
                "start_time": entry.start_time,
                "end_time": entry.end_time,
                "duration_minutes": entry.duration_minutes
            })

        else:
            return Response({"error": "Invalid action"}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_dashboard(request):
    today = date.today()
    entries = TimeEntry.objects.filter(
        user=request.user,
        start_time__date=today
    )

    total = 0
    sessions = []
    running = False

    for e in entries:
        if e.end_time:
            minutes = e.duration_minutes
            is_running = False
        else:
            # LIVE running time
            minutes = int((timezone.now() - e.start_time).total_seconds() // 60)
            running = True
            is_running = True

        total += minutes

        sessions.append({
            "start": e.start_time.strftime("%H:%M:%S"),
            "end": e.end_time.strftime("%H:%M:%S") if e.end_time else None,
            "minutes": minutes,
            "running": is_running
        })

    return Response({
        "username": request.user.username,
        "date": str(today),
        "total_minutes": total,
        "total_hours": f"{total//60}h {total%60}m",
        "running": running,
        "sessions": sessions
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary(request):
    user = request.user
    today = date.today()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    entries = TimeEntry.objects.filter(
        user=user,
        start_time__date__range=(start_date, end_date)
    )

    total_minutes = 0
    worked_days = set()

    for e in entries:
        worked_days.add(e.start_time.date())

        if e.end_time:
            minutes = e.duration_minutes
        else:
            minutes = int((timezone.now() - e.start_time).total_seconds() // 60)

        total_minutes += minutes

    return Response({
        "month": f"{year}-{month:02d}",
        "days_worked": len(worked_days),
        "total_minutes": total_minutes,
        "total_hours": f"{total_minutes//60}h {total_minutes%60}m"
    })




@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    today = date.today()

    users = User.objects.all()

    active_sessions = TimeEntry.objects.filter(end_time__isnull=True)

    active_users = []
    for e in active_sessions:
        active_users.append({
            "username": e.user.username,
            "started_at": e.start_time,
            "running_minutes": int((timezone.now() - e.start_time).total_seconds() / 60)
        })

    user_summaries = []

    for user in users:
        entries = TimeEntry.objects.filter(
            user=user,
            start_time__date=today
        )

        total_minutes = 0
        running = False

        for e in entries:
            if e.end_time:
                total_minutes += e.duration_minutes
            else:
                running = True
                total_minutes += int((timezone.now() - e.start_time).total_seconds() / 60)

        user_summaries.append({
            "username": user.username,
            "today_minutes": total_minutes,
            "today_hours": f"{total_minutes//60}h {total_minutes%60}m",
            "is_running": running
        })

    return Response({
        "date": str(today),
        "active_sessions": active_users,
        "users": user_summaries
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsUser])
def user_dashboard(request):
    return Response({
        "message": "Welcome user",
        "username": request.user.username
    })



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({
        "username": request.user.username,
        "is_staff": request.user.is_staff
    })




@staff_member_required
def monthly_payroll_pdf(request):
    month_param = request.GET.get("month")  # e.g. 2026-02

    if not month_param:
        return HttpResponse("Month is required. Example: ?month=2026-02", status=400)

    year, month = map(int, month_param.split("-"))
    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # Group by user and sum minutes
    totals = (
        TimeEntry.objects
        .filter(start_time__date__range=(start_date, end_date), end_time__isnull=False)
        .values("user__username")
        .annotate(total_minutes=Sum("duration_minutes"))
        .order_by("user__username")
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="payroll_{month_param}.pdf"'

    pdf = canvas.Canvas(response)
    y = 750

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, f"Jetro Web Development — Attendance for {month_param}")
    y -= 40

    pdf.setFont("Helvetica", 12)

    if not totals:
        pdf.drawString(50, y, "No work records found for this month.")
    else:
        for row in totals:
            username = row["user__username"]
            minutes = row["total_minutes"] or 0

            hours = minutes // 60
            mins = minutes % 60

            pdf.drawString(50, y, f"{username}    {hours}h {mins}m")
            y -= 25

            if y < 50:
                pdf.showPage()
                y = 750

    pdf.save()
    return response


# registration form
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    email = request.data.get("email")

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)




#delete account
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user

    # Delete everything owned by this user
    user.timeentry_set.all().delete()   # or TimeEntry.objects.filter(user=user).delete()
    user.delete()

    return Response({"message": "Account deleted successfully"})



# Forgot password
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get("username")   # coming from JS

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "No account with this email"}, status=404)

    reset = PasswordReset.objects.create(user=user)

    reset_link = f"http://127.0.0.1:8000/api/accounts/reset/?token={reset.token}"

    send_mail(
        "Reset your password",
        f"Click to reset your password:\n{reset_link}",
        "noreply@jetroweb.com",
        [user.email],
        fail_silently=False,
    )

    return Response({"message": "Reset link sent"})



# Reset password
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    token = request.data.get("token")
    password = request.data.get("password")

    if not token or not password:
        return Response({"error": "Missing token or password"}, status=400)

    try:
        reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        return Response({"error": "Invalid or expired token"}, status=400)

    user = reset.user   # 🔐 THIS is the real owner

    user.set_password(password)
    user.save()

    reset.delete()

    return Response({"message": "Password reset successful"})




# Login page 
def login_page(request):
    return render(request, "accounts/index.html")

# Forgot password page 
def forgot_page(request):
    return render(request, "accounts/forgot.html")

# Reset password page
def reset_page(request):
    return render(request, "accounts/reset.html")


# At the bottom of accounts/views.py
@staff_member_required
def test_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="test.pdf"'

    pdf = canvas.Canvas(response)
    pdf.drawString(100, 750, "Hello PDF!")
    pdf.save()

    return response


def home(request):
    return render(request, "accounts/index.html")

def admindashboard(request):
    return render(request, "accounts/admin.html")

def dashboard(request):
    return render(request, "accounts/user.html")


# views.py
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'is_staff': user.is_staff,       # ✅ important
            'role': 'admin' if user.is_staff else 'user'  # optional
        })
