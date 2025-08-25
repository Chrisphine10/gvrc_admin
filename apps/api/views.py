# -*- encoding: utf-8 -*-
"""
API views for GVRC Admin - Mobile App Focused
"""

from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Prefetch
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    FacilityListSerializer, FacilityDetailSerializer, FacilitySearchSerializer,
    FacilityMapSerializer, StatisticsSerializer, CountySerializer,
    ConstituencySerializer, WardSerializer, ConsolidatedGeographySerializer, OperationalStatusSerializer,
    ServiceCategorySerializer, ContactTypeSerializer, OwnerTypeSerializer,
    GBVCategorySerializer, InfrastructureTypeSerializer, ConditionStatusSerializer, DocumentTypeSerializer,
    LookupDataResponseSerializer, MobileLookupDataSerializer, EmergencySearchSerializer,
    GBVServiceSearchSerializer, ReferralChainSerializer,
    ReferralOutcomeSerializer, FacilityCompleteSerializer,
    MobileAppFacilitySerializer, MusicSerializer,
    DocumentSerializer, MobileSessionSerializer, MobileSessionCreateSerializer,
    MobileSessionUpdateSerializer, GameScoreUpdateSerializer
)
from apps.facilities.models import (
    Facility, FacilityContact, FacilityService, 
    FacilityOwner, FacilityCoordinate, FacilityGBVCategory
)
from apps.authentication.models import User, UserSession, CustomToken
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import (
    OperationalStatus, ContactType, ServiceCategory, 
    OwnerType, GBVCategory, InfrastructureType, ConditionStatus, DocumentType
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import hashlib
from apps.analytics.models import ContactInteraction
import time
from django.utils import timezone


class MobileSessionPermission(BasePermission):
    """
    Custom permission class for mobile API endpoints.
    Validates device_id from request body or query parameters and checks if mobile session exists and is active.
    """
    
    message = "Valid mobile session required. Please provide a valid device_id."
    
    def has_permission(self, request, view):
        # For GET requests, get device_id from query parameters
        # For POST/PUT requests, get device_id from request body
        if request.method == 'GET':
            device_id = request.query_params.get('device_id')
        else:
            device_id = request.data.get('device_id')
        
        if not device_id:
            self.message = "device_id is required. For GET requests, pass as query parameter. For POST requests, include in request body."
            return False
        
        # Check if mobile session exists and is active
        from apps.mobile_sessions.models import MobileSession
        
        try:
            session = MobileSession.objects.get(device_id=device_id, is_active=True)
            # Store session in request for use in views
            request.mobile_session = session
            return True
        except MobileSession.DoesNotExist:
            self.message = f"Mobile session not found or inactive for device_id: {device_id}. Please create a valid session first."
            return False


class CustomPagination(PageNumberPagination):
    """Custom pagination for mobile app optimization"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class FacilityListView(generics.ListAPIView):
    """
    List facilities with advanced filtering and search capabilities.
    Optimized for mobile app consumption with pagination and efficient queries.
    """
    serializer_class = FacilityListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['facility_name', 'registration_number', 'ward__ward_name', 
                     'ward__constituency__constituency_name', 'ward__constituency__county__county_name']
    ordering_fields = ['facility_name', 'ward__constituency__county__county_name', 'operational_status__status_name']
    ordering = ['facility_name']

    @swagger_auto_schema(
        operation_description="Get a paginated list of facilities with advanced filtering. Each facility includes lists of services and contacts.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search facilities by name, registration number, or location", type=openapi.TYPE_STRING),
            openapi.Parameter('county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('constituency', openapi.IN_QUERY, description="Filter by constituency ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ward', openapi.IN_QUERY, description="Filter by ward ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by operational status ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('service_category', openapi.IN_QUERY, description="Filter by service category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('has_coordinates', openapi.IN_QUERY, description="Filter facilities with GPS coordinates", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Items per page (max 100)", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: FacilityListSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Custom queryset with optimized database queries for mobile apps"""
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            Prefetch(
                'facilitycoordinate',
                queryset=FacilityCoordinate.objects.filter(),
                to_attr='active_coordinates'
            ),
            Prefetch(
                'facilityservice_set',
                queryset=FacilityService.objects.filter(is_active=True).select_related('service_category'),
                to_attr='active_services'
            ),
            Prefetch(
                'facilitycontact_set',
                queryset=FacilityContact.objects.filter(is_active=True).select_related('contact_type'),
                to_attr='active_contacts'
            )
        ).filter(is_active=True)

        # Apply custom filters
        county_id = self.request.query_params.get('county')
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)

        constituency_id = self.request.query_params.get('constituency')
        if constituency_id:
            queryset = queryset.filter(ward__constituency_id=constituency_id)

        ward_id = self.request.query_params.get('ward')
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)

        status_id = self.request.query_params.get('status')
        if status_id:
            queryset = queryset.filter(operational_status_id=status_id)

        service_category_id = self.request.query_params.get('service_category')
        if service_category_id:
            queryset = queryset.filter(facilityservice_set__service_category_id=service_category_id)

        has_coordinates = self.request.query_params.get('has_coordinates')
        if has_coordinates == 'true':
            queryset = queryset.filter(facilitycoordinate__latitude__isnull=False,
                                     facilitycoordinate__longitude__isnull=False)

        return queryset.distinct()


