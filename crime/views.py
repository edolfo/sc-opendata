# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
import xml.etree.ElementTree as ET
import re, datetime, logging, json
from crime.models import Crime
from django.core import serializers

log = logging.getLogger('django')

def index(request):
    title = "SC Open Data: Crime"
    #latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    #return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})
    
    crimeTypes = Crime.objects.values_list('CM_LEGEND', flat=True).distinct()
    
    return render_to_response('crime/base_index.html', {'title': title, 'crimeTypes':crimeTypes})
    
def getCrimeType(request, num):
    crimeTypes = Crime.objects.values_list('CM_LEGEND', flat=True).distinct()
    crimes = Crime.objects.filter(CM_LEGEND__exact=crimeTypes[int(num)-1])
    title = "SC Open Data: Crime"
    args = {'title': title, 'crimeTypes':crimeTypes, 'crimes':crimes, 'crimeTitle':crimes[0].CM_LEGEND, 'crimeNum':num}
    return render_to_response('crime/base_index.html', args)

def getCrimeDataJSON(request, num):
    crimeTypes = Crime.objects.values_list('CM_LEGEND', flat=True).distinct()
    crimes = Crime.objects.filter(CM_LEGEND__exact=crimeTypes[int(num)-1])
    zips = {}
    for crime in crimes:
        key = crime.Zip
        if key == '':
            key = 'No zip'
        if key not in zips.keys():
            zips[key] = 1
        else:
            zips[key] += 1
    #data = serializers.serialize("json", zips)
    data = json.dumps(zips)
    return HttpResponse(data, mimetype='application/json')

def getCrimeTypesJSON(request):
    data = {}
    crimeTypes = Crime.objects.values_list('CM_LEGEND', flat=True).distinct()
    zipsUnique = Crime.objects.values_list('Zip', flat=True).distinct()
    noZip = 'No zip'
    zipsUnique = [noZip if x == '' else x for x in zipsUnique]
    for cType in crimeTypes:
        zips = {}
        crimes = Crime.objects.filter(CM_LEGEND__exact=cType)
        for crime in crimes:
            key = crime.Zip
            if key == '':
                key = noZip
            if key not in zips:
                zips[key] = 1
            else:
                zips[key] += 1
        
        for z in zipsUnique:
            if z not in zips.keys():
                zips[z] = 0
        
        # Preserve order of zips and counts, but convert to lists for easier JSON access via dot syntax
        zipList = []
        countList = []
        for key in zips.keys():
            zipList.append(key)
            countList.append(zips[key])
        entry = {'zips':zipList, 'counts':countList} 
        data[cType] = entry
    log.info(data)
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')














"""
# Used to repopulate the DB

def reboot(request):
    # Should really be in admin stuff
    title = "SC Open Data: Crime (reboot)"
    return render_to_response('crime/base_reboot.html', {'title':title}, context_instance=RequestContext(request))
    
def rebootHandler(request):
    # Should really be in admin stuff
    try:
        passphrase = request.POST['passphrase']
        log.debug('Passphrase was %s' % passphrase)
    except Exception as e:
        title = "Error"
        error = e
        extra = request.POST
        return render_to_response('crime/base_error.html', {'title':title, 'error':error, 'extra':extra})
    
    if passphrase != 'Insert passphrase <here>!':
        title = "Error"
        return render_to_response('crime/base_error.html', {'title':title, 'error':'Shit you out of luck'})
    
    tree = ET.parse('pdexport.xml')
    root = tree.getroot()
    children = root.getchildren()
    fields = ['ObjectID', 'CaseNum', 'ID', 'CM_ID', 'CM_AGENCY', 'DateOccurred1',
    'TimeOccurred1', 'UcrCrime', 'UcrCrimeHierarchy', 'Description', 'UCR1', 
    'CM_LEGEND', 'StrNumber', 'Street', 'Zip', 'Intersection', 'CVADDRESS', 
    'BLOCK_ADDRESS', 'CVDATE', 'CVDOW', 'CVTIME','iwGeoName', 'iwStep', 'Status',
    'Score', 'X', 'Y', 'Stan_Addr', 'pointProperty', 'DomViolMeth', 'Side']
    
    for child in children:
        if 'featureMember' in child.tag:
            args = {}
            fields = child.getchildren()[0].getchildren()
            for field in fields:
                if 'DateOccurred1' in field.tag:
                    if field.text is not None:
                        args['DateOccurred1'] = datetime.datetime.strptime(field.text, '%Y-%m-%d %H:%M:%S')
                    else:
                        args['DateOccurred1'] = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                elif 'TimeOccurred1' in field.tag:
                    if field.text is not None:
                        args['TimeOccurred1'] = datetime.datetime.strptime(field.text, '%Y-%m-%d %H:%M:%S')
                    else:
                        args['TimeOccurred1'] = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
                elif 'ID' in field.tag:
                    continue
                else:
                    key = re.sub('{.*}', '', field.tag)
                    args[key] = field.text
            c = Crime(**args)
            c.save()
    title = 'Reboot success'
    return render_to_response('crime/base_reboot-success.html', {'title':title})
"""
