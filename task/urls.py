from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("categorias/<int:category_id>/tareas/", views.task_list, name="task_list_by_category"),
    path("etiquetas/<int:tag_id>/tareas/", views.task_list, name="task_list_by_tag"),
    path("tareas/nueva/", views.task_create, name="task_create"),
    path("tareas/<int:pk>/", views.task_detail, name="task_detail"),
    path("tareas/<int:pk>/editar/", views.task_update, name="task_update"),
    path("tareas/<int:pk>/completar/", views.task_complete, name="task_complete"),
    path("feedback", views.feedback_create, name="feedback_create"),
    path("feedback/list", views.feedback_list, name="feedback_list"),
]