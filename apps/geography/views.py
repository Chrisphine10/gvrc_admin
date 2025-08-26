from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import County, Constituency, Ward
import json

# Create your views here.

@login_required
def get_constituencies(request, county_id):
    """Get constituencies for a specific county"""
    try:
        constituencies = Constituency.objects.filter(
            county_id=county_id
        ).values('constituency_id', 'constituency_name', 'constituency_code')
        
        return JsonResponse({
            'success': True,
            'constituencies': list(constituencies)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_wards(request, constituency_id):
    """Get wards for a specific constituency"""
    try:
        wards = Ward.objects.filter(
            constituency_id=constituency_id
        ).values('ward_id', 'ward_name', 'ward_code')
        
        return JsonResponse({
            'success': True,
            'wards': list(wards)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def search_geography(request):
    """Search for counties, constituencies, or wards"""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'success': False, 'error': 'Query parameter required'}, status=400)
    
    try:
        results = {
            'counties': [],
            'constituencies': [],
            'wards': []
        }
        
        # Search counties
        counties = County.objects.filter(
            Q(county_name__icontains=query) | Q(county_code__icontains=query)
        )[:10]
        results['counties'] = [{'id': c.county_id, 'name': c.county_name, 'code': c.county_code} for c in counties]
        
        # Search constituencies
        constituencies = Constituency.objects.filter(
            Q(constituency_name__icontains=query) | Q(constituency_code__icontains=query)
        ).select_related('county')[:10]
        results['constituencies'] = [{
            'id': c.constituency_id, 
            'name': c.constituency_name, 
            'code': c.constituency_code,
            'county_name': c.county.county_name
        } for c in constituencies]
        
        # Search wards
        wards = Ward.objects.filter(
            Q(ward_name__icontains=query) | Q(ward_code__icontains=query)
        ).select_related('constituency__county')[:10]
        results['wards'] = [{
            'id': w.ward_id, 
            'name': w.ward_name, 
            'code': w.ward_code,
            'constituency_name': w.constituency.constituency_name,
            'county_name': w.constituency.county.county_name
        } for w in wards]
        
        return JsonResponse({
            'success': True,
            'results': results
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@login_required
def add_geography_item(request):
    """Add a new county, constituency, or ward"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        
        if item_type == 'county':
            county_name = data.get('name', '').strip()
            county_code = data.get('code', '').strip()
            
            if not county_name or not county_code:
                return JsonResponse({'success': False, 'error': 'Name and code are required'}, status=400)
            
            # Check if county already exists
            if County.objects.filter(county_name__iexact=county_name).exists():
                return JsonResponse({'success': False, 'error': 'County with this name already exists'}, status=400)
            
            if County.objects.filter(county_code__iexact=county_code).exists():
                return JsonResponse({'success': False, 'error': 'County with this code already exists'}, status=400)
            
            county = County.objects.create(
                county_name=county_name,
                county_code=county_code
            )
            
            return JsonResponse({
                'success': True,
                'message': f'County "{county_name}" added successfully',
                'county': {
                    'id': county.county_id,
                    'name': county.county_name,
                    'code': county.county_code
                }
            })
            
        elif item_type == 'constituency':
            constituency_name = data.get('name', '').strip()
            constituency_code = data.get('code', '').strip()
            county_id = data.get('county_id')
            
            if not constituency_name or not constituency_code or not county_id:
                return JsonResponse({'success': False, 'error': 'Name, code, and county are required'}, status=400)
            
            try:
                county = County.objects.get(county_id=county_id)
            except County.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid county selected'}, status=400)
            
            # Check if constituency already exists
            if Constituency.objects.filter(constituency_name__iexact=constituency_name).exists():
                return JsonResponse({'success': False, 'error': 'Constituency with this name already exists'}, status=400)
            
            if Constituency.objects.filter(constituency_code__iexact=constituency_code).exists():
                return JsonResponse({'success': False, 'error': 'Constituency with this code already exists'}, status=400)
            
            constituency = Constituency.objects.create(
                constituency_name=constituency_name,
                constituency_code=constituency_code,
                county=county
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Constituency "{constituency_name}" added successfully',
                'constituency': {
                    'id': constituency.constituency_id,
                    'name': constituency.constituency_name,
                    'code': constituency.constituency_code,
                    'county_name': county.county_name
                }
            })
            
        elif item_type == 'ward':
            ward_name = data.get('name', '').strip()
            ward_code = data.get('code', '').strip()
            constituency_id = data.get('constituency_id')
            
            if not ward_name or not ward_code or not constituency_id:
                return JsonResponse({'success': False, 'error': 'Name, code, and constituency are required'}, status=400)
            
            try:
                constituency = Constituency.objects.get(constituency_id=constituency_id)
            except Constituency.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid constituency selected'}, status=400)
            
            # Check if ward already exists
            if Ward.objects.filter(ward_name__iexact=ward_name).exists():
                return JsonResponse({'success': False, 'error': 'Ward with this name already exists'}, status=400)
            
            if Ward.objects.filter(ward_code__iexact=ward_code).exists():
                return JsonResponse({'success': False, 'error': 'Ward with this code already exists'}, status=400)
            
            ward = Ward.objects.create(
                ward_name=ward_name,
                ward_code=ward_code,
                constituency=constituency
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Ward "{ward_name}" added successfully',
                'ward': {
                    'id': ward.ward_id,
                    'name': ward.ward_name,
                    'code': ward.ward_code,
                    'constituency_name': constituency.constituency_name,
                    'county_name': constituency.county.county_name
                }
            })
            
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
