from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Teacher, Student
import json
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            teacher = Teacher.objects.get(username=username, password=password)
            request.session['teacher_id'] = teacher.id
            return redirect('home')
        except Teacher.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'portal/login.html')


def home(request):
    if 'teacher_id' not in request.session:
        return redirect('login')

    students = Student.objects.all()

    teacher = Teacher.objects.get(id=request.session['teacher_id'])
    return render(request, 'portal/home.html', {
        'students': students,
        'username': teacher.username
    })



@csrf_exempt
def add_or_update_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name').strip()
            subject = data.get('subject').strip()
            marks = int(data.get('marks'))

            student = Student.objects.filter(name__iexact=name, subject__iexact=subject).first()

            if student:
                student.marks = marks
                student.save()
                created = False
            else:
                Student.objects.create(name=name, subject=subject, marks=marks)
                created = True

            return JsonResponse({'success': True, 'created': created})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            Student.objects.filter(id=student_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def update_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get('id')
            name = data.get('name').strip()
            subject = data.get('subject').strip()
            marks = int(data.get('marks'))

            student = Student.objects.get(id=student_id)
            student.name = name
            student.subject = subject
            student.marks = marks
            student.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def logout_view(request):
    request.session.flush() 
    return redirect('login')
