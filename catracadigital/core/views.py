from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, resolve_url as r, redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import LoginForm, EmployeeForm
from .models import Employee, Register


def login(request):
    '''
    Handles the login page
    '''

    # Handling GET request -> displays login form
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})

    # Handling authentication
    elif request.method == 'POST':
        user_info = LoginForm(request.POST)

        # Validating form data
        if user_info.is_valid():

            # Retrieving user
            user = authenticate(
                username=user_info.cleaned_data['username'],
                password=user_info.cleaned_data['password']
            )

            # Authenticating user
            if user is not None:
                login_auth(request, user)
                return redirect(r('core:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Usuário e/ou senha inválidos.')
                return redirect(r('core:login'))


@login_required
def employee_detail(request, pk):
    '''
    Display employee view
    '''
    employee = get_object_or_404(Employee, pk=pk)

    return render(request, 'employee/detail.html', {
        'employee': employee
    })


@login_required
def employee_create(request):
    '''
    Displays and handles form for employee creation
    '''
    if request.method == 'GET':
        e = EmployeeForm(initial={'company': request.user.companies.first().pk})
        return render(request, 'employee/create.html', {'form': e})
    elif request.method == 'POST':
        employee = EmployeeForm(request.POST)
        if employee.is_valid():
            employee.save()
            messages.add_message(request, messages.INFO, 'Funcionário adicionado com sucesso!')
            return redirect(r('core:index'))


@login_required
def employee_delete(request, pk):
    '''
    Deletes an employee
    '''
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.add_message(request, messages.INFO, 'Funcionário removido com sucesso!')
    return redirect(r('core:index'))


@login_required
def register_detail(request, pk):
    '''
    Displays register details
    '''
    return render(request, 'register.html', {
        'register': get_object_or_404(Register, pk=pk)
    })

def generate_report(request, pk):
    '''
    Generates PDF for employee
    '''
    employee = get_object_or_404(Employee, pk=pk)

    # Render html content through html template with context
    html = render_to_string('employee/report.html', {'employee': employee})

    # Write PDF to file

    return HttpResponse(html)


def employee_register(request, pk):
    '''
    Register an entry for an employee
    '''
    employee = get_object_or_404(Employee, pk=pk)
    Register.objects.create(employee=employee, registered_by_manager=True)
    messages.add_message(request, messages.INFO, 'Horário marcado com sucesso!')
    return redirect(r('core:index'))

@login_required
def index(request):
    '''
    Displays main page (employees)
    '''
    return render(request, 'index.html', {
        'employees': Employee.objects.filter(company=request.user.companies.first()).prefetch_related('registers')
    })


@login_required
def logout(request):
    '''
    Handles logout action
    '''
    logout_auth(request)
    return redirect(r('core:login'))
