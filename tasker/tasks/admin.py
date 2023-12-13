from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_tasks', 'recent_undone_tasks', 'owner']
    list_filter = ['owner']
    search_fields = ['name']
    list_display_links = ['name']

    def total_tasks(self, obj: models.Project):
        return obj.tasks.count()
    total_tasks.short_description = _('total tasks')

    def undone_tasks(self, obj: models.Project):
        return obj.tasks.filter(is_done=False).count()
    undone_tasks.short_description = _('undone tasks')

    def recent_tasks(self, obj: models.Project):
        return "; ".join(obj.tasks.order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _('recent tasks')

    def recent_undone_tasks(self, obj: models.Project):
        return "; ".join(obj.tasks.filter(is_done=False).order_by('-created_at').values_list('name', flat=True)[:3])
    recent_tasks.short_description = _('recent tasks')


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_done', 'project', 'owner', 'created_at']
    list_filter = ['is_done', 'created_at']
    search_fields = ['name', 'description', 'project__name', 'owner__last_name', 'owner__username']
    list_editable = ['is_done']
    readonly_fields = ['created_at', 'updated_at', 'id']
    fieldsets = (
        (_('General'), {
            "fields": (
                ('id', 'is_done', 'name'), 'description',
            ),
        }),
        (_('Ownership'), {
            "fields": (
                ('owner', 'project'),
            ),
        }),
        (_('Temporal Tracking'), {
            "fields": (
                ('created_at', 'updated_at'),
            ),
        }),
    )


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