class FacilityDetailView(generics.RetrieveAPIView):
    """
    Get detailed information about a specific facility.
    Includes all related data optimized for mobile app consumption.
    """
    queryset = Facility.objects.select_related(
        'ward__constituency__county',
        'operational_status'
    ).prefetch_related(
        'facilitycontact_set__contact_type',
        'facilityservice_set__service_category',
        'facilityowner_set__owner_type',
        'facilitygbvcategory_set__gbv_category',
        'facilitycoordinate'
    ).filter(is_active=True)
    serializer_class = FacilityDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'facility_id'

    @swagger_auto_schema(
        operation_description="Get comprehensive details of a specific facility",
        responses={
            200: openapi.Response('Facility details', FacilityDetailSerializer),
            404: 'Facility not found',
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FacilityMapView(generics.ListAPIView):
    """
    Get facilities with coordinates for map display.
    Optimized for mobile app map views with minimal data transfer.
    """
    serializer_class = FacilityMapSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Get facilities with GPS coordinates for map display",
        manual_parameters=[
            openapi.Parameter('county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('constituency', openapi.IN_QUERY, description="Filter by constituency ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ward', openapi.IN_QUERY, description="Filter by ward ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by operational status ID", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: FacilityMapSerializer,
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Get only facilities with valid coordinates"""
        queryset = Facility.objects.select_related(
            'ward__constituency__county'
        ).prefetch_related(
            Prefetch(
                'facilitycoordinate',
                queryset=FacilityCoordinate.objects.filter(
                    latitude__isnull=False,
                    longitude__isnull=False
                ),
                to_attr='valid_coordinates'
            )
        ).filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False
        )

        # Apply filters
        county_id = self.request.query_params.get('county')
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)

        constituency_id = self.request.query_params.get('constituency')
        if constituency_id:
            queryset = queryset.filter(ward__constituency_id=constituency_id)

        ward_id = self.request.query_params.get('ward')
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)

        status_id = self.request.query_params.get('status')
        if status_id:
            queryset = queryset.filter(operational_status_id=status_id)

        return queryset.distinct()


class FacilitySearchView(generics.ListAPIView):
    """
    Advanced facility search with multiple filter options.
    Designed for mobile app search functionality with efficient querying.
    """
    serializer_class = FacilityListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Advanced facility search with multiple filters",
        request_body=FacilitySearchSerializer,
        responses={
            200: FacilityListSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        """Advanced search queryset with multiple filter combinations"""
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitycoordinate'
        ).filter(is_active=True)

        # Get search parameters
        search_query = self.request.data.get('search', '')
        county_id = self.request.data.get('county')
        constituency_id = self.request.data.get('constituency')
        ward_id = self.request.data.get('ward')
        status_id = self.request.data.get('status')
        service_category_id = self.request.data.get('service_category')
        has_coordinates = self.request.data.get('has_coordinates')

        # Apply search query
        if search_query:
            queryset = queryset.filter(
                Q(facility_name__icontains=search_query) |
                Q(registration_number__icontains=search_query) |
                Q(ward__ward_name__icontains=search_query) |
                Q(ward__constituency__constituency_name__icontains=search_query) |
                Q(ward__constituency__county__county_name__icontains=search_query)
            )

        # Apply filters
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)
        if constituency_id:
            queryset = queryset.filter(ward__constituency_id=constituency_id)
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        if status_id:
            queryset = queryset.filter(operational_status_id=status_id)
        if service_category_id:
            queryset = queryset.filter(facilityservice_set__service_category_id=service_category_id)
        if has_coordinates:
            queryset = queryset.filter(
                facilitycoordinate__latitude__isnull=False,
                facilitycoordinate__longitude__isnull=False
            )

        return queryset.distinct()


class StatisticsView(generics.GenericAPIView):
    """
    Get comprehensive statistics about facilities and geography.
    Useful for mobile app dashboards and analytics.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get comprehensive statistics about facilities and geography",
        responses={
            200: openapi.Response('Statistics data', StatisticsSerializer),
            401: 'Unauthorized',
        }
    )
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def get(self, request):
        """Get comprehensive statistics"""
        # Basic counts
        total_facilities = Facility.objects.filter(is_active=True).count()
        operational_facilities = Facility.objects.filter(
            is_active=True,
            operational_status__status_name='Operational'
        ).count()
        
        # Geography counts
        counties_count = County.objects.count()
        constituencies_count = Constituency.objects.count()
        wards_count = Ward.objects.count()
        
        # Facilities with coordinates
        facilities_with_coordinates = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False
        ).distinct().count()
        
        # Facilities by operational status
        facilities_by_status = Facility.objects.filter(
            is_active=True
        ).values('operational_status__status_name').annotate(
            count=Count('facility_id')
        ).order_by('-count')
        
        # Facilities by county
        facilities_by_county = Facility.objects.filter(
            is_active=True
        ).values(
            'ward__constituency__county__county_name'
        ).annotate(
            count=Count('facility_id')
        ).order_by('-count')[:10]  # Top 10 counties
        
        statistics = {
            'total_facilities': total_facilities,
            'operational_facilities': operational_facilities,
            'counties_count': counties_count,
            'constituencies_count': constituencies_count,
            'wards_count': wards_count,
            'facilities_with_coordinates': facilities_with_coordinates,
            'facilities_by_status': {item['operational_status__status_name']: item['count'] for item in facilities_by_status},
            'facilities_by_county': list(facilities_by_county)
        }
        
        serializer = StatisticsSerializer(statistics)
        return Response(serializer.data)


class LookupDataView(generics.GenericAPIView):
    """
    Get lookup data for dropdowns and filters.
    Essential for mobile app forms and filtering.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all lookup data for forms and filters",
        responses={
            200: LookupDataResponseSerializer,
            401: 'Unauthorized',
        }
    )
    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def get(self, request):
        """Get all lookup data"""
        lookup_data = {
            'counties': CountySerializer(County.objects.all().order_by('county_name'), many=True).data,
            'operational_statuses': OperationalStatusSerializer(OperationalStatus.objects.all().order_by('status_name'), many=True).data,
            'service_categories': ServiceCategorySerializer(ServiceCategory.objects.all().order_by('category_name'), many=True).data,
            'contact_types': ContactTypeSerializer(ContactType.objects.all().order_by('type_name'), many=True).data,
            'owner_types': OwnerTypeSerializer(OwnerType.objects.all().order_by('type_name'), many=True).data,
            'gbv_categories': GBVCategorySerializer(GBVCategory.objects.all().order_by('category_name'), many=True).data,
        }
        
        return Response(lookup_data)


class CountyListView(generics.ListAPIView):
    """Get list of counties"""
    queryset = County.objects.all().order_by('county_name')
    serializer_class = CountySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ConstituencyListView(generics.ListAPIView):
    """Get list of constituencies with county information"""
    queryset = Constituency.objects.select_related('county').all().order_by('constituency_name')
    serializer_class = ConstituencySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class WardListView(generics.ListAPIView):
    """Get list of wards with constituency and county information"""
    queryset = Ward.objects.select_related('constituency__county').all().order_by('ward_name')
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ConsolidatedGeographyView(generics.ListAPIView):
    """
    Consolidated geography endpoint that returns all counties with nested constituencies and wards.
    This provides a single API call to get the complete geographic hierarchy.
    """
    queryset = County.objects.prefetch_related(
        'constituency_set__ward_set'
    ).all().order_by('county_name')
    serializer_class = ConsolidatedGeographySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    @swagger_auto_schema(
        operation_description="Get complete geographic hierarchy including counties, constituencies, and wards in a single API call",
        responses={
            200: ConsolidatedGeographySerializer,
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_description="API status and health check",
    responses={
        200: openapi.Response('API status', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING),
                'version': openapi.Schema(type=openapi.TYPE_STRING),
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'timestamp': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """API status endpoint for health checks"""
    from django.utils import timezone
    return Response({
        "status": "active",
        "version": "v1.0.0",
        "message": "Hodi Admin API is running successfully",
        "timestamp": timezone.now().isoformat()
    })


@swagger_auto_schema(
    method='get',
    operation_description="Simple hello world endpoint for testing",
    responses={
        200: openapi.Response('Hello message', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    """Simple hello world API endpoint for testing"""
    return Response({"message": "Hello, Hodi Admin API!"})


class EmergencyServicesView(generics.GenericAPIView):
    """
    Emergency SOS services endpoint for finding nearest emergency facilities.
    Optimized for urgent situations with location-based search.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Find nearest emergency services for SOS situations",
        request_body=EmergencySearchSerializer,
        responses={
            200: FacilityListSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request):
        """Find emergency services based on location and urgency"""
        serializer = EmergencySearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        latitude = data['latitude']
        longitude = data['longitude']
        radius_km = data.get('radius_km', 10)
        service_types = data.get('service_types', ['Emergency Services', 'Security Services'])
        
        # Calculate distance and find nearby facilities
        from django.db.models import F, FloatField
        from django.db.models.functions import Power, Sqrt
        
        # Haversine formula approximation for distance calculation
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitycontact_set__contact_type'
        ).filter(
            is_active=True,
            operational_status__status_name='Operational',
            facilityservice_set__service_category__category_name__in=service_types,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False
        ).annotate(
            distance=Sqrt(
                Power(F('facilitycoordinate__latitude') - latitude, 2) +
                Power(F('facilitycoordinate__longitude') - longitude, 2),
                output_field=FloatField()
            ) * 111.32  # Approximate conversion to km
        ).filter(
            distance__lte=radius_km
        ).order_by('distance').distinct()[:10]  # Top 10 nearest
        
        serializer = FacilityListSerializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data,
            'emergency_contacts': {
                'police': '999',
                'ambulance': '999',
                'gbv_hotline': '116'
            }
        })


