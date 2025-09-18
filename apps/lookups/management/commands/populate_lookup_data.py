# -*- encoding: utf-8 -*-
"""
Management command to populate all lookup data
"""

from django.core.management.base import BaseCommand
from apps.lookups.models import DocumentType, GBVCategory


class Command(BaseCommand):
    help = 'Populate all lookup data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--document-types',
            action='store_true',
            help='Populate document types only',
        )
        parser.add_argument(
            '--gbv-categories',
            action='store_true',
            help='Populate GBV categories only',
        )

    def handle(self, *args, **options):
        """Populate lookup data based on options"""
        
        if options['document_types'] or not any([options['document_types'], options['gbv_categories']]):
            self.populate_document_types()
        
        if options['gbv_categories'] or not any([options['document_types'], options['gbv_categories']]):
            self.populate_gbv_categories()

    def populate_document_types(self):
        """Create default document types if they don't exist"""
        
        document_types = [
            {
                'type_name': 'Policy Document',
                'description': 'Official policy or procedure documents',
                'allowed_extensions': '["pdf", "doc", "docx"]',
                'max_file_size_mb': 10
            },
            {
                'type_name': 'Training Material',
                'description': 'Training guides, manuals, or educational materials',
                'allowed_extensions': '["pdf", "doc", "docx", "ppt", "pptx"]',
                'max_file_size_mb': 15
            },
            {
                'type_name': 'Report',
                'description': 'Incident reports, case studies, or research reports',
                'allowed_extensions': '["pdf", "doc", "docx", "xls", "xlsx"]',
                'max_file_size_mb': 10
            },
            {
                'type_name': 'Form',
                'description': 'Official forms, applications, or templates',
                'allowed_extensions': '["pdf", "doc", "docx", "xls", "xlsx"]',
                'max_file_size_mb': 5
            },
            {
                'type_name': 'Reference Material',
                'description': 'Reference guides, directories, or informational materials',
                'allowed_extensions': '["pdf", "doc", "docx", "txt", "rtf"]',
                'max_file_size_mb': 10
            },
            {
                'type_name': 'Legal Document',
                'description': 'Legal documents, contracts, or agreements',
                'allowed_extensions': '["pdf", "doc", "docx"]',
                'max_file_size_mb': 10
            },
            {
                'type_name': 'Image Document',
                'description': 'Images, photos, or visual materials',
                'allowed_extensions': '["jpg", "jpeg", "png", "gif", "bmp", "tiff"]',
                'max_file_size_mb': 5
            },
            {
                'type_name': 'Other',
                'description': 'Other types of documents not covered above',
                'allowed_extensions': '["pdf", "doc", "docx", "txt", "rtf", "odt"]',
                'max_file_size_mb': 10
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for doc_type_data in document_types:
            doc_type, created = DocumentType.objects.get_or_create(
                type_name=doc_type_data['type_name'],
                defaults={
                    'description': doc_type_data['description'],
                    'allowed_extensions': doc_type_data['allowed_extensions'],
                    'max_file_size_mb': doc_type_data['max_file_size_mb']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created document type: {doc_type.type_name}')
                )
            else:
                # Update existing document type with missing fields
                if not doc_type.allowed_extensions:
                    doc_type.allowed_extensions = doc_type_data['allowed_extensions']
                    doc_type.max_file_size_mb = doc_type_data['max_file_size_mb']
                    doc_type.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated document type: {doc_type.type_name}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Document types population complete. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )

    def populate_gbv_categories(self):
        """Create default GBV categories if they don't exist"""
        
        gbv_categories = [
            {
                'category_name': 'Physical Violence',
                'description': 'Physical harm or injury inflicted on a person'
            },
            {
                'category_name': 'Sexual Violence',
                'description': 'Any sexual act or attempt to obtain a sexual act by violence or coercion'
            },
            {
                'category_name': 'Emotional/Psychological Violence',
                'description': 'Verbal abuse, threats, intimidation, or other psychological harm'
            },
            {
                'category_name': 'Economic Violence',
                'description': 'Control over financial resources, employment, or economic opportunities'
            },
            {
                'category_name': 'Digital Violence',
                'description': 'Online harassment, cyberbullying, or digital abuse'
            },
            {
                'category_name': 'Institutional Violence',
                'description': 'Violence perpetrated by institutions or systems'
            }
        ]
        
        created_count = 0
        
        for category_data in gbv_categories:
            category, created = GBVCategory.objects.get_or_create(
                category_name=category_data['category_name'],
                defaults={
                    'description': category_data['description']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created GBV category: {category.category_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'GBV categories population complete. Created: {created_count}'
            )
        )
