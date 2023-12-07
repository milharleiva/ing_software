from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Cliente, Administrador,Producto,Carrito, Boleta, ItemCarrito
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound
from django.views.generic import(View,TemplateView,ListView,DeleteView)
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
import uuid
from .forms import ProductoForm 
from django.http import HttpResponseForbidden
import logging


def index(request):
    return render(request, 'logins/index.html')



def register(request):
    if request.method == 'POST':
        
        rut = request.POST.get('usuario')
        nombre = request.POST.get('nombre')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')

        
        if password == re_password:
          
           

          
            user = User.objects.create(
                username=rut,
                first_name=nombre,
                last_name=last_name,
                email=email,
                password=make_password(password) 
            )

          
            cliente = Cliente.objects.create(
                usuario=user,
                nombre=nombre
            )

           
            login(request, user)
            return redirect('/login')
        else:
            
            return redirect('/')

   
    return render(request, 'logins/register.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'logins/login.html', {'error_message': 'Credenciales incorrectas'})
    return render(request, 'logins/login.html')



def cerrar_sesion(request):
    logout(request)
    return redirect('/')




@login_required
def dashboard(request):
    users = User.objects.all()
    data = {'users':users}
    return render(request, 'logins/dashboard.html', data)

def change(request, username=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        return redirect('/')
    else:
        data = {'username':username}
        return render(request, 'logins/change.html', data)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def crear_usuario(request):

    if not request.user.is_superuser:
      
        return HttpResponseNotFound("No tienes permisos para ver esta página.")



    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        is_admin = request.POST.get('is_admin') == 'on'

       
        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=nombre,
            is_superuser=is_admin,
            is_staff=is_admin  
        )

        
        if is_admin:
            Administrador.objects.create(usuario=user, nombre=nombre)

       
        return redirect('/')
    else:
        
        return render(request, 'web/crear_usuario.html')





@login_required
def carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = ItemCarrito.objects.get(id=item_id, carrito=carrito)

        if action == 'remove_one':
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else:
                item.delete()
        elif action == 'remove_all':
            item.delete()

        return redirect('carrito')  

    total = sum(item.get_cost() for item in items)
    return render(request, 'web/carrito.html', {'items': items, 'total': total})



def confirmacion_pago(request):
    return render(request, 'web/confirmacion_pago.html')



@login_required
def procesar_pago(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario).first()

    if not carrito:
        
        return redirect('listar_productos')

    items = ItemCarrito.objects.filter(carrito=carrito)

    if not items:
        
        return redirect('listar_productos')

    total = sum(item.get_cost() for item in items)  # Asegúrate de que la función get_cost() devuelve un valor decimal

    
    boleta = Boleta.objects.create(usuario=usuario, total=total)

    
    for item in items:
        boleta.itemboleta_set.create(producto=item.producto, cantidad=item.cantidad, precio=item.producto.precio)

    
    items.delete()

    
    return render(request, 'web/detalle_boleta.html', {'boleta': boleta})

logger = logging.getLogger(__name__)
@login_required
def actualizar_carrito(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        logger.debug(f"Actualizando carrito con item_id: {item_id}, acción: {action}")
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

        if action == 'remove_one':

            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
                messages.info(request, 'Se ha reducido la cantidad de un producto.')
            else:
                item.delete()
                messages.info(request, 'El producto ha sido eliminado del carrito.')
        elif action == 'remove_all':
            
            item.delete()
            messages.info(request, 'Todos los productos han sido eliminados del carrito.')
        elif action == 'update':
            
            nueva_cantidad = request.POST.get('cantidad', 1)
            try:
                nueva_cantidad = int(nueva_cantidad)
                if nueva_cantidad > 0:
                    item.cantidad = nueva_cantidad
                    item.save()
                    messages.info(request, 'La cantidad del producto ha sido actualizada.')
                else:
                    messages.error(request, 'La cantidad debe ser mayor que cero.')
            except ValueError:
                messages.error(request, 'Cantidad inválida.')
    else:
        messages.error(request, 'Acción inválida.')
        
    return redirect('carrito')

@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)

       
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

       
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

        if not created:
           
            item.cantidad += 1
            item.save()

        
        return redirect('listar_productos')

    
    return redirect('listar_productos')





@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')  
def crear_productos(request):
    if not request.user.is_superuser:
        
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == 'POST':
       
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')

        
        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            disponible=True  
        )

       
        return redirect('listar_productos')

    
    return render(request, 'web/crear_productos.html')




def error_404(request, exception):
    return render(request, 'web/error404.html', status=404)


def listar_productos(request):

    productos = Producto.objects.all()
 
    return render(request, 'web/listar_productos.html', {'productos': productos})


@login_required
def detalle_boleta(request, boleta_id):
    boleta = get_object_or_404(Boleta, id=boleta_id, usuario=request.user)
    items = boleta.itemboleta_set.all()  
    total = boleta.total  

    return render(request, 'web/detalle_boleta.html', {
        'boleta': boleta,
        'items': items,
        'total': total
    })

def mostrar_boleta(request, boleta_id):
  
    boleta = get_object_or_404(Boleta, pk=boleta_id)
   
    return render(request, 'web/mostrar_boleta.html', {'boleta': boleta})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')  
def detalles_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    return render(request, 'web/detalles_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')  
def confirmar_eliminacion_usuario(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'El usuario {username} ha sido eliminado exitosamente.')
        return redirect('dashboard')
    else:
        return render(request, 'web/confirmar_eliminar_usuario.html', {'usuario': user})


@login_required
def confirmar_eliminar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if request.method == 'POST':
        item.delete()
        messages.info(request, 'El producto ha sido eliminado del carrito.')
        return redirect('carrito')
    else:
        
        return render(request, 'web/confirmar_eliminar_producto.html', {'item': item})
    


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')  
def gestion_productos(request):
    productos = Producto.objects.all()
    return render(request, 'web/gestion_productos.html', {'productos': productos})


def confirmar_eliminar_gestion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect('gestion_productos')

    return render(request, 'web/confirmar_eliminar_gestion.html', {'producto': producto})


def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('gestion_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'web/editar_producto.html', {'form': form})


