# 🎯 Intelligent Data Scraper Design

## Overview
Based on the analysis of all data files, here's the tailored design for the intelligent data scraper to extract data from various sources in the GBV project.

## File Processing Strategy

### 1. **Excel Files** (High Priority - Easy Processing)

#### A. FGM Resources Materials.xlsx
- **Processing Method**: Direct pandas DataFrame processing
- **Extraction Logic**: 
  - Read all columns as-is
  - Clean empty/null values
  - Map to Document model fields
- **Output**: Document records with metadata

#### B. NAIROBI LIST OF POLICE STATIONS.xlsx
- **Processing Method**: Direct pandas DataFrame processing
- **Extraction Logic**:
  - Map columns: NAIROBI → facility_name, Unnamed: 1 → phone, Unnamed: 2 → sub_county
  - Extract phone numbers from station names if needed
  - Create Facility records with FacilityContact
- **Output**: Facility records with contacts

#### C. GBV SDTATION PILOT.xlsx (Complex)
- **Processing Method**: Multi-pass parsing with region detection
- **Extraction Logic**:
  1. **Region Detection**: Find rows containing "REGION" to identify sections
  2. **Header Detection**: Find rows with "COUNTY", "SUB-COUNTY", "POLICE STATION", "POLICE POST"
  3. **Data Extraction**: Parse each region's data section
  4. **Phone Number Extraction**: Use regex to extract phone numbers from station names
  5. **Geographic Mapping**: Map counties and sub-counties to Ward/Constituency/County models
- **Output**: Facility records (stations and posts) with geographic and contact data

### 2. **DOCX File** (Medium Priority - Text Parsing)

#### GBV Support Organizations.docx
- **Processing Method**: Paragraph-based text parsing with pattern recognition
- **Extraction Logic**:
  1. **Organization Detection**: Find paragraphs starting with numbers (1., 2., etc.)
  2. **Service Extraction**: Look for "Services:" patterns
  3. **Contact Extraction**: Use regex for phone numbers and email addresses
  4. **Coverage Extraction**: Look for "Coverage:" patterns
  5. **Website Extraction**: Look for "https://" patterns
- **Output**: Facility records representing organizations with services and contacts

### 3. **PDF Files** (High Priority - Structured Data)

#### A. KMPDC Licensed Facilities PDFs
- **Processing Method**: PDF table extraction with PyPDF2/pdfplumber
- **Extraction Logic**:
  1. **Table Detection**: Identify table boundaries
  2. **Column Mapping**: Map to Facility model fields
  3. **Address Parsing**: Extract P.O Box, location details
  4. **Level Mapping**: Map facility levels to appropriate categories
- **Output**: Facility records with licensing information

#### B. National Shelters Network PDF
- **Processing Method**: PDF table extraction
- **Extraction Logic**:
  1. **Table Extraction**: Extract structured table data
  2. **Contact Parsing**: Separate phone numbers and emails
  3. **Geographic Mapping**: Map counties to Ward/Constituency/County
- **Output**: Facility records representing shelters

## Data Processing Pipeline

```
Raw Files → File Type Detection → Parser Selection → Data Extraction → Data Cleaning → Model Mapping → Database Storage
```

### 1. **File Type Detection**
```python
def detect_file_type(file_path):
    if file_path.endswith('.xlsx'):
        return 'excel'
    elif file_path.endswith('.pdf'):
        return 'pdf'
    elif file_path.endswith('.docx'):
        return 'docx'
```

### 2. **Parser Selection**
```python
def select_parser(file_type, file_name):
    if file_type == 'excel':
        if 'FGM' in file_name:
            return FGMResourcesParser()
        elif 'POLICE' in file_name:
            return PoliceStationsParser()
        elif 'GBV' in file_name:
            return GBVStationPilotParser()
    elif file_type == 'pdf':
        if 'KMPDC' in file_name:
            return KMPDCFacilitiesParser()
        elif 'Shelter' in file_name:
            return SheltersParser()
    elif file_type == 'docx':
        return GBVOrganizationsParser()
```

### 3. **Data Extraction Patterns**

#### Excel Patterns
- **Clean Data**: Direct column mapping
- **Complex Data**: Multi-pass parsing with pattern recognition
- **Phone Extraction**: Regex patterns for Kenyan phone numbers

#### PDF Patterns
- **Table Extraction**: Use pdfplumber for better table detection
- **Text Cleaning**: Remove extra whitespace and formatting
- **Column Alignment**: Handle misaligned columns

#### DOCX Patterns
- **Paragraph Parsing**: Process each paragraph for structured data
- **Pattern Matching**: Use regex for contact information
- **Service Mapping**: Map services to ServiceCategory model

## Error Handling & Data Quality

### 1. **Validation Rules**
- Required fields validation
- Phone number format validation
- Email format validation
- Geographic data validation

### 2. **Data Cleaning**
- Remove extra whitespace
- Standardize phone number formats
- Clean special characters
- Handle missing data gracefully

### 3. **Duplicate Detection**
- Check for existing facilities by name and location
- Merge duplicate records
- Update existing records with new information

## Implementation Priority

1. **Phase 1**: Excel files (FGM, Police Stations) - Easy wins
2. **Phase 2**: PDF files (KMPDC, Shelters) - Structured data
3. **Phase 3**: Complex Excel (GBV Station Pilot) - Requires parsing logic
4. **Phase 4**: DOCX file (Organizations) - Text parsing

## Expected Output

- **Facilities**: ~3,000+ healthcare facilities, ~100+ police stations, ~30+ shelters, ~20+ organizations
- **Documents**: ~15+ resource documents
- **Contacts**: Phone numbers and email addresses for facilities
- **Geographic Data**: Counties, constituencies, and wards
- **Services**: Mapped service categories for each facility type

This design ensures comprehensive data extraction while handling the unique challenges of each file format and data structure.

