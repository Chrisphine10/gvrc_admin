from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404

from .models import (
    User, Facility, FacilityContact, FacilityCoordinate,
    FacilityService, FacilityOwner, UserLocation, UserSession,
    County, Constituency, Ward, OperationalStatus, ContactType,
    ServiceCategory, OwnerType
)
from .serializers import (
    UserSerializer, FacilitySerializer, FacilityListSerializer,
    FacilityContactSerializer, FacilityCoordinateSerializer,
    FacilityServiceSerializer, FacilityOwnerSerializer,
    UserLocationSerializer, UserSessionSerializer,
    CountySerializer, ConstituencySerializer, WardSerializer,
    OperationalStatusSerializer, ContactTypeSerializer,
    ServiceCategorySerializer, OwnerTypeSerializer,
    LoginSerializer, UserRegistrationSerializer
)


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)


# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().select_related('facility').prefetch_related('locations__ward')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'facility', 'facility__ward']
    search_fields = ['full_name', 'email', 'phone_number']
    ordering_fields = ['full_name', 'created_at', 'updated_at']
    ordering = ['-created_at']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related('facility').prefetch_related('locations__ward')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


# Facility Views
class FacilityListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'operational_status', 'ward', 'ward__constituency', 
        'ward__constituency__county', 'active_status'
    ]
    search_fields = [
        'facility_name', 'registration_number', 
        'ward__ward_name', 'ward__constituency__constituency_name',
        'ward__constituency__county__county_name'
    ]
    ordering_fields = ['facility_name', 'created_at', 'updated_at']
    ordering = ['facility_name']
    
    def get_queryset(self):
        queryset = Facility.objects.select_related(
            'operational_status', 'ward', 'ward__constituency', 
            'ward__constituency__county', 'created_by', 'updated_by'
        ).prefetch_related(
            'contacts__contact_type',
            'coordinates',
            'services__service_category',
            'owners__owner_type',
            'users'
        )
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FacilityListSerializer
        return FacilitySerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'facility_id'
    
    def get_queryset(self):
        return Facility.objects.select_related(
            'operational_status', 'ward', 'ward__constituency', 
            'ward__constituency__county', 'created_by', 'updated_by'
        ).prefetch_related(
            'contacts__contact_type',
            'coordinates',
            'services__service_category',
            'owners__owner_type',
            'users'
        )
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FacilitySearchView(generics.ListAPIView):
    serializer_class = FacilityListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Facility.objects.select_related(
            'operational_status', 'ward', 'ward__constituency', 'ward__constituency__county'
        ).filter(active_status=True)
        
        # Get query parameters
        query = self.request.query_params.get('q', '')
        county = self.request.query_params.get('county', '')
        constituency = self.request.query_params.get('constituency', '')
        ward = self.request.query_params.get('ward', '')
        service_category = self.request.query_params.get('service_category', '')
        
        # Apply filters
        if query:
            queryset = queryset.filter(
                Q(facility_name__icontains=query) |
                Q(registration_number__icontains=query)
            )
        
        if county:
            queryset = queryset.filter(ward__constituency__county_id=county)
        
        if constituency:
            queryset = queryset.filter(ward__constituency_id=constituency)
        
        if ward:
            queryset = queryset.filter(ward_id=ward)
        
        if service_category:
            queryset = queryset.filter(services__service_category_id=service_category).distinct()
        
        return queryset


# Facility Related Views
class FacilityContactListCreateView(generics.ListCreateAPIView):
    serializer_class = FacilityContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        facility_id = self.kwargs.get('facility_id')
        return FacilityContact.objects.filter(
            facility_id=facility_id
        ).select_related('contact_type')


class FacilityContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityContact.objects.select_related('contact_type')
    serializer_class = FacilityContactSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'contact_id'


class FacilityCoordinateView(generics.RetrieveUpdateAPIView):
    serializer_class = FacilityCoordinateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        facility_id = self.kwargs.get('facility_id')
        facility = get_object_or_404(Facility, facility_id=facility_id)
        coordinate, created = FacilityCoordinate.objects.get_or_create(facility=facility)
        return coordinate


class FacilityServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = FacilityServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        facility_id = self.kwargs.get('facility_id')
        return FacilityService.objects.filter(
            facility_id=facility_id
        ).select_related('service_category')


class FacilityServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityService.objects.select_related('service_category')
    serializer_class = FacilityServiceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'service_id'


