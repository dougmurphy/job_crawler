import urllib2
import unicodedata
from xml.dom import minidom

class JobPost:
    title = ''
    company = ''
    salary = -1 # should be integer
    location = ''
    lat    = ''
    lon    = ''
    url    = ''
    data_posted = '' # should be a datetime object
    
    def __init__ (self):
        pass

    def gps (self):
        return {'lat' : lat, 'lon' : lon}
    
    

cb_params = { #http://api.careerbuilder.com/JobSearchInfo.aspx
    'DeveloperKey' : 'WDHB2SG690RJMWRLR5KX',
    'Keywords'     : '', # single or comma-separated.
    'Location'     : 'Madison,WI',
    'Radius'       : '10', # in miles
    'CountryCode'  : 'US',
    'Category'     : '', # Can accept a single value, or a comma-separated list of values. (Maximum 10)
    'PostedWithin' : '', # Must be one of: 1, 3, 7, or 30. If no value is provided, defaults to 30.
    'EmpType'      : '', 
    'PayLow'       : '75000',
    'PayHigh'      : '',
    'PageNumber'   : '1', # start with 1
    'PerPage'      : '50', 
    'OrderBy'      : ''
    }

def main ():
    URL         = make_url()
    h           = urllib2.urlopen(URL).read()
    x           = minidom.parseString(h)
    total, data = data_from_xml(x)

    print 'URL =', URL
    print 'Total results =', total, '\n'*2

    list_jobs(data)
    print map_from_gps(data)

def data_from_xml (x):
    # 'company' = {'jobs' : [list of jobs],
    #              'lat'  : latitude_string,
    #              'lon'  : longitude_string,
    #              }
    # http://www.blog.pythonlibrary.org/2010/11/12/python-parsing-xml-with-minidom/
    total       = node_text(x, 'TotalCount')
    total_pages = node_text(x, 'TotalPages')
    jobs        = x.getElementsByTagName("JobSearchResult")

    results = {} 

    for job in jobs:
        company   = node_text(job, 'Company')
        job_title = node_text(job, 'JobTitle')
        lat       = node_text(job, 'LocationLatitude')
        lon       = node_text(job, 'LocationLongitude')

        if company not in results:
            results[company] = {}
            results[company]['jobs'] = [] # create empty jobs list

        results[company]['jobs'].append(job_title)
        results[company]['lat'] = lat
        results[company]['lon'] = lon

    return total, results


def node_text (node, tag):
    # input node should have a child with 'tag'.
    # return results

    children = node.getElementsByTagName(tag)[0].childNodes
    results = []
    
    for child in children:
        if child.nodeType == child.TEXT_NODE:
            results.append(child.data)

    if len(results) != 1:
        print 'WARNING: node_text() found', len(results),
        print 'with TagName =', tag, '(expected 1)'
        return 'UNKNOWN'

#    return unicodedata.normalize('NFKD', results[0]).encode('ascii','ignore')
    return results[0]

                
def make_url ():
    URL = 'http://api.careerbuilder.com/v1/jobsearch?'

    for i in cb_params.keys():
        URL += '&%s=%s' % (i, cb_params[i])

    return URL

def list_jobs (data):
    num = 1

    for k in data.keys():
        print k
        for i in data[k]['jobs']:
            print ''*5, num, ':',
            print i
            num += 1
        print

def map_from_gps (gps):
    URL = 'http://maps.googleapis.com/maps/api/staticmap?&size=1000x1000&sensor=false'

    for i in gps.values():
        if i['lat'] == '0' or i['lon'] == 0:
            continue
        URL += '&markers=%s,%s' % (i['lat'], i['lon'])

    return URL

main()




