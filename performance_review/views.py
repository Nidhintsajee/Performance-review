from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import datetime

from .forms import *
from .models import *


@login_required
def dashboard(request):
    total_employees = Employee.objects.all().count()
    total_reviews = Review.objects.all().count()

    # -----------------------------------------------------------------------------------------------------------------
    if request.user.is_superuser:
        context = {
            'report': "today_r",
            'total_employees': total_employees,
            'total_reviews': total_reviews,
            # 'today_min_user': minimum_user,
            # 'today_max': maximum,
            # 'today_max_user': maximum_user,

            # 'total_tasks': total_tasks,
            # 'completed_tasks': completed_tasks,
            # 'running_tasks': running_tasks,
            # 'cancelled_tasks': cancelled_tasks,
        }
        return render(request=request, template_name='application/dashboard.html', context=context)
    else:
        return render(request=request, template_name='application/employee_dashboard.html')


def help_view(request):
    return render(request=request, template_name='application/help.html')


# ---------------------------------------------------------------------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def employees(request):
    context = {
        'employees': Employee.objects.exclude(user__is_superuser=True)
    }
    return render(request=request, template_name='application/employees.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def employee(request, pk):
    try:
        emp = Employee.objects.get(pk=pk)
        context = {
            'employee': emp
        }
        return render(request=request, template_name='application/employee.html')
    except Employee.DoesNotExist:
        messages.error(request=request,
                       message=f"Requested Employee ID: {pk} doesn't exists, please check the employees below.")
        return redirect('application:employees')


@user_passes_test(lambda u: u.is_superuser)
def report(request):
    return render(request=request, template_name='application/report.html')


@user_passes_test(lambda u: u.is_superuser)
def add_employee(request):
    form = None

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            Employee.objects.create(user=user)
            messages.success(request=request, message=f'New Employee added successfully')
            return redirect('application:update_employee', Employee.objects.get(user=user).pk)
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request=request, template_name='application/add_employee.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def update_employee(request, pk):
    emp = Employee.objects.get(pk=pk)
    u = emp.user

    user_form = UserForm(instance=u)
    emp_form = EmployeeForm(instance=emp)

    if request.method == 'POST':
        order = request.GET['action']
        if order == 'other':

            emp_form = EmployeeForm(request.POST, request.FILES or None, instance=emp)
            if emp_form.is_valid():
                emp_form.save(commit=True)
                messages.success(request, f'{u.first_name} details updated successfully')

        elif order == 'account':

            user_form = UserForm(request.POST, instance=u)
            if user_form.is_valid():
                user_form.save(commit=True)
                messages.success(request, f'{u.first_name} details updated successfully')

    context = {
        'user_form': user_form,
        'emp_form': emp_form,
        'pk': pk,
    }
    return render(request=request, template_name='application/update_employee.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, pk):
    try:
        user = Employee.objects.get(pk=pk).user

        if user.is_superuser:
            messages.error(
                request=request,
                message=f"{user} is super user _ you are not allowed to delete"
            )
        else:
            messages.success(request=request, message=f'{user.first_name} {user.last_name} deleted successfully')
            user.delete()
    except User.DoesNotExist:
        messages.error(
            request=request,
            message=f"Requested Employee ID: {pk} doesn't exists, please check the employees below."
        )
    return redirect('application:employees')


# ---------------------------------------------------------------------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def reviews(request):
    context = {
        'tasks': Review.objects.all()
    }
    return render(request=request, template_name='application/tasks.html', context=context)


@login_required
def review(request, pk):
    try:
        tsk = Review.objects.get(pk=pk)
        context = {
            'task': tsk
        }
        return render(request=request, template_name='application/task.html', context=context)
    except Review.DoesNotExist:
        messages.error(request=request,
                       message=f"Requested task ID: {pk} doesn't exists, please check the tasks below.")
        return redirect('application:reviews')


# @user_passes_test(lambda u: u.is_superuser)
def add_review(request):
    form = None

    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request=request, message=f'New task added successfully')
            return redirect('application:reviews', permanent=True)
    else:
        form = ReviewForm()

    context = {
        'form': form
    }
    return render(request=request, template_name='application/../../templates/application/add_task.html',
                  context=context)


@user_passes_test(lambda u: u.is_superuser)
def update_review(request, pk):
    emp = None
    form = None

    try:
        emp = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        messages.error(
            request=request,
            message=f"Requested task ID: {pk} doesn't exists, please check the tasks below."
        )
        return redirect('application:reviews')

    if request.method == 'POST':
        form = ReviewForm(instance=emp, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request=request, message=f'{emp.employee} details updated successfully')
            return redirect('application:update_review', emp.pk, permanent=True)
    else:
        form = ReviewForm(instance=emp)

    context = {'form': form}
    return render(request=request, template_name='application/add_task.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_review(request, pk):
    try:
        task = Review.objects.get(pk=pk)
        messages.success(request=request, message=f'{task.employee} deleted successfully')
        task.delete()
    except Review.DoesNotExist:
        messages.error(
            request=request,
            message=f"Requested task ID: {pk} doesn't exists, please check the tasks below."
        )
    return redirect('application:reviews')


# @user_passes_test(lambda u: u.is_superuser)
def emp_reviews(request):
    user = request.user
    context = {
        'tasks': Review.objects.filter(employee__user_id=user.id)
    }
    return render(request=request, template_name='application/tasks.html', context=context)


# ---------------------------------------------------------------------------------------------------------------------
def view_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
    else:
        form = AuthenticationForm
    return render(request=request, template_name='accounts/login.html', context={'form': form})


@login_required
def view_logout(request):
    logout(request)
    return redirect('/accounts/login/')
