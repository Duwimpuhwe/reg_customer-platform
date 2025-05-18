from django import forms
from django.core.validators import validate_email
from .models import ProjectApplication
from django.forms import widgets
from django.core.exceptions import ValidationError

class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        model = ProjectApplication
        fields = [
            'project_id', 
            # 'serial_number', 
            # 'application_date', 
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
            'comments'
        ]

        # Define widgets for the form fields
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'project_owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project owner'}),
            'project_owner_tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project owner phone number', 'type': 'tel'}),
            'project_owner_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter project owner email'}),
            'project_implementor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project implementor'}),
            'implementor_tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter implementor phone number', 'type': 'tel'}),
            'implementor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter implementor email'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sector'}),
            'cell': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cell'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter village'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter latitude (e.g., 1.9501 or 1°57′0″S)'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter longitude (e.g., 30.0500 or 30°3′0″E)'}),
            'load_capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter load capacity'}),
            'load_capacity_unit': forms.Select(attrs={'class': 'form-control'}),
            'tx_capacity_kva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter transformer capacity in kVA, note:float value (e.g. 100.0)'}),
            'proof_survey_fee_attachments': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'project_category': forms.Select(attrs={'class': 'form-control'}),
            'eucl_scope': forms.Select(attrs={'class': 'form-control'}),
            'attachments': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter comments', 'rows': 4}),
        }

        help_texts = {
            'attachments': 'Zip the files or merge them into a single file if there is more than one.',
            'proof_survey_fee_attachments': 'Attach proof of survey fee payment.'
        }

    def clean(self):
        cleaned_data = super().clean()

        # Custom validation for email fields
        project_owner_email = cleaned_data.get('project_owner_email')
        implementor_email = cleaned_data.get('implementor_email')

        if project_owner_email:
            try:
                validate_email(project_owner_email)  # Explicitly validate the email
            except ValidationError:
                self.add_error('project_owner_email', "Invalid email format. Please enter a valid project owner email.")
        
        if implementor_email:
            try:
                validate_email(implementor_email)  # Explicitly validate the email
            except ValidationError:
                self.add_error('implementor_email', "Invalid email format. Please enter a valid implementor email.")
        
        return cleaned_data