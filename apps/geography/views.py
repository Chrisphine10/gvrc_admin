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

@login_required
def check_facility_connections(request):
    """Check if a geography item has facility connections"""
    try:
        item_type = request.GET.get('type')
        item_id = request.GET.get('id')
        
        if not item_type or not item_id:
            return JsonResponse({'success': False, 'error': 'Type and ID are required'}, status=400)
        
        has_facilities = False
        
        if item_type == 'county':
            county = County.objects.get(county_id=item_id)
            has_facilities = county.has_facilities()
        elif item_type == 'constituency':
            constituency = Constituency.objects.get(constituency_id=item_id)
            has_facilities = constituency.has_facilities()
        elif item_type == 'ward':
            ward = Ward.objects.get(ward_id=item_id)
            has_facilities = ward.has_facilities()
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
        
        return JsonResponse({
            'success': True,
            'has_facilities': has_facilities
        })
        
    except (County.DoesNotExist, Constituency.DoesNotExist, Ward.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@login_required
def edit_geography_item(request):
    """Edit an existing county, constituency, or ward"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')
        
        if not item_type or not item_id:
            return JsonResponse({'success': False, 'error': 'Type and ID are required'}, status=400)
        
        if item_type == 'county':
            try:
                county = County.objects.get(county_id=item_id)
                county_name = data.get('name', '').strip()
                county_code = data.get('code', '').strip()
                
                if not county_name or not county_code:
                    return JsonResponse({'success': False, 'error': 'Name and code are required'}, status=400)
                
                # Check if new name conflicts with existing counties (excluding current one)
                if County.objects.exclude(county_id=item_id).filter(county_name__iexact=county_name).exists():
                    return JsonResponse({'success': False, 'error': 'County with this name already exists'}, status=400)
                
                # Check if new code conflicts with existing counties (excluding current one)
                if County.objects.exclude(county_id=item_id).filter(county_code__iexact=county_code).exists():
                    return JsonResponse({'success': False, 'error': 'County with this code already exists'}, status=400)
                
                county.county_name = county_name
                county.county_code = county_code
                county.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'County "{county_name}" updated successfully',
                    'county': {
                        'id': county.county_id,
                        'name': county.county_name,
                        'code': county.county_code
                    }
                })
                
            except County.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'County not found'}, status=404)
                
        elif item_type == 'constituency':
            try:
                constituency = Constituency.objects.get(constituency_id=item_id)
                constituency_name = data.get('name', '').strip()
                constituency_code = data.get('code', '').strip()
                county_id = data.get('county_id')
                
                if not constituency_name or not constituency_code or not county_id:
                    return JsonResponse({'success': False, 'error': 'Name, code, and county are required'}, status=400)
                
                try:
                    county = County.objects.get(county_id=county_id)
                except County.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid county selected'}, status=400)
                
                # Check if new name conflicts with existing constituencies (excluding current one)
                if Constituency.objects.exclude(constituency_id=item_id).filter(constituency_name__iexact=constituency_name).exists():
                    return JsonResponse({'success': False, 'error': 'Constituency with this name already exists'}, status=400)
                
                # Check if new code conflicts with existing constituencies (excluding current one)
                if Constituency.objects.exclude(constituency_id=item_id).filter(constituency_code__iexact=constituency_code).exists():
                    return JsonResponse({'success': False, 'error': 'Constituency with this code already exists'}, status=400)
                
                constituency.constituency_name = constituency_name
                constituency.constituency_code = constituency_code
                constituency.county = county
                constituency.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Constituency "{constituency_name}" updated successfully',
                    'constituency': {
                        'id': constituency.constituency_id,
                        'name': constituency.constituency_name,
                        'code': constituency.constituency_code,
                        'county_name': county.county_name
                    }
                })
                
            except Constituency.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Constituency not found'}, status=404)
                
        elif item_type == 'ward':
            try:
                ward = Ward.objects.get(ward_id=item_id)
                ward_name = data.get('name', '').strip()
                ward_code = data.get('code', '').strip()
                constituency_id = data.get('constituency_id')
                
                if not ward_name or not ward_code or not constituency_id:
                    return JsonResponse({'success': False, 'error': 'Name, code, and constituency are required'}, status=400)
                
                try:
                    constituency = Constituency.objects.get(constituency_id=constituency_id)
                except Constituency.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid constituency selected'}, status=400)
                
                # Check if new name conflicts with existing wards (excluding current one)
                if Ward.objects.exclude(ward_id=item_id).filter(ward_name__iexact=ward_name).exists():
                    return JsonResponse({'success': False, 'error': 'Ward with this name already exists'}, status=400)
                
                # Check if new code conflicts with existing wards (excluding current one)
                if Ward.objects.exclude(ward_id=item_id).filter(ward_code__iexact=ward_code).exists():
                    return JsonResponse({'success': False, 'error': 'Ward with this code already exists'}, status=400)
                
                ward.ward_name = ward_name
                ward.ward_code = ward_code
                ward.constituency = constituency
                ward.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Ward "{ward_name}" updated successfully',
                    'ward': {
                        'id': ward.ward_id,
                        'name': ward.ward_name,
                        'code': ward.ward_code,
                        'constituency_name': constituency.constituency_name,
                        'county_name': constituency.county.county_name
                    }
                })
                
            except Ward.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Ward not found'}, status=404)
                
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@login_required
def delete_geography_item(request):
    """Delete a county, constituency, or ward"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')
        
        if not item_type or not item_id:
            return JsonResponse({'success': False, 'error': 'Type and ID are required'}, status=400)
        
        if item_type == 'county':
            try:
                county = County.objects.get(county_id=item_id)
                county_name = county.county_name
                
                # Check if county can be deleted using model method
                if not county.can_delete():
                    if county.has_facilities():
                        return JsonResponse({
                            'success': False, 
                            'error': f'Cannot delete county "{county_name}" because it has facilities. This item can only be edited.'
                        }, status=400)
                    else:
                        return JsonResponse({
                            'success': False, 
                            'error': f'Cannot delete county "{county_name}" because it has constituencies. Delete all constituencies first.'
                        }, status=400)
                
                county.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'County "{county_name}" deleted successfully'
                })
                
            except County.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'County not found'}, status=404)
                
        elif item_type == 'constituency':
            try:
                constituency = Constituency.objects.get(constituency_id=item_id)
                constituency_name = constituency.constituency_name
                
                # Check if constituency can be deleted using model method
                if not constituency.can_delete():
                    if constituency.has_facilities():
                        return JsonResponse({
                            'success': False, 
                            'error': f'Cannot delete constituency "{constituency_name}" because it has facilities. This item can only be edited.'
                        }, status=400)
                    else:
                        return JsonResponse({
                            'success': False, 
                            'error': f'Cannot delete constituency "{constituency_name}" because it has wards. Delete all wards first.'
                        }, status=400)
                
                constituency.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'Constituency "{constituency_name}" deleted successfully'
                })
                
            except Constituency.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Constituency not found'}, status=404)
                
        elif item_type == 'ward':
            try:
                ward = Ward.objects.get(ward_id=item_id)
                ward_name = ward.ward_name
                
                # Check if ward can be deleted using model method
                if not ward.can_delete():
                    return JsonResponse({
                        'success': False, 
                        'error': f'Cannot delete ward "{ward_name}" because it has facilities. This item can only be edited.'
                    }, status=400)
                
                ward.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'Ward "{ward_name}" deleted successfully'
                })
                
            except Ward.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Ward not found'}, status=404)
                
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def get_all_counties(request):
    """Get all counties for dropdown selection"""
    try:
        counties = County.objects.all().order_by('county_name').values('county_id', 'county_name')
        return JsonResponse({
            'success': True,
            'counties': list(counties)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_all_constituencies(request):
    """Get all constituencies for dropdown selection"""
    try:
        constituencies = Constituency.objects.select_related('county').all().order_by('constituency_name').values(
            'constituency_id', 'constituency_name', 'county__county_name'
        )
        return JsonResponse({
            'success': True,
            'constituencies': list(constituencies)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
