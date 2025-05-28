from django.contrib import admin
from .models import ProjectApplication #added after to register the model

# Register your models here.

# admin.site.register(ProjectApplication)
@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ('project_id', 
            'serial_number', 
            'application_date', 
            'project_name', 
            'project_owner', 
            'project_owner_tel', 
            'project_owner_email',
            'project_implementor', 
            'implementor_tel', 
            'implementor_email',
            'district', 
            'sector', 
            'cell', 
            'village', 
            'latitude', 
            'longitude', 
            'load_capacity', 
            'load_capacity_unit', 
            'tx_capacity_kva', 
            'proof_survey_fee_attachments', 
            'project_category', 
            'eucl_scope', 
            'attachments', 
            'comments')