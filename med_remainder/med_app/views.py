from django.shortcuts import render, redirect
from .models import CustomUser, MedRemainder, User_Otp
from django.contrib import messages
from django import forms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timezone, date
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import send_otp
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
                password=password,
            )
            return redirect('/login')
        else:
            messages.error(request, "your password is too short")
            return render(request, 'med_app/signup.html')

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
            user = CustomUser.objects.filter(email=is_user).first()
            otp = send_otp(user.phone)
            otp = User_Otp.objects.create(
                user=user,
                phone_otp=otp,
                email_otp=None
            )
            return redirect('/login-otp')

    return render(request, 'med_app/login.html')


def login_with_otp(request):
    if request.method == "POST":
        phone_otp = request.POST.get('phone_otp')
        email_otp = request.POST.get('email_otp')
        user = User_Otp.objects.filter(phone_otp=phone_otp).first()
        if user is None:
            messages.info(request, "Otp incorrect !")
            return render(request, 'med_app/otp_screen.html')

        login(request, user.user)
        user.delete()
        return redirect("/remainderList")

    return render(request, 'med_app/otp_screen.html')


def logout_user(request):
    logout(request)
    return redirect('/login')


class RemainderCreate(LoginRequiredMixin, CreateView):
    model = MedRemainder
    fields = ['name', 'med_name', 'med_description',
              'time_slot_morning', 'time_slot_noon', 'time_slot_evening', 'remind_number_days']
    template_name = 'med_app/remainder_create.html'
    success_url = reverse_lazy('remaindersList')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # to change the format of the date, because by django it was set as text
        form.fields['med_description'].widget = forms.Textarea(attrs={'type': 'text'})
        form.fields['remind_number_days'].widget = forms.DateInput(attrs={'type': 'date'})

        class DateTimeLocalInput(forms.DateTimeInput):
            input_type = 'datetime-local'
            format = '%Y-%m-%dT%H:%M'

        form.fields['time_slot_morning'].widget = DateTimeLocalInput()
        form.fields['time_slot_noon'].widget = DateTimeLocalInput()
        form.fields['time_slot_evening'].widget = DateTimeLocalInput()
        return form

    def form_valid(self, form):
        # to create a form for the user who is logged in!
        form.instance.user = self.request.user
        form.instance.name = form.instance.name.capitalize()
        form.instance.med_name = form.instance.med_name.capitalize()
        # logic so that a user can't put the due date before the current date
        # due_date = form.cleaned_data['due_date']
        # c_time = datetime.now(timezone.utc)
        # if due_date < c_time:
        #     form.add_error('due_date', 'Due date must be greater than current date.')
        #     return self.form_invalid(form)
        return super(RemainderCreate, self).form_valid(form)


class RemainderListView(LoginRequiredMixin, ListView):
    model = MedRemainder
    context_object_name = 'remainders'
    template_name = 'med_app/remainder_list.html'
    paginate_orphans = 1

    def get_queryset(self):
        # to filer the tasks with respect to the user only
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(context['remainders'], 3)
        page = self.request.GET.get('page')
        remainders = p.get_page(page)
        context['remainders'] = remainders
        return context

@login_required
def searchUser(request):
    loggeduser = request.user
    if request.method == 'POST':
        search_query = request.POST.get('search')
        if not search_query:
            return redirect('/remainderList')
        else:
            med = MedRemainder.objects.filter(user=loggeduser)
            data = med.filter(name__contains=search_query.capitalize())
            if len(data) == 0:
                med_data = med.filter(med_name__contains=search_query.capitalize())
                params = {'datas': med_data}
                return render(request, 'med_app/search.html', params)
            params = {'datas': data}
            return render(request, 'med_app/search.html', params)
    else:
        return render(request, 'med_app/search.html')


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
