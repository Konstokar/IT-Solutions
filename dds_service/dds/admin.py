from django.contrib import admin
from .models import Status, OperationType, Category, SubCategory, MoneyMovement

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'operation_type')
    list_filter = ('operation_type',)
    inlines = [SubCategoryInline]

class MoneyMovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'operation_type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = ('status', 'operation_type', 'category', 'subcategory', 'date')
    search_fields = ('comment', 'amount')
    date_hierarchy = 'date'
    ordering = ('-date',)

admin.site.register(Status)
admin.site.register(OperationType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(MoneyMovement, MoneyMovementAdmin)