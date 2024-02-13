from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class ProdjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_tasks', 'undone_tasks', 'owner', 'recent_tasks']
    list_display_links = ['id', 'name']
    list_filter = ['owner']
    search_fields = ['name']
    fieldsets = (
        (None, {
            "fields": (
                ('name', 'owner')
            ),
        }),
    )

    def total_tasks(self, objektas: models.Project):
        return objektas.tasks_count()
    total_tasks.short_description =_("total tasks")

    def undone_tasks(self, objektas: models.Project):
        return objektas.tasks.filter(is_done=False).count()
    undone_tasks.short_description =_("undone tasks")
    
    def recent_tasks(self, objektas: models.Project):
        return "; ".join(objektas.tasks_order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _("recent tasks")    


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'deadline', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'deadline', 'created_at']
    search_fields = ['name', 'description', 'project__name', 'owner__lasst_name']    
    list_editable = ['is_done', 'owner', 'project']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (("general").title(), {
            "fields": (
                ('name', 'deadline'),
                'description', 'is_done',
                
            ),
        }),
    
    
        (("ownership").title(), {
            "fields": (
                ('owner', 'project'),
                
            ),
        }),
    
    
        (("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
                
            ),
        }),
    )
    











admin.site.register(models.Project, ProdjectAdmin)
admin.site.register(models.Task, TaskAdmin)

