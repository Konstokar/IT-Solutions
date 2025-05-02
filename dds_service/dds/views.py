from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MoneyMovement, Status, OperationType, Category, SubCategory
from .forms import MoneyMovementForm
from django.db.models import Q
from datetime import datetime


class MoneyMovementListView(ListView):
    model = MoneyMovement
    template_name = 'dds/money_movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по дате
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(date__gte=datetime.strptime(date_from, '%Y-%m-%d').date())
        if date_to:
            queryset = queryset.filter(date__lte=datetime.strptime(date_to, '%Y-%m-%d').date())

        # Фильтрация по другим параметрам
        filters = {
            'status': 'status',
            'operation_type': 'operation_type',
            'category': 'category',
            'subcategory': 'subcategory',
        }

        for param, field in filters.items():
            value = self.request.GET.get(param)
            if value:
                queryset = queryset.filter(**{f'{field}__id': value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['operation_types'] = OperationType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()

        # Сохраняем параметры фильтрации для формы
        for param in ['date_from', 'date_to', 'status', 'operation_type', 'category', 'subcategory']:
            context[param] = self.request.GET.get(param)

        return context


class MoneyMovementCreateView(CreateView):
    model = MoneyMovement
    form_class = MoneyMovementForm
    template_name = 'dds/money_movement_form.html'
    success_url = reverse_lazy('money_movement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать запись о движении денежных средств'
        return context


class MoneyMovementUpdateView(UpdateView):
    model = MoneyMovement
    form_class = MoneyMovementForm
    template_name = 'dds/money_movement_form.html'
    success_url = reverse_lazy('money_movement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать запись о движении денежных средств'
        return context


class MoneyMovementDeleteView(DeleteView):
    model = MoneyMovement
    template_name = 'dds/money_movement_confirm_delete.html'
    success_url = reverse_lazy('money_movement_list')


def load_categories(request):
    operation_type_id = request.GET.get('operation_type')
    categories = Category.objects.filter(operation_type_id=operation_type_id)
    return render(request, 'dds/category_dropdown_list_options.html', {'categories': categories})


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 'dds/subcategory_dropdown_list_options.html', {'subcategories': subcategories})