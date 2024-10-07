from django.urls import path
from .views import (
    evento_list,
    evento_create,
    evento_update,
    evento_delete,
    mostrar_eventos_y_usuarios,
    registrar_usuario,
    registro_evento_list,
    registro_evento_create,
    registro_evento_update,
    registro_evento_delete,
    evento_detail,
    registro_evento_detail,
    registro,
    login_view,
    cantidad_usuarios_evento,
    cantidad_eventos_mes_actual,
    usuarios_mas_activos,
    eventos_organizados_por_usuario,
)

urlpatterns = [
    # Rutas de gestión de eventos
    path('', evento_list, name='evento_list'),
    path('nuevo/', evento_create, name='evento_create'),
    path('editar/<int:pk>/', evento_update, name='evento_update'),
    path('eliminar/<int:pk>/', evento_delete, name='evento_delete'),
    path('detalle/<int:pk>/', evento_detail, name='evento_detail'),
    path('registrar-usuarios/', mostrar_eventos_y_usuarios, name='mostrar_eventos_y_usuarios'),  
    path('registrar/<int:evento_pk>/<int:usuario_pk>/', registrar_usuario, name='registrar_usuario'),
    
    # Nuevas rutas para el CRUD de registros de eventos
    path('registros/', registro_evento_list, name='registro_evento_list'),  # Listar registros
    path('registros/nuevo/', registro_evento_create, name='registro_evento_create'),  # Crear registro
    path('registros/editar/<int:pk>/', registro_evento_update, name='registro_evento_update'),  # Editar registro
    path('registros/eliminar/<int:pk>/', registro_evento_delete, name='registro_evento_delete'),  # Eliminar registro
    path('registros/detalle/<int:pk>/', registro_evento_detail, name='registro_evento_detail'),  # Detalle del registro

    # Rutas para el login y registro
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),

    # Rutas para mostrar el orm
    path('evento/<int:evento_id>/usuarios/', cantidad_usuarios_evento, name='cantidad_usuarios_evento'),
    path('eventos/mes/', cantidad_eventos_mes_actual, name='cantidad_eventos_mes'),
    path('usuarios/activos/', usuarios_mas_activos, name='usuarios_mas_activos'),
    path('usuarios/<int:usuario_id>/eventos-organizados/', eventos_organizados_por_usuario, name='eventos_organizados_por_usuario'),
]
