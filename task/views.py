from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TaskCompleteForm, TaskForm, FeedbackForm
from .models import Category, Feedback, Tag, Task


def task_list(request, category_id=None, tag_id=None):
    tasks = Task.objects.select_related("category").prefetch_related("tags")
    category = None
    tag = None

    if category_id is not None:
        category = get_object_or_404(Category, pk=category_id)
        tasks = tasks.filter(category=category)

    if tag_id is not None:
        tag = get_object_or_404(Tag, pk=tag_id)
        tasks = tasks.filter(tags=tag)

    query = request.GET.get("q", "").strip()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "category": category,
        "tag": tag,
        "query": query,
        "categories": Category.objects.order_by("name"),
        "tags": Tag.objects.order_by("name"),
    }
    return render(request, "task/task_list.html", context)


def task_detail(request, pk):
    task = get_object_or_404(Task.objects.select_related("category").prefetch_related("tags"), pk=pk)
    complete_form = TaskCompleteForm(initial={"confirm": True})
    return render(
        request,
        "task/task_detail.html",
        {"task": task, "complete_form": complete_form},
    )


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, "Tarea creada correctamente.")
            return redirect(reverse("task_detail", args=[task.pk]))
    else:
        form = TaskForm()
    return render(request, "task/task_form.html", {"form": form, "title": "Nueva tarea"})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarea actualizada correctamente.")
            return redirect(reverse("task_detail", args=[task.pk]))
    else:
        form = TaskForm(instance=task)
    return render(request, "task/task_form.html", {"form": form, "title": "Editar tarea"})


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskCompleteForm(request.POST)
        if form.is_valid():
            task.completed = True
            task.save(update_fields=["completed", "updated_at"])
            messages.success(request, "La tarea fue marcada como completada.")
        else:
            messages.warning(request, "Debes confirmar la accion para marcar la tarea como completada.")
    return redirect(reverse("task_detail", args=[task.pk]))

def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = FeedbackForm()

    return render(request, 'task/feedback_form.html', {'form': form, 'title': 'Deja tu feedback'})

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'task/feedback_list.html', {'feedbacks': feedbacks})