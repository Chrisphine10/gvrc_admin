# -*- encoding: utf-8 -*-
"""
Document management forms for GVRC Admin
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Document
from apps.lookups.models import DocumentType, GBVCategory
from apps.common.utils import validate_file_extension, validate_file_size, secure_filename


class DocumentForm(forms.ModelForm):
    """Form for creating and editing documents"""
    
    class Meta:
        model = Document
        fields = [
            'title', 'description', 'file', 'content', 'document_type',
            'gbv_category', 'image_url', 'external_url', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter document description'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter document content (if no file uploaded)'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'gbv_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/document.pdf'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set querysets for foreign key fields
        self.fields['document_type'].queryset = DocumentType.objects.all().order_by('type_name')
        self.fields['gbv_category'].queryset = GBVCategory.objects.all().order_by('category_name')
        
        # Make gbv_category optional
        self.fields['gbv_category'].required = False
        
        # Add help text
        self.fields['file'].help_text = 'Upload a document file (PDF, DOC, DOCX, etc.)'
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.rtf,.odt'
        })
    
    def clean(self):
        """Custom validation for the form"""
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        content = cleaned_data.get('content')
        external_url = cleaned_data.get('external_url')
        
        # At least one of file, content, or external_url must be provided
        if not file and not content and not external_url:
            raise ValidationError(
                _('Please provide either a file upload, content, or external URL.')
            )
        
        # If file is uploaded, validate it
        if file:
            # Validate file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']
            if not validate_file_extension(file.name, allowed_extensions):
                raise ValidationError(
                    _('File type not allowed. Please upload a document file (PDF, DOC, DOCX, TXT, RTF, or ODT).')
                )
            
            # Validate file size (default 10MB, can be overridden by document type)
            document_type = cleaned_data.get('document_type')
            max_size_mb = 10  # Default max size
            
            if document_type and hasattr(document_type, 'max_file_size_mb'):
                max_size_mb = document_type.max_file_size_mb
            
            if not validate_file_size(file, max_size_mb):
                raise ValidationError(
                    _('File size exceeds the maximum allowed size of %(max_size)s MB.') % {
                        'max_size': max_size_mb
                    }
                )
            
            # Store original filename for later use
            cleaned_data['_original_filename'] = secure_filename(file.name)
        
        return cleaned_data
    
    def save(self, commit=True):
        """Override save to handle original filename"""
        instance = super().save(commit=False)
        
        # Set original filename if file is uploaded
        if self.cleaned_data.get('_original_filename'):
            instance.set_original_filename(self.cleaned_data['_original_filename'])
        
        if commit:
            instance.save()
        
        return instance


class DocumentUploadForm(forms.Form):
    """Simple form for bulk document uploads"""
    
    file = forms.FileField(
        label='Document File',
        help_text='Select a document file to upload',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.rtf,.odt'
        })
    )
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter document title'
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter document description (optional)'
        })
    )
    
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all().order_by('type_name'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_public = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Validate file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']
            if not validate_file_extension(file.name, allowed_extensions):
                raise ValidationError(
                    _('File type not allowed. Please upload a document file (PDF, DOC, DOCX, TXT, RTF, or ODT).')
                )
            
            # Validate file size
            if not validate_file_size(file, 10):  # 10MB limit
                raise ValidationError(
                    _('File size exceeds the maximum allowed size of 10 MB.')
                )
        
        return file

