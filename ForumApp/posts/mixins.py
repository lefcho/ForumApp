from django import forms


class DisableFieldsMixin(forms.Form):
    disabled_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if self.disabled_fields[0] == '__all__' or field in self.disabled_fields:
                self.fields[field].disabled = True
