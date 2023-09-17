from django.contrib import admin
from .models import StudentStatus
from leaflet.admin import LeafletGeoAdmin
from django import forms
from subjects.models import SubjectInstance
from accounts.models import CustomUser


class CustomStudentStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomStudentStatusForm, self).__init__(*args, **kwargs)
        if self.instance:
            studentstatus = StudentStatus.objects.filter(
                user=self.instance.user).first()
            user = CustomUser.objects.filter(
                id=studentstatus.user.id).first()
            subjects = SubjectInstance.objects.filter(
                course=user.course)
            self.fields['subject'].queryset = subjects

    subject = forms.ModelMultipleChoiceField(
        queryset=SubjectInstance.objects.none(), required=False)

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
