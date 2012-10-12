import urllib2
import unicodedata
import sys
import datetime
from xml.dom import minidom

DEBUG = False

cb_params = { #http://api.careerbuilder.com/JobSearchInfo.aspx
    'DeveloperKey' : 'WDHB2SG690RJMWRLR5KX',
    'Keywords'     : '', # single or comma-separated.
    'Location'     : 'Madison,WI',
    'Radius'       : '5', # in miles valid: '5, 10, 20, 30, 50, 100, or 150'
    'CountryCode'  : 'US',
    'Category'     : '', # Can accept a single value, or a comma-separated list of values. (Maximum 10)
    'PostedWithin' : '', # Must be one of: 1, 3, 7, or 30. If no value is provided, defaults to 30.
    'EmpType'      : '', 
    'PayLow'       : '75000',
    'PayHigh'      : '',
    'PageNumber'   : '1', # start with 1
    'PerPage'      : '50', # default: just looking for total results
    'OrderBy'      : '',
    'ExcludeNational': 'True',
    }

class JobPost:    
    def __init__ (self, x):
        self.title           = xml_tag_data(x, 'JobTitle')
        self.company         = xml_tag_data(x, 'Company')
        self.salary          = xml_tag_data(x, 'Pay')
        self.location        = xml_tag_data(x, 'Location')
        self.lat             = xml_tag_data(x, 'LocationLatitude')
        self.lon             = xml_tag_data(x, 'LocationLongitude')
        self.url             = xml_tag_data(x, 'JobDetailsURL')
        self.employment_type = xml_tag_data(x, 'EmploymentType')

        d = xml_tag_data(x, 'PostedDate')
        self.date_posted = datetime.datetime.strptime(d, '%m/%d/%Y').date()
        
    def gps (self):
        return {'lat' : lat, 'lon' : lon}

    def __repr__ (self):
        s  = 'Title   - %s\n' % self.title
        s += 'Company - %s\n' % self.company
        s += 'Salary  - %s\n' % self.salary
        s += 'Posted  - %s\n' % self.date_posted
        s += 'Age     - %s days\n' % self.age_days()

        return s.encode('utf-8')

    def age_days (self):
        d = datetime.datetime.today().date() - self.date_posted

        return d.days

def get_xml ():
    url  = make_url()
    html = urllib2.urlopen(url).read()
    xml  = minidom.parseString(html)

    return xml
    
def main (term='', get_jobs=False):
    print
    print 'Job search: "%s" within %s miles of %s' % (term,
                                                      cb_params['Radius'],
                                                      cb_params['Location'])
    print
                                                      
    # todo: set cb_params properly from more input args
    cb_params['Keywords'] = term
    job_dict = {}

    xml         = get_xml()
    total_jobs  = int(xml_tag_data(xml, 'TotalCount'))
    total_pages = int(xml_tag_data(xml, 'TotalPages'))

    print '! Found', total_jobs, 'matching results !\n'

    if get_jobs:
        page = 1

        while page <= total_pages:
            cb_params['PageNumber'] = str(page)
            page += 1

            xml = get_xml()
            xml_jobs = xml.getElementsByTagName("JobSearchResult")

            for j in xml_jobs:
                tmp = JobPost(j)
                if tmp.url in job_dict:
                    if DEBUG:
                        print ' WARNING: duplicate job found'
                        print ' URL:', tmp.url
                        raw_input('enter to continue\n')
                else:
                    if DEBUG:
                        print tmp.url
                    job_dict[tmp.url] = tmp

                if DEBUG:
                    print tmp
                    raw_input('enter to continue\n')
    
    res = {'total' : total_jobs,
           'jobs' : job_dict}

    #print res
    return res

def sort_by_company (din):
    # din  = dict of {URL KEY: job object, ...}
    # dnew = dict of {company : [list of (title, url) tuples, ...]}

    dnew = {}

    # company is lowercase!
    for url in din:
        company = din[url].company.lower()
        title   = din[url].title
        
        if company not in dnew:
            dnew[company] = []

        dnew[company].append((title, url))

    return dnew

def xml_tag_data (node, tag):
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
        if cb_params[i] != '':
            URL += '&%s=%s' % (i, cb_params[i])

    return URL

if __name__ == '__main__':
    l = len(sys.argv)

    if l > 1 and sys.argv[1].lower() == 'help':
        print 'This program searches Career Builder for the term "%s"' % cb_params['Keywords']
        print
        print 'Optional input arguments are:'
        print '  1: Search Term'
        print '  2: Non-zero to return actual job info.'
        print '     Zero will just return hit count (default).'
        exit(0)

    if   l == 1:
        main()
    elif l == 2:
        main(term=sys.argv[1], get_jobs=False)
    elif l == 3:
        search = True if sys.argv[2] else False
        main(term=sys.argv[1], get_jobs=search)
