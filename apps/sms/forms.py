from django import forms

from apps.authentication.models import UserRole
from apps.geography.models import Constituency, County, Ward
from apps.lookups.models import GBVCategory

from .models import SmsSettings
from .services import MAX_MESSAGE_LENGTH, is_sendable_phone, normalize_phone, parse_custom_numbers, split_phone_values

_input = {"class": "form-control"}
_select = {"class": "form-control"}


class BroadcastForm(forms.Form):
    title = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs=_input | {"placeholder": "e.g. County focal persons - December meeting"}),
        help_text="Only staff see this.",
    )
    message = forms.CharField(
        max_length=MAX_MESSAGE_LENGTH,
        widget=forms.Textarea(attrs=_input | {"rows": 5, "id": "sms-message",
                                              "placeholder": "Hello {name}, ..."}),
        help_text="{name} becomes the recipient's first name. 160 characters = 1 SMS.",
    )

    facilities = forms.BooleanField(required=False, label="Facility contacts (service providers)",
                                      widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    county = forms.ModelChoiceField(queryset=County.objects.none(), required=False, empty_label="All counties",
                                    widget=forms.Select(attrs=_select))
    constituency = forms.ModelChoiceField(queryset=Constituency.objects.none(), required=False,
                                          empty_label="All constituencies", widget=forms.Select(attrs=_select))
    ward = forms.ModelChoiceField(queryset=Ward.objects.none(), required=False, empty_label="All wards",
                                  widget=forms.Select(attrs=_select))
    gbv_category = forms.ModelChoiceField(queryset=GBVCategory.objects.none(), required=False,
                                          empty_label="Any GBV service", widget=forms.Select(attrs=_select))
    primary_only = forms.BooleanField(required=False, label="Primary contact of each facility only",
                                        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))

    staff = forms.BooleanField(required=False, label="Staff users of this admin",
                                 widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    role = forms.ModelChoiceField(queryset=UserRole.objects.none(), required=False, empty_label="All roles",
                                  widget=forms.Select(attrs=_select))

    custom_numbers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs=_input | {"rows": 4, "placeholder": "0712345678, Jane Wanjiku\n0722000111\n254733222333"}),
        label="Other numbers",
        help_text="One per line, or comma-separated. Add a name after a comma: 0712345678, Jane.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["county"].queryset = County.objects.order_by("county_name")
        self.fields["constituency"].queryset = Constituency.objects.select_related("county").order_by("constituency_name")
        self.fields["ward"].queryset = Ward.objects.order_by("ward_name")
        self.fields["gbv_category"].queryset = GBVCategory.objects.order_by("category_name")
        self.fields["role"].queryset = UserRole.objects.order_by("role_name")

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise forms.ValidationError("Write the message to send.")
        return message

    def clean(self):
        data = super().clean()
        if not (data.get("facilities") or data.get("staff") or (data.get("custom_numbers") or "").strip()):
            raise forms.ValidationError("Choose at least one group of recipients, or type some numbers.")
        return data

    def audience_spec(self):
        d = self.cleaned_data
        return {
            "facilities": bool(d.get("facilities")),
            "county": d["county"].pk if d.get("county") else None,
            "constituency": d["constituency"].pk if d.get("constituency") else None,
            "ward": d["ward"].pk if d.get("ward") else None,
            "gbv_category": d["gbv_category"].pk if d.get("gbv_category") else None,
            "primary_only": bool(d.get("primary_only")),
            "staff": bool(d.get("staff")),
            "role": d["role"].pk if d.get("role") else None,
            "custom_numbers": d.get("custom_numbers") or "",
        }


class SmsSettingsForm(forms.ModelForm):
    """Secrets are write-only: the page never sends them back to the browser.
    Leaving a secret box empty keeps the saved value; tick "clear" to remove it."""

    SECRET_FIELDS = ("client_id", "api_key", "api_secret", "service_id")

    clear_saved_credentials = forms.BooleanField(
        required=False, label="Clear the saved credentials (fall back to the server environment)",
    )

    class Meta:
        model = SmsSettings
        fields = [
            "enabled", "provider_name", "sender_id", "client_id", "api_key", "api_secret", "service_id", "endpoint",
            "notify_assigned_staff", "notify_new_chats", "notify_urgent_messages", "alert_numbers",
        ]
        widgets = {
            "provider_name": forms.TextInput(attrs=_input),
            "sender_id": forms.TextInput(attrs=_input),
            "client_id": forms.PasswordInput(attrs=_input | {"autocomplete": "off"}, render_value=False),
            "api_key": forms.PasswordInput(attrs=_input | {"autocomplete": "new-password"}, render_value=False),
            "api_secret": forms.PasswordInput(attrs=_input | {"autocomplete": "new-password"}, render_value=False),
            "service_id": forms.PasswordInput(attrs=_input | {"autocomplete": "off"}, render_value=False),
            "endpoint": forms.URLInput(attrs=_input | {"placeholder": SmsSettings.DEFAULT_ENDPOINT}),
            "alert_numbers": forms.Textarea(attrs=_input | {"rows": 3, "placeholder": "0712345678, 0733111222"}),
        }

    def clean_alert_numbers(self):
        # split_phone_values splits on new lines and strips each part.
        parts = split_phone_values(self.cleaned_data.get("alert_numbers") or "")
        bad = [p for p in parts if not is_sendable_phone(p)]
        if bad:
            raise forms.ValidationError("Not a Kenyan mobile number: " + ", ".join(bad))
        return ", ".join(dict.fromkeys(normalize_phone(p) for p in parts))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remember saved secrets before binding overwrites them with blanks.
        self._saved = {n: getattr(self.instance, n, "") or "" for n in self.SECRET_FIELDS}
        for name in self.SECRET_FIELDS:
            self.fields[name].required = False
            if self._saved[name]:
                self.fields[name].widget.attrs["placeholder"] = "Saved - leave empty to keep"

    def save(self, commit=True):
        obj = super().save(commit=False)
        clear = self.cleaned_data.get("clear_saved_credentials")
        for name in self.SECRET_FIELDS:
            typed = (self.cleaned_data.get(name) or "").strip()
            setattr(obj, name, "" if clear else (typed or self._saved[name]))
        if commit:
            obj.save()
        return obj


class TestSmsForm(forms.Form):
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs=_input | {"placeholder": "0712345678"}))
    message = forms.CharField(
        max_length=160, initial="Hodi test message: SMS from the Hodi admin is working.",
        widget=forms.TextInput(attrs=_input),
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not is_sendable_phone(phone):
            raise forms.ValidationError("Enter a Kenyan mobile number, e.g. 0712345678.")
        return phone


__all__ = ["BroadcastForm", "SmsSettingsForm", "TestSmsForm", "parse_custom_numbers"]