class GBVServicesView(generics.GenericAPIView):
    """
    GBV-specific service search endpoint for finding facilities
    that provide specific GBV response services.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Find facilities providing specific GBV services",
        request_body=GBVServiceSearchSerializer,
        responses={
            200: FacilityListSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request):
        """Find facilities offering specific GBV services"""
        serializer = GBVServiceSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        gbv_category = data['gbv_category']
        
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitygbvcategory_set__gbv_category'
        ).filter(
            is_active=True,
            operational_status__status_name='Operational',
            facilitygbvcategory_set__gbv_category__category_name__icontains=gbv_category
        )
        
        # Apply additional filters
        service_types = data.get('service_types', [])
        if service_types:
            queryset = queryset.filter(
                facilityservice_set__service_category__category_name__in=service_types
            )
        
        county_id = data.get('county')
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)
        
        constituency_id = data.get('constituency')
        if constituency_id:
            queryset = queryset.filter(ward__constituency_id=constituency_id)
        
        ward_id = data.get('ward')
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        
        queryset = queryset.distinct()
        serializer = FacilityListSerializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })


class ReferralChainView(generics.GenericAPIView):
    """
    Multi-service referral chain endpoint for getting recommended
    service pathways for GBV cases.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get recommended service pathway for GBV cases",
        request_body=ReferralChainSerializer,
        responses={
            200: openapi.Response('Referral chain recommendations', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'immediate_services': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    'followup_services': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    'recommended_order': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            401: openapi.Response('Unauthorized', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        }
    )
    def post(self, request):
        """Generate referral chain recommendations"""
        serializer = ReferralChainSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        case_type = data['case_type']
        location = data['location']
        immediate_needs = data['immediate_needs']
        followup_needs = data.get('followup_needs', [])
        
        # Build referral chain based on needs
        referral_chain = {
            'immediate_services': [],
            'followup_services': [],
            'recommended_order': []
        }
        
        # Find facilities for immediate needs
        for need in immediate_needs:
            facilities = Facility.objects.select_related(
                'ward__constituency__county'
            ).filter(
                is_active=True,
                operational_status__status_name='Operational',
                facilityservice_set__service_category__category_name__icontains=need
            )
            
            # Apply location filter
            if 'county' in location:
                facilities = facilities.filter(ward__constituency__county_id=location['county'])
            if 'ward' in location:
                facilities = facilities.filter(ward_id=location['ward'])
            
            facility_data = FacilityListSerializer(facilities[:5], many=True).data
            referral_chain['immediate_services'].append({
                'service_type': need,
                'facilities': facility_data
            })
        
        # Find facilities for follow-up needs
        for need in followup_needs:
            facilities = Facility.objects.select_related(
                'ward__constituency__county'
            ).filter(
                is_active=True,
                operational_status__status_name='Operational',
                facilityservice_set__service_category__category_name__icontains=need
            )
            
            if 'county' in location:
                facilities = facilities.filter(ward__constituency__county_id=location['county'])
            
            facility_data = FacilityListSerializer(facilities[:5], many=True).data
            referral_chain['followup_services'].append({
                'service_type': need,
                'facilities': facility_data
            })
        
        # Recommended order based on case type
        if 'Sexual Violence' in case_type:
            referral_chain['recommended_order'] = [
                'Medical Care (within 72 hours)',
                'Police Report',
                'Safe House (if needed)',
                'Counseling Services',
                'Legal Aid'
            ]
        elif 'Physical Violence' in case_type:
            referral_chain['recommended_order'] = [
                'Medical Care',
                'Police Report',
                'Safe House (if needed)',
                'Legal Aid',
                'Counseling Services'
            ]
        
        return Response(referral_chain)


class FacilityCompleteView(generics.RetrieveAPIView):
    """
    Get complete facility information with all related data
    in a single optimized request.
    """
    queryset = Facility.objects.select_related(
        'ward__constituency__county',
        'operational_status'
    ).prefetch_related(
        'facilitycontact_set__contact_type',
        'facilityservice_set__service_category',
        'facilityowner_set__owner_type',
        'facilitygbvcategory_set__gbv_category',
        'facilitycoordinate'
    ).filter(is_active=True)
    serializer_class = FacilityCompleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'facility_id'
    
    @swagger_auto_schema(
        operation_description="Get complete facility details with all related data",
        responses={
            200: openapi.Response('Complete facility details', FacilityCompleteSerializer),
            404: 'Facility not found',
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ContactInteractionAnalyticsView(generics.GenericAPIView):
    """
    Track contact interactions for analytics and referral effectiveness.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Track when users interact with a facility contact",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'contact_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Contact ID'),
                'is_helpful': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the contact was helpful'),
                'user_latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='User latitude'),
                'user_longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='User longitude'),
            },
            required=['contact_id']
        ),
        responses={
            201: openapi.Response('Contact interaction tracked successfully'),
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Contact not found',
        }
    )
    def post(self, request):
        """Track contact interaction for analytics"""
        try:
            contact_id = request.data.get('contact_id')
            if not contact_id:
                return Response({
                    'error': 'contact_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the contact
            contact = get_object_or_404(FacilityContact, contact_id=contact_id)
            
            # Get user from request - handle both session and token authentication
            user = None
            
            # For session-based authentication (web)
            if hasattr(request, 'session') and 'user_id' in request.session:
                try:
                    user = User.objects.get(user_id=request.session['user_id'], is_active=True)
                except User.DoesNotExist:
                    pass
            
            # For token-based authentication (API/mobile), try to get user from request
            elif hasattr(request, 'user') and hasattr(request.user, 'user_id'):
                user = request.user
            
            # If no user found, return error
            if not user:
                return Response({
                    'error': 'User authentication required for contact tracking',
                    'message': 'Please ensure you are properly authenticated'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create contact interaction record
            from django.utils import timezone
            
            interaction = ContactInteraction.objects.create(
                device_id=f"web_{user.user_id}_{int(timezone.now().timestamp())}",
                contact=contact,
                user_latitude=request.data.get('user_latitude'),
                user_longitude=request.data.get('user_longitude'),
                is_helpful=request.data.get('is_helpful'),
                created_at=timezone.now()
            )
            
            # Return success response with interaction details
            return Response({
                'message': 'Contact interaction tracked successfully',
                'interaction_id': interaction.interaction_id,
                'contact': {
                    'id': contact.contact_id,
                    'type': contact.contact_type.type_name if contact.contact_type else 'Unknown',
                    'value': contact.contact_value
                },
                'tracked_at': interaction.created_at.isoformat(),
                'helpful': interaction.is_helpful
            }, status=status.HTTP_201_CREATED)
            
        except FacilityContact.DoesNotExist:
            return Response({
                'error': 'Contact not found',
                'contact_id': contact_id
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': 'Failed to track contact click',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReferralOutcomeView(generics.GenericAPIView):
    """
    Track referral outcomes for inter-agency coordination effectiveness.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Track referral outcomes between facilities",
        request_body=ReferralOutcomeSerializer,
        responses={
            201: openapi.Response('Referral outcome tracked successfully'),
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request):
        """Track referral outcome"""
        serializer = ReferralOutcomeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Here you would save to ReferralOutcome model
        # For now, we'll just return success
        
        return Response({
            'message': 'Referral outcome tracked successfully',
            'from_facility': data['from_facility'],
            'to_facility': data['to_facility'],
            'success': data['service_accessed']
        }, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    operation_description="Obtain API token for authentication",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        },
        required=['email', 'password']
    ),
    responses={
        200: openapi.Response(
            'Token obtained successfully',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: 'Invalid credentials',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_api_token(request):
    """
    Custom token authentication endpoint for GVRC Admin API.
    Compatible with the custom User model.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Authenticate using custom User model
        user = User.objects.get(email=email, is_active=True)
        
        # Use Django's built-in password checking
        if user.check_password(password):
            # Get or create custom token for our User model
            token, created = CustomToken.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.user_id,
                'email': user.email,
                'full_name': user.full_name,
                'message': 'Token obtained successfully',
                'created': created,
                'token_created': token.created.isoformat()
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Authentication failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Mobile App Simplified Views
class MobileFacilitiesView(generics.ListAPIView):
    """
    Simplified facilities endpoint for mobile app with pagination.
    Returns all facility information in a single optimized request.
    """
    serializer_class = MobileAppFacilitySerializer
    permission_classes = [MobileSessionPermission]
    pagination_class = CustomPagination
    
    @swagger_auto_schema(
        operation_description="Get all facilities with complete information for mobile app using mobile session authentication",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Items per page (max 100)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by operational status ID", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: MobileAppFacilitySerializer,
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def get(self, request, *args, **kwargs):
        # Update mobile session activity
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Optimized queryset for mobile app"""
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilitycontact_set__contact_type',
            'facilityservice_set__service_category',
            'facilityowner_set__owner_type',
            'facilitygbvcategory_set__gbv_category',
            'facilitycoordinate',
            'facilityinfrastructure_set__infrastructure_type',
            'facilityinfrastructure_set__condition_status'
        ).filter(is_active=True)
        
        # Apply filters
        county_id = self.request.query_params.get('county')
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)
        
        status_id = self.request.query_params.get('status')
        if status_id:
            queryset = queryset.filter(operational_status_id=status_id)
        
        # Add proper ordering to avoid pagination warnings
        return queryset.order_by('facility_id').distinct()


class MobileFacilityDetailView(generics.RetrieveAPIView):
    """
    Mobile facility detail endpoint.
    Returns comprehensive facility information including all linked data like services, contacts, owners, GBV categories, and infrastructure.
    """
    serializer_class = MobileAppFacilitySerializer
    permission_classes = [MobileSessionPermission]
    lookup_field = 'facility_id'
    
    @swagger_auto_schema(
        operation_description="Get comprehensive facility details for mobile app using mobile session authentication",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response(
                'Facility details with all linked data', 
                MobileAppFacilitySerializer,
                examples={
                    "application/json": {
                        "facility_id": 1,
                        "facility_name": "Example Health Center",
                        "facility_code": "EHC001",
                        "registration_number": "REG123456",
                        "ward": {
                            "ward_id": 1,
                            "ward_name": "Example Ward",
                            "constituency": {
                                "constituency_id": 1,
                                "constituency_name": "Example Constituency",
                                "county": {
                                    "county_id": 1,
                                    "county_name": "Example County"
                                }
                            }
                        },
                        "operational_status": {
                            "operational_status_id": 1,
                            "status_name": "Operational"
                        },
                        "coordinates": {
                            "coordinate_id": 1,
                            "latitude": -1.123456,
                            "longitude": 36.789012,
                            "collection_date": "2024-01-01",
                            "data_source": "GPS",
                            "collection_method": "Manual",
                            "created_at": "2024-01-01T10:00:00Z",
                            "updated_at": "2024-01-01T10:00:00Z"
                        },
                        "contacts": [
                            {
                                "contact_id": 1,
                                "contact_type": {
                                    "contact_type_id": 1,
                                    "type_name": "Phone"
                                },
                                "contact_value": "+254700000000",
                                "contact_person_name": "John Doe",
                                "is_primary": True,
                                "is_active": True,
                                "created_at": "2024-01-01T10:00:00Z",
                                "updated_at": "2024-01-01T10:00:00Z"
                            }
                        ],
                        "services": [
                            {
                                "service_id": 1,
                                "service_name": "HIV Testing",
                                "service_category": {
                                    "service_category_id": 1,
                                    "category_name": "Health Services"
                                },
                                "service_description": "Free HIV testing and counseling",
                                "is_free": True,
                                "cost_range": "",
                                "currency": "KES",
                                "availability_hours": "8:00 AM - 5:00 PM",
                                "availability_days": "Monday to Friday",
                                "appointment_required": False,
                                "is_active": True,
                                "created_at": "2024-01-01T10:00:00Z",
                                "updated_at": "2024-01-01T10:00:00Z"
                            }
                        ],
                        "owners": [
                            {
                                "owner_id": 1,
                                "owner_name": "Ministry of Health",
                                "owner_type": {
                                    "owner_type_id": 1,
                                    "type_name": "Government"
                                },
                                "created_at": "2024-01-01T10:00:00Z",
                                "updated_at": "2024-01-01T10:00:00Z"
                            }
                        ],
                        "gbv_categories": [
                            {
                                "gbv_category": {
                                    "gbv_category_id": 1,
                                    "category_name": "Domestic Violence",
                                    "description": "Support for domestic violence cases"
                                },
                                "created_at": "2024-01-01T10:00:00Z"
                            }
                        ],
                        "infrastructure": [
                            {
                                "infrastructure_id": 1,
                                "infrastructure_type": {
                                    "type_id": 1,
                                    "type_name": "Consultation Room",
                                    "description": "Private room for patient consultations"
                                },
                                "condition_status": {
                                    "status_id": 1,
                                    "status_name": "Good",
                                    "description": "In good working condition"
                                },
                                "description": "Standard consultation room",
                                "capacity": 1,
                                "current_utilization": 1,
                                "is_available": True,
                                "created_at": "2024-01-01T10:00:00Z",
                                "updated_at": "2024-01-01T10:00:00Z"
                            }
                        ],
                        "address_line_1": "123 Health Street",
                        "address_line_2": "Building A",
                        "description": "Primary health center serving the community",
                        "website_url": "https://example.com",
                        "is_active": True,
                        "created_at": "2024-01-01T10:00:00Z",
                        "updated_at": "2024-01-01T10:00:00Z"
                    }
                }
            ),
            404: 'Facility not found',
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def get(self, request, *args, **kwargs):
        # Update mobile session activity
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Optimized queryset for mobile facility detail with all related data"""
        return Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilitycontact_set__contact_type',
            'facilityservice_set__service_category',
            'facilityowner_set__owner_type',
            'facilitygbvcategory_set__gbv_category',
            'facilitycoordinate',
            'facilityinfrastructure_set__infrastructure_type',
            'facilityinfrastructure_set__condition_status'
        ).filter(is_active=True)


class MobileEmergencySOSView(generics.GenericAPIView):
    """
    Emergency SOS endpoint for mobile app.
    Finds nearest emergency facilities based on mobile session location.
    """
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_description="Emergency SOS - Find nearest emergency facilities using mobile session location",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Device ID from mobile session'),
                'emergency_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of emergency (e.g., "Medical", "Security", "GBV")'),
                'radius_km': openapi.Schema(type=openapi.TYPE_NUMBER, description='Search radius in kilometers (optional, default: 5)'),
            },
            required=['device_id', 'emergency_type']
        ),
        responses={
            200: openapi.Response('Emergency facilities found', MobileAppFacilitySerializer),
            400: 'Bad Request - Missing device_id or emergency_type, or location not available in session',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def post(self, request):
        """Handle emergency SOS request"""

        
        # Check if device_id is provided
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({
                'error': 'device_id is required',
                'message': 'Please provide your device_id to identify your mobile session'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get data directly from request (no serializer validation needed)
        emergency_type = request.data.get('emergency_type')
        if not emergency_type:
            return Response({
                'error': 'emergency_type is required',
                'message': 'Please specify the type of emergency (e.g., "Medical", "Security", "GBV")'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        radius_km = request.data.get('radius_km', 5)
        
        # Get location from mobile session
        mobile_session = request.mobile_session
        latitude = mobile_session.latitude
        longitude = mobile_session.longitude
        
        if not latitude or not longitude:
            return Response({
                'error': 'Location not available in mobile session',
                'message': 'Please enable location services in your mobile app to use emergency SOS features. Your mobile session must have valid GPS coordinates stored.',
                'help': 'Update your mobile session with current location before using emergency SOS'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # radius_km and emergency_type already set above
        
        # Find facilities within radius (simplified distance calculation)
        from django.db.models import F, FloatField
        from django.db.models.functions import Power, Sqrt
        
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilitycontact_set__contact_type',
            'facilityservice_set__service_category',
            'facilityowner_set__owner_type',
            'facilitygbvcategory_set__gbv_category',
            'facilitycoordinate',
            'facilityinfrastructure_set__infrastructure_type',
            'facilityinfrastructure_set__condition_status'
        ).filter(
            is_active=True,
            operational_status__status_name='Operational',
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False
        ).annotate(
            distance=Sqrt(
                Power(F('facilitycoordinate__latitude') - latitude, 2) +
                Power(F('facilitycoordinate__longitude') - longitude, 2),
                output_field=FloatField()
            ) * 111.32  # Approximate conversion to km
        ).filter(
            distance__lte=radius_km
        ).order_by('distance')[:10]  # Top 10 nearest
        
        serializer = MobileAppFacilitySerializer(queryset, many=True)
        
        # Update mobile session activity
        mobile_session.update_activity()
        
        return Response({
            'emergency_type': emergency_type,
            'user_location': {'latitude': latitude, 'longitude': longitude},
            'search_radius_km': radius_km,
            'facilities_found': len(serializer.data),
            'facilities': serializer.data,
            'emergency_contacts': {
                'police': '999',
                'ambulance': '999',
                'gbv_hotline': '116',
                'fire_brigade': '999'
            },
            'session_info': {
                'device_id': mobile_session.device_id,
                'location_updated_at': mobile_session.location_updated_at.isoformat() if mobile_session.location_updated_at else None,
                'last_active': mobile_session.last_active_at.isoformat()
            },
            'message': f'Found {len(serializer.data)} emergency facilities within {radius_km}km'
        })


class MobileMusicView(generics.ListAPIView):
    """
    Music endpoint for mobile app with pagination.
    Returns all available music tracks.
    """
    serializer_class = MusicSerializer
    permission_classes = [MobileSessionPermission]
    pagination_class = CustomPagination
    
    @swagger_auto_schema(
        operation_description="Get all music tracks for mobile app using mobile session authentication",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Items per page (max 100)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING),
            openapi.Parameter('artist', openapi.IN_QUERY, description="Filter by artist", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response('Paginated music list', MusicSerializer),
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def get(self, request, *args, **kwargs):
        # Update mobile session activity
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Get music tracks with filters"""
        from apps.music.models import Music
        
        queryset = Music.objects.filter(is_active=True)
        
        # Apply filters
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        artist = self.request.query_params.get('artist')
        if artist:
            queryset = queryset.filter(artist__icontains=artist)
        
        # Add proper ordering to avoid pagination warnings
        return queryset.order_by('-created_at')


class MobileDocumentsView(generics.ListAPIView):
    """
    Documents endpoint for mobile app with pagination.
    Returns all available documents.
    """
    serializer_class = DocumentSerializer
    permission_classes = [MobileSessionPermission]
    pagination_class = CustomPagination
    
    @swagger_auto_schema(
        operation_description="Get all documents for mobile app using mobile session authentication",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Items per page (max 100)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('document_type', openapi.IN_QUERY, description="Filter by document type ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gbv_category', openapi.IN_QUERY, description="Filter by GBV category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_public', openapi.IN_QUERY, description="Filter public documents only", type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            200: openapi.Response('Paginated documents list', DocumentSerializer),
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def get(self, request, *args, **kwargs):
        # Update mobile session activity
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Get documents with filters"""
        from apps.documents.models import Document
        
        queryset = Document.objects.filter(is_active=True)
        
        # Apply filters
        document_type = self.request.query_params.get('document_type')
        if document_type:
            queryset = queryset.filter(document_type_id=document_type)
        
        gbv_category = self.request.query_params.get('gbv_category')
        if gbv_category:
            queryset = queryset.filter(gbv_category_id=gbv_category)
        
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        # Add proper ordering to avoid pagination warnings
        return queryset.order_by('-uploaded_at')


class MobileSessionView(generics.GenericAPIView):
    """
    Mobile session management endpoint.
    Create, retrieve, and update mobile device sessions.
    Anonymous access for mobile app session creation.
    """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Create a new mobile device session",
        request_body=MobileSessionCreateSerializer,
        responses={
            201: openapi.Response('Session created successfully', MobileSessionSerializer),
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request):
        """Create a new mobile session"""
        serializer = MobileSessionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Create new mobile session
        from apps.mobile_sessions.models import MobileSession
        
        session, created = MobileSession.objects.get_or_create(
            device_id=data['device_id'],
            defaults={
                'notification_enabled': data.get('notification_enabled', True),
                'dark_mode_enabled': data.get('dark_mode_enabled', False),
                'preferred_language': data.get('preferred_language', 'en-US'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'location_permission_granted': data.get('location_permission_granted', False),
                'is_active': True,
                'last_active_at': timezone.now()
            }
        )
        
        if not created:
            # Update existing session
            session.is_active = True
            session.last_active_at = timezone.now()
            session.save(update_fields=['is_active', 'last_active_at', 'updated_at'])
        
        serializer = MobileSessionSerializer(session)
        return Response({
            'message': 'Mobile session created/updated successfully',
            'session': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description="Get mobile session information",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device identifier", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response('Session information', MobileSessionSerializer),
            404: 'Session not found',
            401: 'Unauthorized',
        }
    )
    def get(self, request):
        """Get session information"""
        device_id = request.query_params.get('device_id')
        
        if not device_id:
            return Response({
                'error': 'device_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Query the MobileSession model
        from apps.mobile_sessions.models import MobileSession
        
        try:
            session = MobileSession.objects.get(device_id=device_id)
            serializer = MobileSessionSerializer(session)
            
            return Response({
                'session': serializer.data,
                'message': 'Session information retrieved successfully'
            })
            
        except MobileSession.DoesNotExist:
            return Response({
                'error': 'Session not found',
                'device_id': device_id
            }, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Update mobile session information",
        request_body=MobileSessionUpdateSerializer,
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device identifier", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response('Session updated successfully', MobileSessionSerializer),
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Session not found',
        }
    )
    def put(self, request):
        """Update session information"""
        device_id = request.query_params.get('device_id')
        
        if not device_id:
            return Response({
                'error': 'device_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MobileSessionUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the MobileSession model
        from apps.mobile_sessions.models import MobileSession
        
        try:
            session = MobileSession.objects.get(device_id=device_id)
            
            # Update fields
            for field, value in serializer.validated_data.items():
                if value is not None:
                    setattr(session, field, value)
            
            # Update location timestamp if coordinates changed
            if 'latitude' in serializer.validated_data or 'longitude' in serializer.validated_data:
                session.location_updated_at = timezone.now()
            
            session.last_active_at = timezone.now()
            session.updated_at = timezone.now()
            session.save()
            
            response_serializer = MobileSessionSerializer(session)
            return Response({
                'message': 'Mobile session updated successfully',
                'session': response_serializer.data
            })
            
        except MobileSession.DoesNotExist:
            return Response({
                'error': 'Session not found',
                'device_id': device_id
            }, status=status.HTTP_404_NOT_FOUND)


class MobileSessionEndView(generics.GenericAPIView):
    """
    Deactivate mobile session endpoint.
    """
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_description="Deactivate a mobile device session using mobile session authentication",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Device ID from mobile session'),
            },
            required=['device_id']
        ),
        responses={
            200: openapi.Response('Session deactivated successfully'),
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def post(self, request):
        """Deactivate a mobile session"""
        # Get mobile session from permission class
        mobile_session = request.mobile_session
        device_id = mobile_session.device_id
        
        # Update the MobileSession model
        from apps.mobile_sessions.models import MobileSession
        
        try:
            session = MobileSession.objects.get(device_id=device_id)
            
            # Deactivate session
            session.is_active = False
            session.updated_at = timezone.now()
            session.save(update_fields=['is_active', 'updated_at'])
            
            return Response({
                'message': 'Mobile session deactivated successfully',
                'device_id': session.device_id,
                'deactivated_at': session.updated_at.isoformat()
            })
            
        except MobileSession.DoesNotExist:
            return Response({
                'error': 'Session not found',
                'device_id': device_id
            }, status=status.HTTP_404_NOT_FOUND)


class MobileContactInteractionView(generics.GenericAPIView):
    """
    Mobile-optimized contact interaction tracking endpoint.
    Designed specifically for mobile app usage with mobile session authentication.
    """
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_description="Track contact interactions from mobile devices using mobile session authentication",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'contact_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Contact ID to track interaction with'),
                'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Device ID from mobile session (required for session validation)'),
                'is_helpful': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the contact was helpful (optional)'),
            },
            required=['contact_id', 'device_id']
        ),
        responses={
            201: openapi.Response('Contact interaction tracked successfully'),
            400: 'Bad Request - Missing contact_id or device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
            404: 'Contact not found',
        }
    )
    def post(self, request):
        """Track contact interaction from mobile device"""
        try:
            contact_id = request.data.get('contact_id')
            
            if not contact_id:
                return Response({
                    'error': 'contact_id is required',
                    'message': 'Please provide the contact_id of the facility contact you want to track'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate contact_id is a valid integer
            try:
                contact_id = int(contact_id)
            except (ValueError, TypeError):
                return Response({
                    'error': 'Invalid contact_id format',
                    'message': 'contact_id must be a valid integer',
                    'received_value': contact_id
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get mobile session data (already validated by permission class)
            mobile_session = request.mobile_session
            device_id = mobile_session.device_id
            
            # Get the contact
            contact = get_object_or_404(FacilityContact, contact_id=contact_id)
            
            # Get location from mobile session if not provided in request
            user_latitude = request.data.get('user_latitude') or mobile_session.latitude
            user_longitude = request.data.get('user_longitude') or mobile_session.longitude
            
            # Create contact interaction record with mobile session data
            interaction = ContactInteraction.objects.create(
                device_id=device_id,
                contact=contact,
                user_latitude=user_latitude,
                user_longitude=user_longitude,
                is_helpful=request.data.get('is_helpful'),
                created_at=timezone.now()
            )
            
            # Update mobile session activity
            mobile_session.update_activity()
            
            # Return success response optimized for mobile
            return Response({
                'success': True,
                'message': 'Contact interaction tracked successfully',
                'data': {
                    'interaction_id': interaction.interaction_id,
                    'contact': {
                        'id': contact.contact_id,
                        'type': contact.contact_type.type_name if contact.contact_type else 'Unknown',
                        'value': contact.contact_value
                    },
                    'tracked_at': interaction.created_at.isoformat(),
                    'helpful': interaction.is_helpful,
                    'device_id': device_id,
                    'session_info': {
                        'device_id': mobile_session.device_id,
                        'location': {
                            'latitude': mobile_session.latitude,
                            'longitude': mobile_session.longitude,
                            'updated_at': mobile_session.location_updated_at.isoformat() if mobile_session.location_updated_at else None
                        },
                        'last_active': mobile_session.last_active_at.isoformat()
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except FacilityContact.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Contact not found',
                'contact_id': contact_id
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'Failed to track contact interaction',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileLookupView(generics.GenericAPIView):
    """
    Mobile lookup data endpoint.
    Returns all essential lookup data for mobile app forms, filters, and dropdowns.
    Uses device_id authentication like other mobile endpoints.
    """
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_description="Get comprehensive lookup data for mobile app using mobile session authentication",
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response('Complete lookup data for mobile app', MobileLookupDataSerializer),
            400: 'Bad Request - Missing device_id',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def get(self, request):
        """Get all lookup data for mobile app"""
        try:
            # Update mobile session activity
            mobile_session = request.mobile_session
            mobile_session.update_activity()
            
            # Get all lookup data with optimized queries
            lookup_data = {
                # Geography
                'counties': CountySerializer(County.objects.all().order_by('county_name'), many=True).data,
                'constituencies': ConstituencySerializer(Constituency.objects.select_related('county').all().order_by('constituency_name'), many=True).data,
                'wards': WardSerializer(Ward.objects.select_related('constituency__county').all().order_by('ward_name'), many=True).data,
                
                # Facility-related lookups
                'operational_statuses': OperationalStatusSerializer(OperationalStatus.objects.all().order_by('sort_order', 'status_name'), many=True).data,
                'service_categories': ServiceCategorySerializer(ServiceCategory.objects.all().order_by('category_name'), many=True).data,
                'contact_types': ContactTypeSerializer(ContactType.objects.all().order_by('type_name'), many=True).data,
                'owner_types': OwnerTypeSerializer(OwnerType.objects.all().order_by('type_name'), many=True).data,
                'gbv_categories': GBVCategorySerializer(GBVCategory.objects.all().order_by('category_name'), many=True).data,
                
                # Infrastructure and equipment
                'infrastructure_types': InfrastructureTypeSerializer(InfrastructureType.objects.all().order_by('type_name'), many=True).data,
                'condition_statuses': ConditionStatusSerializer(ConditionStatus.objects.all().order_by('status_name'), many=True).data,
                
                # Document types
                'document_types': DocumentTypeSerializer(DocumentType.objects.all().order_by('type_name'), many=True).data,
                
                # Metadata
                'last_updated': timezone.now(),
                'total_lookup_items': 0,  # Will be calculated below
            }
            
            # Calculate total lookup items
            total_items = sum(len(data) for data in lookup_data.values() if isinstance(data, list))
            lookup_data['total_lookup_items'] = total_items
            
            return Response(lookup_data)
            
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve lookup data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameScoreUpdateView(generics.GenericAPIView):
    """
    Game score update endpoint for mobile app.
    Updates the high score for a mobile session if the new score is higher.
    """
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_description="Update game high score for mobile session",
        request_body=GameScoreUpdateSerializer,
        responses={
            200: openapi.Response('Game score updated successfully', GameScoreUpdateSerializer),
            400: 'Bad Request - Invalid score data',
            401: 'Unauthorized - Invalid or inactive mobile session',
        }
    )
    def post(self, request):
        """Update game high score for mobile session"""
        try:
            # Update mobile session activity
            mobile_session = request.mobile_session
            mobile_session.update_activity()
            
            # Get the new score from request data
            new_score = request.data.get('game_score', 0)
            game_name = request.data.get('game_name', 'Unknown Game')
            
            if new_score < 0:
                return Response({
                    'success': False,
                    'error': 'Game score cannot be negative',
                    'details': 'Score must be 0 or greater'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update the high score if the new score is higher
            score_updated = mobile_session.update_game_score(new_score)
            
            return Response({
                'success': True,
                'message': 'Game score updated successfully',
                'data': {
                    'device_id': mobile_session.device_id,
                    'game_name': game_name,
                    'new_score': new_score,
                    'high_score': mobile_session.game_high_score,
                    'score_updated': score_updated,
                    'session_info': {
                        'device_id': mobile_session.device_id,
                        'last_active': mobile_session.last_active_at.isoformat(),
                        'high_score': mobile_session.game_high_score
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'Failed to update game score',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)