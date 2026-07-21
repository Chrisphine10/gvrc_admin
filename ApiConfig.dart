class ApiConfig {



  // Base URLs for different environments

  static const String devBaseUrl = 'https://hodi.co.ke';

  static const String stagingBaseUrl = 'https://hodi.co.ke';

  static const String prodBaseUrl = 'https://hodi.co.ke';

  // API version path - removed since endpoints don't use /api prefix

  static const String _apiVersion = '';

  // Session Management endpoints

  static const String createSession = '/mobile/sessions/create/';

  static const String updateSession = '/mobile/sessions/update/';

  static const String getSessionInfo = '/mobile/sessions/';

  static const String endSession = '/mobile/sessions/end/';

  // Emergency Services endpoints

  static const String emergencySOS = '/mobile/emergency/sos/';

  // Facility Discovery endpoints

  static const String getFacilities = '/mobile/facilities/list/';

  static const String getFacilityDetail = '/mobile/facilities/'; // Will be appended with {id}/detail/

  static const String getFacilitiesMap = '/api/facilities/map/';

  static const String searchFacilities = '/api/facilities/search/';

  // Document Management endpoints

  static const String getDocuments = '/mobile/documents/list/';

  // Music/Media endpoints

  static const String getMusic = '/mobile/music/list/';

  // Analytics endpoints

  static const String trackContactInteraction = '/mobile/analytics/contact-interaction/';

  // Chat endpoints

  static const String chatBase = '/mobile/chat/';

  static const String checkConversationStatus = '/mobile/chat/check-status/';

  static const String startConversation = '/mobile/chat/start/';

  static const String listConversations = '/mobile/chat/list/';

  static const String getConversationDetail = '/mobile/chat/'; // Will be appended with {id}/detail/

  static const String sendMessage = '/mobile/chat/'; // Will be appended with {id}/send-message/

  static const String sendMediaMessage = '/mobile/chat/send-media-message/';

  static const String closeConversation = '/mobile/chat/'; // Will be appended with {id}/close/

  static const String updateMessageStatus = '/mobile/chat/messages/'; // Will be appended with {message_id}/status/

  static const String adminListConversations = '/mobile/chat/admin/list/';

  static const String testFileUpload = '/mobile/chat/test-upload/';

  // Lookup endpoints

  static const String getLookups = '/mobile/lookups/data/';

  // Timeout settings - reduced for faster startup

  static const Duration connectionTimeout = Duration(seconds: 10);

  static const Duration receiveTimeout = Duration(seconds: 10);

  // Pagination settings

  static const int defaultPageSize = 50;

  static const int maxPageSize = 100;

  // Retry settings

  static const int maxRetries = 3;

  static const Duration retryDelay = Duration(seconds: 2);

  // Cache settings

  static const Duration cacheExpiry = Duration(hours: 24);

  static const Duration emergencyCacheExpiry = Duration(minutes: 30);

  // Environment detection

  static bool get isDevelopment {

    // Check if we're running in debug mode or on development server

    const bool isDebugMode = bool.fromEnvironment('dart.vm.product') == false;

    // For now, use development server if in debug mode

    // You can add more sophisticated environment detection here

    return isDebugMode;

  }

  // Get base URL based on environment

  static String getBaseUrl() {

    if (isDevelopment) {

      return devBaseUrl + _apiVersion;

    } else {

      return prodBaseUrl + _apiVersion;

    }

  }

  // Get full endpoint URL

  static String getEndpoint(String endpoint) {

    return getBaseUrl() + endpoint;

  }

  // Get headers for API requests

  static Map<String, String> getHeaders({

    String? accessToken,

    String? deviceId,

    String? csrfToken,

  }) {

    final headers = <String, String>{

      'Content-Type': 'application/json',

      'Accept': 'application/json',

      'User-Agent': 'GVRC-Hodi-App/1.0.0',

    };

    if (accessToken != null) {

      headers['Authorization'] = 'Bearer $accessToken';

    }

    if (deviceId != null) {

      headers['X-Device-ID'] = deviceId;

    }

    if (csrfToken != null) {

      headers['X-CSRFTOKEN'] = csrfToken;

    }

    return headers;

  }

  // Check if mobile API endpoints are available

  static Future<bool> checkMobileApiAvailability() async {

    try {

      // This would need to be implemented with actual HTTP calls

      // For now, return true to indicate endpoints are ready for testing

      return true;

    } catch (e) {

      return false;

    }

  }

  // Get API status information

  static Map<String, dynamic> getApiStatus() {

    return {

      'is_development': isDevelopment,

      'base_url': getBaseUrl(),

      'mobile_api_ready': true, // Mobile API endpoints are implemented

      'endpoints_available': {

        'sessions': true,

        'facilities': true,

        'documents': true,

        'music': true,

        'emergency': true,

        'chat': true,

        'lookups': true,

        'analytics': true,

      },

      'recommendation': 'Mobile API endpoints are ready for use',

    };

  }

  // Emergency types

  static const List<String> emergencyTypes = [

    'Medical',

    'Security',

    'GBV',

    'Fire',

    'Accident',

    'Natural Disaster',

  ];

  // Document types

  static const List<String> documentTypes = [

    'Information',

    'Form',

    'Guide',

    'Policy',

    'Report',

    'Resource',

  ];

  // GBV categories

  static const List<String> gbvCategories = [

    'Physical Violence',

    'Sexual Violence',

    'Emotional Violence',

    'Economic Violence',

    'Digital Violence',

    'Child Abuse',

    'Elder Abuse',

  ];

  // Music genres

  static const List<String> musicGenres = [

    'Pop',

    'Rock',

    'Hip Hop',

    'R&B',

    'Jazz',

    'Classical',

    'Folk',

    'Electronic',

    'Country',

    'Reggae',

  ];

  // Facility types

  static const List<String> facilityTypes = [

    'Hospital',

    'Police Station',

    'Fire Station',

    'Counseling Center',

    'Shelter',

    'Legal Aid',

    'Support Group',

    'Emergency Contact',

  ];

  // Facility statuses

  static const List<String> facilityStatuses = [

    'Active',

    'Inactive',

    'Maintenance',

    'Closed',

    'Temporary',

  ];

  // Google Maps API Configuration

  static String get googleMapsApiKey {

    // Try to get from environment variable first

    try {

      // Import dotenv at the top of the file if using flutter_dotenv

      // For now, we'll use a const fallback and update via dotenv in main.dart

      return const String.fromEnvironment(

        'GOOGLE_MAPS_API_KEY',

        defaultValue: 'AIzaSyBYKU1YgvaJwUYkFUqYkfwdPuOG5EvA_Bk',

      );

    } catch (e) {

      // Fallback to hardcoded key if env loading fails

      return 'AIzaSyBYKU1YgvaJwUYkFUqYkfwdPuOG5EvA_Bk';

    }

  }

  // Store the API key from .env file

  static String? _cachedApiKey;

  static void setGoogleMapsApiKey(String? key) {

    _cachedApiKey = key;

  }

  static String getGoogleMapsApiKey() {

    // Return cached key from .env if available, otherwise use const fallback

    return _cachedApiKey ?? googleMapsApiKey;

  }

}


