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
from .models import WorkEntry
from calendar import monthrange
from django.db.models import Q
from calendar import monthrange







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
@permission_classes([IsAuthenticated])
def monthly_dashboard(request):
    user = request.user
    today = date.today()

    # Get year and month from query params, default to current
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # Determine the first and last day of the month
    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # Fetch all entries in that month
    entries = TimeEntry.objects.filter(
        user=user,
        start_time__date__range=(start_date, end_date)
    ).order_by("start_time")

    total_minutes = 0
    days_set = set()
    running = False
    sessions = []

    for e in entries:
        days_set.add(e.start_time.date())

        if e.end_time:
            minutes = e.duration_minutes
            session_running = False
        else:
            # calculate running session duration on the fly
            minutes = int((timezone.now() - e.start_time).total_seconds() / 60)
            session_running = True
            running = True

        total_minutes += minutes
        sessions.append({
            "start": e.start_time.strftime("%H:%M:%S"),
            "end": e.end_time.strftime("%H:%M:%S") if e.end_time else None,
            "minutes": minutes,
            "running": session_running
        })

    return Response({
        "month": f"{year}-{month:02d}",
        "days_worked": len(days_set),
        "total_minutes": total_minutes,
        "total_hours": f"{total_minutes//60}h {total_minutes%60}m",
        "running": running,
        "sessions": sessions
    })

