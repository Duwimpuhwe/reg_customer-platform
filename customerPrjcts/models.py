from django.db import models
from django.db.models.signals import post_delete, pre_save # Added 
from django.dispatch import receiver # Added
from django.core.exceptions import ValidationError # Added
from django.core.validators import validate_email #A ddded

# Create your models here.

class ProjectApplication(models.Model):

  # Basic info
  project_id = models.AutoField(primary_key=True)
  serial_number = models.PositiveIntegerField(unique=True, blank=True, null=True)  # Auto-adjusted column
  application_date = models.DateField(auto_now_add=True)
  
  # Project Details
  project_name = models.CharField(max_length=255)
  project_owner = models.CharField(max_length=100)
  project_owner_tel = models.CharField(max_length=20, blank=True, null=True)
  project_owner_email = models.EmailField(blank=True, null=True)

  # Implementor Details
  project_implementor = models.CharField(max_length=100)
  implementor_tel = models.CharField(max_length=16, blank=True, null=True)
  implementor_email = models.EmailField(blank=True, null=True)

  # Location Information district
  District_CHOICES=[
      ('Kirehe', 'Kirehe'),
      ('Ngoma', 'Ngoma'),
      ('Kayonza', 'Kayonza'),
      ('Bugesera', 'Bugesera'),
      ('Rwamagana', 'Rwamagana'),
      ('Gatsibo', 'Gatsibo'),
      ('Nyagatare', 'Nyagatare'),
      ('Gicumbi', 'Gicumbi'),
      ('Rulindo', 'Rulindo'),
      ('Gakenke', 'Gakenke'),
      ('Musanze', 'Musanze'),
      ('Burera', 'Burera'),
      ('Nyabihu', 'Nyabihu'),
      ('Rubavu', 'Rubavu'),
      ('Nyamasheke', 'Nyamasheke'),
      ('Karongi', 'Karongi'),
      ('Rutsiro', 'Rutsiro'),
      ('Muhanga', 'Muhanga'),
      ('Kamonyi', 'Kamonyi'),
      ('Ruhango', 'Ruhango'),
      ('Nyanza', 'Nyanza'),
      ('Gisagara', 'Gisagara'),
      ('Huye', 'Huye'),
      ('Nyamagabe', 'Nyamagabe'),
      ('Ngororero', 'Ngororero'),
      ('Nyaruguru', 'Nyaruguru'),
      ('Rusizi', 'Rusizi'),
      ('Nyarugenge', 'Nyarugenge'),
      ('Kicukiro', 'Kicukiro'),
      ('Gasabo', 'Gasabo'),
  ]
  district = models.CharField(max_length=100, choices=District_CHOICES)
  # Location Information district
  sector = models.CharField(max_length=100)
  cell = models.CharField(max_length=100)
  village = models.CharField(max_length=100)

  # Geolocation (Latitude & Longitude)
  latitude = models.CharField(max_length=50, blank=True, null=True)
  longitude = models.CharField(max_length=50, blank=True, null=True)

  # Load & Capacity Details
  load_capacity = models.FloatField(blank=True, null=True)
  load_capacity_unit = models.CharField(max_length=10, choices=[('KW', 'KW'), ('KVA', 'KVA')], blank=True, null=True)
  tx_capacity_kva = models.FloatField(blank=True, null=True)

  # Proof of Survey Fee (Multiple Files)
  proof_survey_fee_attachments = models.ManyToManyField('ProjectFile', blank=True, related_name='proof_survey_fee_files')

  # Project Category
  PROJECT_CATEGORIES = [
      ('Residential', 'Residential'),
      ('Commercial', 'Commercial'),
      ('Industrial', 'Industrial'),
      ('College', 'College'),
      ('Mining', 'Mining'),
      ('EV', 'EV'),
      ('Telecom tower', 'Telecom tower'),
      ('Broadcasters', 'Broadcasters'),
      ('Hotels', 'Hotels'),
      ('Water SS Or TP', 'Water SS Or TP'),
      ('Health', 'Health'),
      ('Data Centers', 'Data Centers'),
      ('Airport', 'Airport'),
      ('Govt intitution', 'Govt intitution'),
      ('Street light', 'Street light'),
  ]
  project_category = models.CharField(max_length=50, choices=PROJECT_CATEGORIES, blank=True, null=True)

  # EUCL Scope
  EUCL_SCOPE_CHOICES = [
      ('Supply&Installation', 'Supply&Installation'),
      ('Installation', 'Installation'),
      ('Supervision', 'Supervision'),
  ]
  eucl_scope = models.CharField(max_length=50, choices=EUCL_SCOPE_CHOICES, blank=True, null=True)

  # General Attachments (Multiple Files)
  attachments = models.ManyToManyField('ProjectFile', blank=True, related_name='project_attachments')

  # Comments Section
  comments = models.TextField(blank=True, null=True)

  def save(self, *args, **kwargs):
        """ Assigns the next available serial number when a new item is created. """
        if self.serial_number is None:
            last_serial = ProjectApplication.objects.aggregate(models.Max('serial_number'))['serial_number__max'] or 0
            self.serial_number = last_serial + 1
        super().save(*args, **kwargs)

  def clean(self):
      if self.project_owner_email:
        try:
            validate_email(self.project_owner_email)
        except ValidationError:
            raise ValidationError({"project_email": "Invalid email format. Please enter a valid project owner email."})

       # Validate implementor_email
      if self.implementor_email:
        try:
            validate_email(self.implementor_email)
        except ValidationError:
            raise ValidationError({"implementor_email": "Invalid email format. Please enter a valid implementor email."})

  def __str__(self):
        return f"{self.project_name} ({self.district}, {self.sector})"
  
@receiver(post_delete, sender=ProjectApplication)
def save(self, *args, **kwargs):
        if self.serial_number is None:  # Assign only if it's empty
            last_entry = ProjectApplication.objects.order_by('-serial_number').first()
            self.serial_number = (last_entry.serial_number + 1) if last_entry else 1
        super().save(*args, **kwargs)

class ProjectFile(models.Model):
    file = models.FileField(upload_to='project_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

