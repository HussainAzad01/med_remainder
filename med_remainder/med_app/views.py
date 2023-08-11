from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import CustomUser, MedRemainder
from django.contrib import messages
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from datetime import datetime,timezone, date
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        user = CustomUser.objects.filter(email=email)
        # try:
        if user.exists():
            messages.info(request, "User already Exists, Please login!")
            return redirect('/login')

        if password == password_repeat and len(password) >= 8:
            user = CustomUser.objects.create_user(
                email=email,
                phone=phone,
                password=password
            )
            messages.success(request, "User Signup successfully, please login!")
            return redirect('/login')

        # except:
        #     messages.error(request, 'Please enter valid email')

    return render(request, 'med_app/signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_user = authenticate(request, email=email, password=password)
        user = CustomUser.objects.filter(email=email)

        if not user.exists():
            messages.info(request, "User does not exist, Please Signup First!")
            return redirect('/signup')

        elif is_user is None:
            messages.info(request, 'Password is incorrect!')

        elif is_user is not None:
            login(request, is_user)
            return redirect('/remainderList')

    return render(request, 'med_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('/login')


# @login_required
# def remainderCreate(request):
#     if request.method == 'POST':
#         data = request.POST
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         med_name = data.get('med_name')
#         med_description = data.get('med_description')
#         reminder_morning = str_to_datetime(data.get('morning'))
#         reminder_noon = str_to_datetime(data.get('noon'))
#         reminder_evening = str_to_datetime(data.get('evening'))
#         reminder_upto = str_to_date(data.get('remind_date'))
#         # c_time = date.today()
#         c_time = datetime.now(tz=timezone.utc)
#         if reminder_upto >= c_time:
#             med = MedRemainder.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 med_name=med_name,
#                 med_description=med_description,
#                 time_slot_morning=reminder_morning,
#                 time_slot_noon=reminder_noon,
#                 time_slot_evening=reminder_evening,
#                 remind_number_days=reminder_upto
#             )
#
#
#         else:
#             messages.error(request, f"Date should be greater than {c_time}")
#     return render(request, 'med_app/remainder_create.html')

class RemainderCreate(CreateView):
    model = MedRemainder
    fields = ['first_name', 'last_name', 'med_name', 'med_description', 'time_slot_morning', 'time_slot_noon', 'time_slot_evening', 'remind_number_days']
    template_name = 'med_app/remainder_create.html'
    success_url = reverse_lazy('remainderList')

    def form_valid(self, form):
        # to add current time in the created_on field
        form.instance.user = self.request.user
        # logic so that a user can't put the due date before the current date
        # due_date = form.cleaned_data['due_date']
        # c_time = datetime.now(timezone.utc)
        # if due_date < c_time:
        #     form.add_error('due_date', 'Due date must be greater than current date.')
        #     return self.form_invalid(form)
        return super(RemainderCreate, self).form_valid(form)


def remainderList(request):
    email = request.user
    print(email)
    data = MedRemainder.objects.filter(user=email)
    params = {'reminders': data}
    return render(request, 'med_app/remainder_list.html', params)


def str_to_date(reminder_date):
    if reminder_date == '':
        return None
    date_string = reminder_date
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_string, date_format).date()
    return date_object


def str_to_datetime(reminder_datetime):
    if reminder_datetime == '':
        return None
    date_string = reminder_datetime
    date_format = '%Y-%m-%dT%H:%M'
    date_object = datetime.strptime(date_string, date_format)
    return date_object
