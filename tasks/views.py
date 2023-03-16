from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, Company
from django.utils import timezone
from django.contrib.auth.decorators import login_required # proteger urls 

# Create your views here.


def home(request):
    company = Company.objects.all() # todas las tareas
    return render(request, 'home.html', {'company': company})



def signup(request):
    contexto = {'form': UserCreationForm,
                'error': 'User created succesfully'
                }
    if request.method == "GET":
        return render(request, 'signup.html', contexto)

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario
                # obtengo usuario y password del usurio, asigno en vble user
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                # Grabo el usurio en la base de datos
                user.save()
                login(request, user) # crea seccion d usuario y/o Cookies.
                return redirect('tasks')
            except IntegrityError:
                contexto = {'form': UserCreationForm,
                'error': 'Username already exists',
                }
                return render(request, 'signup.html', contexto)
                
        contexto = {'form': UserCreationForm,
                'error': 'Password do not match',
                }
        return render(request, 'signup.html', contexto)

@login_required
def tasks(request):
    # tasks = Task.objects.all() # todas las tareas
    # tareas del usuario activo y sin terminadas 
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # filtra tarea x usuario logueado

    return render(request, 'tasks.html', {'tasks': tasks, 'title':'Tasks Pending'})

@login_required
def tasks_completed(request):
    # tasks = Task.objects.all() # todas las tareas
    # tareas del usuario activo y sin terminadas 
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted') # filtra tarea x usuario logueado

    return render(request, 'tasks.html', {'tasks': tasks,'title':'Tasks Completed'})


@login_required
def create_task(request):
    if request.method =='GET':
        return render(request, 'create_task.html', {
                    'form': TaskForm
                })
    else:
        try:

            # print(request.POST) # OBTENGO LOS DATOS QUE DIGITARON 
            # EN FORM TASK print(request.POST)
            form = TaskForm(request.POST)
            
            new_task = form.save(commit=False) # commit, grabe solo los datos
            new_task.user = request.user # asigna el usuario de la seccion, viene en el request
            new_task.save()
            #print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                    'form': TaskForm,
                    'error': "Please provide valid data"
                })

@login_required
def task_detail(request, task_id):
    if request.method=='GET':
        # odtenga (get) la tarea donde Task (modelo a consultar) 
        # pk (primaryKey) sea igual a task_id
        # # si la busqueda no existe, no se cae el programa. pag Error 404
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task) # rellena un form con los datos de instancia de x tarea
        return render(request, 'task_detail.html', {'task': task,
                                                 'form': form })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task) # rellena un form con los datos de instancia de x tarea
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', 
                                        {'task': task,
                                         'form': form,
                                         'error': 'Error Updateng task'})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now() # actualiza fecha
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request): # ausrio existente
    if request.method == "GET":
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        # valido datos del usuario, username y password
        print(request.POST)
        # authenticate, devuelve un usuario si existe
        # delo contario de vuelve un dato vacio
        user = authenticate(request, username=request.POST['username'],
                     password=request.POST['password']
                    )
        if user is None: # si el usurio no existe 
            contexto = {'form': AuthenticationForm,
                        'error': 'Username or Password is Incorrect'
                        } 
            return render(request, 'signin.html', contexto )
        else: # SI EXISTE 
            login(request, user) # crea seccion d usuario y/o Cookies.
            return redirect('tasks')
                