class FacilityOwnerListCreateView(generics.ListCreateAPIView):
    serializer_class = FacilityOwnerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        facility_id = self.kwargs.get('facility_id')
        return FacilityOwner.objects.filter(
            facility_id=facility_id
        ).select_related('owner_type')


class FacilityOwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityOwner.objects.select_related('owner_type')
    serializer_class = FacilityOwnerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'owner_id'


# Location Views
class CountyListView(generics.ListAPIView):
    queryset = County.objects.all().order_by('county_name')
    serializer_class = CountySerializer
    permission_classes = [IsAuthenticated]


class ConstituencyListView(generics.ListAPIView):
    serializer_class = ConstituencySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        county_id = self.request.query_params.get('county', None)
        queryset = Constituency.objects.select_related('county').order_by('constituency_name')
        
        if county_id:
            queryset = queryset.filter(county_id=county_id)
        
        return queryset


class WardListView(generics.ListAPIView):
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        constituency_id = self.request.query_params.get('constituency', None)
        county_id = self.request.query_params.get('county', None)
        queryset = Ward.objects.select_related(
            'constituency', 'constituency__county'
        ).order_by('ward_name')
        
        if constituency_id:
            queryset = queryset.filter(constituency_id=constituency_id)
        elif county_id:
            queryset = queryset.filter(constituency__county_id=county_id)
        
        return queryset


# Lookup Views
class OperationalStatusListView(generics.ListAPIView):
    queryset = OperationalStatus.objects.all().order_by('status_name')
    serializer_class = OperationalStatusSerializer
    permission_classes = [IsAuthenticated]


class ContactTypeListView(generics.ListAPIView):
    queryset = ContactType.objects.all().order_by('type_name')
    serializer_class = ContactTypeSerializer
    permission_classes = [IsAuthenticated]


class ServiceCategoryListView(generics.ListAPIView):
    queryset = ServiceCategory.objects.all().order_by('category_name')
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticated]


class OwnerTypeListView(generics.ListAPIView):
    queryset = OwnerType.objects.all().order_by('type_name')
    serializer_class = OwnerTypeSerializer
    permission_classes = [IsAuthenticated]


# User Location Views
class UserLocationListCreateView(generics.ListCreateAPIView):
    serializer_class = UserLocationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserLocation.objects.filter(
            user=self.request.user
        ).select_related('ward', 'ward__constituency', 'ward__constituency__county')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserLocationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'location_id'
    
    def get_queryset(self):
        return UserLocation.objects.filter(
            user=self.request.user
        ).select_related('ward', 'ward__constituency', 'ward__constituency__county')


# Session Views
class UserSessionListView(generics.ListAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


# Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    stats = {
        'total_facilities': Facility.objects.filter(active_status=True).count(),
        'total_users': User.objects.filter(is_active=True).count(),
        'facilities_by_county': list(
            Facility.objects.filter(active_status=True)
            .select_related('ward__constituency__county')
            .values('ward__constituency__county__county_name')
            .annotate(count=models.Count('facility_id'))
            .order_by('-count')[:10]
        ),
        'recent_facilities': FacilityListSerializer(
            Facility.objects.filter(active_status=True)
            .select_related('operational_status', 'ward__constituency__county')
            .order_by('-created_at')[:5],
            many=True
        ).data
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nearby_facilities(request):
    """Get facilities near user's location"""
    latitude = request.query_params.get('lat')
    longitude = request.query_params.get('lng')
    radius = float(request.query_params.get('radius', 10))  # Default 10km
    
    if not latitude or not longitude:
        return Response(
            {'error': 'Latitude and longitude are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Simple distance calculation (for more accurate results, consider using PostGIS)
    from django.db.models import F
    from decimal import Decimal
    
    lat = Decimal(latitude)
    lng = Decimal(longitude)
    
    facilities = Facility.objects.filter(
        active_status=True,
        coordinates__active_status=True,
        coordinates__latitude__isnull=False,
        coordinates__longitude__isnull=False
    ).select_related(
        'operational_status', 'ward__constituency__county', 'coordinates'
    ).prefetch_related(
        'contacts__contact_type', 'services__service_category'
    )
    
    # Filter by approximate distance (this is a simplified approach)
    # For production, consider using PostGIS or GeoDjango
    facilities = facilities.filter(
        coordinates__latitude__range=(lat - Decimal('0.1'), lat + Decimal('0.1')),
        coordinates__longitude__range=(lng - Decimal('0.1'), lng + Decimal('0.1'))
    )
    
    serializer = FacilitySerializer(facilities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)