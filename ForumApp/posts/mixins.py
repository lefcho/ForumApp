from datetime import time

from django import forms
from django.http import HttpResponseForbidden
from django.utils.timezone import localtime


class DisableFieldsMixin(forms.Form):
    disabled_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if self.disabled_fields[0] == '__all__' or field in self.disabled_fields:
                self.fields[field].disabled = True


class TimeRestrictionMixin:
    start_time = time(0, 0)
    end_time = time(23, 0)
    forbidden_message = 'Access restricted at current time. Please try again later.'

    def dispatch(self, request, *args, **kwargs):
        current_time = localtime().time()
        print(current_time)
        if not (self.start_time <= current_time <= self.end_time):
            return HttpResponseForbidden(self.forbidden_message)

        return super().dispatch(request, *args, **kwargs)
