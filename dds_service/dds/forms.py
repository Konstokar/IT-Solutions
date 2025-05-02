from django import forms
from .models import MoneyMovement, Status, OperationType, Category, SubCategory


class MoneyMovementForm(forms.ModelForm):
    class Meta:
        model = MoneyMovement
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтрация категорий по выбранному типу операции
        if 'operation_type' in self.data:
            try:
                operation_type_id = int(self.data.get('operation_type'))
                self.fields['category'].queryset = Category.objects.filter(operation_type_id=operation_type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.operation_type.category_set.all()

        # Фильтрация подкатегорий по выбранной категории
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()