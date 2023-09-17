from django.contrib import admin
from .models import StudentStatus
from leaflet.admin import LeafletGeoAdmin
from django import forms
from subjects.models import SubjectInstance, Subject
from accounts.models import CustomUser


class CustomStudentStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomStudentStatusForm, self).__init__(*args, **kwargs)
        if self.instance:
            studentstatus = StudentStatus.objects.filter(
                user=self.instance.user).first()
            user = CustomUser.objects.filter(
                id=studentstatus.user.id).first()
            subject_instances = SubjectInstance.objects.filter(
                course=user.course)
            # Get the names of the SubjectInstance objects
            subject_instance_names = subject_instances.values_list(
                'subject', flat=True)

            # Filter the Subject objects by these names
            subjects = Subject.objects.filter(name__in=subject_instance_names)
            self.fields['subject'].queryset = subjects

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(), required=False)

    class Meta:
        model = StudentStatus
        fields = '__all__'


class StudentStatusAdmin(LeafletGeoAdmin):
    model = StudentStatus
    form = CustomStudentStatusForm
    # define which fields are required

    def get_form(self, request, obj=None, **kwargs):
        form = super(StudentStatusAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['landmark'].required = False
        return form


# Register the new StudentStatus model
admin.site.register(StudentStatus, StudentStatusAdmin)
