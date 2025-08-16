# -*- encoding: utf-8 -*-
"""
API views for GVRC Admin - Mobile App Focused
"""

from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    ConstituencySerializer, WardSerializer, OperationalStatusSerializer,
    ServiceCategorySerializer, ContactTypeSerializer, OwnerTypeSerializer,
    GBVCategorySerializer, LookupDataResponseSerializer, EmergencySearchSerializer,
    GBVServiceSearchSerializer, ReferralChainSerializer, ContactClickSerializer,
    ReferralOutcomeSerializer, FacilityCompleteSerializer
)
from apps.facilities.models import (
    Facility, FacilityContact, FacilityService, 
    FacilityOwner, FacilityCoordinate, FacilityGBVCategory
)
from apps.authentication.models import ContactClick, User, UserSession, CustomToken
from apps.common.geography import County, Constituency, Ward
from apps.common.lookups import (
    OperationalStatus, ContactType, ServiceCategory, 
    OwnerType, GBVCategory
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import hashlib


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
        operation_description="Get a paginated list of facilities with advanced filtering",
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
            200: openapi.Response('List of facilities', FacilityListSerializer(many=True)),
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
                'facilitycoordinate_set',
                queryset=FacilityCoordinate.objects.filter(active_status=True),
                to_attr='active_coordinates'
            )
        ).filter(active_status=True)

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
            queryset = queryset.filter(facilitycoordinate_set__active_status=True,
                                     facilitycoordinate_set__latitude__isnull=False,
                                     facilitycoordinate_set__longitude__isnull=False)

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
        'facilitycoordinate_set'
    ).filter(active_status=True)
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
            200: openapi.Response('Facilities with coordinates', FacilityMapSerializer(many=True)),
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
                'facilitycoordinate_set',
                queryset=FacilityCoordinate.objects.filter(
                    active_status=True,
                    latitude__isnull=False,
                    longitude__isnull=False
                ),
                to_attr='valid_coordinates'
            )
        ).filter(
            active_status=True,
            facilitycoordinate_set__active_status=True,
            facilitycoordinate_set__latitude__isnull=False,
            facilitycoordinate_set__longitude__isnull=False
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
            200: openapi.Response('Search results', FacilityListSerializer(many=True)),
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
            'facilitycoordinate_set'
        ).filter(active_status=True)

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
                facilitycoordinate_set__active_status=True,
                facilitycoordinate_set__latitude__isnull=False,
                facilitycoordinate_set__longitude__isnull=False
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
        total_facilities = Facility.objects.filter(active_status=True).count()
        operational_facilities = Facility.objects.filter(
            active_status=True,
            operational_status__status_name='Operational'
        ).count()
        
        # Geography counts
        counties_count = County.objects.count()
        constituencies_count = Constituency.objects.count()
        wards_count = Ward.objects.count()
        
        # Facilities with coordinates
        facilities_with_coordinates = Facility.objects.filter(
            active_status=True,
            facilitycoordinate_set__active_status=True,
            facilitycoordinate_set__latitude__isnull=False,
            facilitycoordinate_set__longitude__isnull=False
        ).distinct().count()
        
        # Facilities by operational status
        facilities_by_status = Facility.objects.filter(
            active_status=True
        ).values('operational_status__status_name').annotate(
            count=Count('facility_id')
        ).order_by('-count')
        
        # Facilities by county
        facilities_by_county = Facility.objects.filter(
            active_status=True
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
        "message": "GVRC Admin API is running successfully",
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
    return Response({"message": "Hello, GVRC Admin API!"})


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
            200: openapi.Response('Emergency services found', FacilityListSerializer(many=True)),
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
            active_status=True,
            operational_status__status_name='Operational',
            facilityservice_set__service_category__category_name__in=service_types,
            facilitycoordinate_set__active_status=True,
            facilitycoordinate_set__latitude__isnull=False,
            facilitycoordinate_set__longitude__isnull=False
        ).annotate(
            distance=Sqrt(
                Power(F('facilitycoordinate_set__latitude') - latitude, 2) +
                Power(F('facilitycoordinate_set__longitude') - longitude, 2)
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
            200: openapi.Response('GBV services found', FacilityListSerializer(many=True)),
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
            active_status=True,
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
            200: openapi.Response('Referral chain recommendations'),
            400: 'Bad Request',
            401: 'Unauthorized',
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
                active_status=True,
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
                active_status=True,
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
        'facilitycoordinate_set'
    ).filter(active_status=True)
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


class ContactClickAnalyticsView(generics.GenericAPIView):
    """
    Track contact clicks for analytics and referral effectiveness.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Track when users contact a facility",
        request_body=ContactClickSerializer,
        responses={
            201: openapi.Response('Contact click tracked successfully'),
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Facility or Contact not found',
        }
    )
    def post(self, request):
        """Track contact click for analytics"""
        serializer = ContactClickSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            # Get the facility and contact
            facility = get_object_or_404(Facility, facility_id=data['facility_id'])
            contact = get_object_or_404(FacilityContact, contact_id=data['contact_id'])
            
            # Get user from request - handle both session and token authentication
            user = None
            session = None
            
            # For session-based authentication (web)
            if hasattr(request, 'session') and 'user_id' in request.session:
                try:
                    user = User.objects.get(user_id=request.session['user_id'], is_active=True)
                    session_id = request.session.get('session_id')
                    if session_id:
                        session = UserSession.objects.filter(session_id=session_id).first()
                except User.DoesNotExist:
                    pass
            
            # For token-based authentication (API/mobile), try to get user from request
            elif hasattr(request, 'user') and hasattr(request.user, 'user_id'):
                user = request.user
                # Try to get the most recent session for this user
                session = UserSession.objects.filter(user=user).order_by('-created_at').first()
            
            # If no user found, create anonymous tracking record
            if not user:
                return Response({
                    'error': 'User authentication required for contact tracking',
                    'message': 'Please ensure you are properly authenticated'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create contact click record
            from django.utils import timezone
            contact_click = ContactClick.objects.create(
                user=user,
                session=session,
                facility=facility,
                contact=contact,
                clicked_at=timezone.now(),
                helpful=data.get('helpful', True)
            )
            
            # Return success response with click details
            return Response({
                'message': 'Contact click tracked successfully',
                'click_id': contact_click.click_id,
                'facility': {
                    'id': facility.facility_id,
                    'name': facility.facility_name
                },
                'contact': {
                    'id': contact.contact_id,
                    'type': contact.contact_type.type_name if contact.contact_type else 'Unknown',
                    'value': contact.contact_value
                },
                'tracked_at': contact_click.clicked_at.isoformat(),
                'helpful': contact_click.helpful
            }, status=status.HTTP_201_CREATED)
            
        except Facility.DoesNotExist:
            return Response({
                'error': 'Facility not found',
                'facility_id': data['facility_id']
            }, status=status.HTTP_404_NOT_FOUND)
            
        except FacilityContact.DoesNotExist:
            return Response({
                'error': 'Contact not found',
                'contact_id': data['contact_id']
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
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user.password_hash == password_hash:
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