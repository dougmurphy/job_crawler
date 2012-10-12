#!/usr/bin/python
import urllib2
import string
import datetime

# todo: put salary limit on dice results
#       add more search websites

DEBUG = False
#DEBUG = True

comma = '%2C'

services = ['indeed',
            'dice',
            'monster',
            'careerbuilder',
            'simplyhired',
            #linkup.com
            ]

terms = ['software developer',
         'software',
         'hardware',
         'circuits',
         ]

# terms = ['engineering',
#          'engineer',
#          'software',
#          'hardware',
#          'computer science',
#          'computer engineer',
#          'controls engineer',
#          'electrical engineer',
#          'medical device',
#          'c programming',
#          'c++',
#          'electronics',
#          'analog circuits',
#          'digital circuits',
#          'circuits',
#          'embedded systems',
#          'microcontroller',
#          'dsp engineer',
#          'communications engineer',
#          'scripting',
#          'fpga',
#          'storage engineer',
#          'matlab',
#          'hardware engineer',
#          'java',
#          'c#',
#          'python',
#          'pcb design',
#          'unix',
#          'software engineer',
#          'software developer',
#          'systems engineer',
#          'web design',
#          'project manager',
#          'technical documentation',
#          'labview',
#          'rtos',
#          'i2c',
#          'spi',
#          'data visualization',
#          'bluetooth',
#          'zigbee',
#          'ruby',
#          'xml',
#          'database',
#          'analytics',
#          'soap',
#          'json',
#          'php',
#          '.net',
#          'ios',
#          'android',
#          'firmware',
#          'sql',
#          ]

def miles_to_km (mi):
    return 1.62*mi

radius = 5
salary = '75,000'

def quoteme (s):
    return ('"' + s + '"')

def makeurl (service, term, age=30):
    url = ''
    min = ''
    max = ''

    term = quoteme(term)

    if service not in services:
        print '-'*30
        print 'WEBSITE:', service, 'NOT SUPPORTED'
        exit(1)

    if service == 'dice':
        url = 'http://seeker.dice.com/jobsearch/servlet/JobSearch?op=300&N=0&Hf=0&NUM_PER_PAGE=30&Ntk=JobSearchRanking&Ntx=mode+matchall&AREA_CODES=&AC_COUNTRY=1525&QUICK=1&ZIPCODE=&RADIUS=%s&ZC_COUNTRY=0&COUNTRY=1525&STAT_PROV=0&METRO_AREA=33.78715899%s-84.39164034&TRAVEL=0&TAXTERM=0&SORTSPEC=0&FRMT=0&DAYSBACK=30&LOCATION_OPTION=2&FREE_TEXT=%s&WHERE=madison%s+wi' % ( str(miles_to_km(radius)), comma, urllib2.quote(term), comma)

        # we want to find a string of the form: "Search results 1 - X of Y</h2>", then get the number Y

        min = 'Search results:'
        max = '</h2>'

    if service == 'indeed':
        url  = 'http://www.indeed.com/jobs?q=%s+$%s&l=53715&radius=%s' % (urllib2.quote(term), salary, str(radius))
        min  = 'Jobs 1 to'
        max  = '</div>'

    if service == 'monster':
        url = 'http://jobsearch.monster.com/search/Wisconsin+Madison_12?q=%s&where=Madison__2c-WI&salmin=%s&saltyp=1&rad=%s' % (urllib2.quote(term).replace('%', '__'), salary.replace(',', ''), str(radius))
        min = '"description" content="'
        max = ' ' + term.replace('"', '&amp;quot;')

    if DEBUG:
        print 'URL:'   , url
        print 'MIN:'   , min
        print 'MAX:'   , max

        raw_input('press enter to continue')
        
    return (url, min, max)

def extract_results (url, min, max):
    response = urllib2.urlopen(url)
    html     = response.read()
    start    = html.lower().find(min.lower())
    offset   = start + len(min)
    end      = html.lower().find(max.lower(), offset)
    s        = html[offset:end] # s is of form described above

    if DEBUG:
        print 'URL:', url
        print 'START:', start
        print 'OFFSET:', offset
        print 'END:', end
#        print 'S:', s

        raw_input('press enter to print string')
        print s
        
    if start < 0 or end < 0:
        return 0
    elif ('Sorry, no jobs' in html) or ('did not match any jobs' in html):
        return 0
    else:
        return int(s.split(' ')[-1]) # note: could crash if not int...

##############################
# MAIN
##############################
def main ():
    hits = {}

    # hits should be a dictionary with key = service, value = list of (term, #) tuples

    for s in services:
        hits[s] = []

        print 'PROCESSING %s' % s

        for t in terms:
            print '  - %s ... ' % t,

            (url, min, max) = makeurl(s, t)
            val = extract_results(url, min, max)

            print val
            
            hits[s].append((t, val)) 

    print_results(hits)
    log_results(hits)

def print_results (hits):
    for k in hits.keys():
        string = '\n' + k
        print string

        vals_sorted = sorted(hits[k], key=lambda v: v[1], reverse=True)

        for v in vals_sorted:
            string = ' %s: %s' % (v[0], v[1])
            print string

def log_results (hits):
    fname = datetime.datetime.now().ctime() + '.txt'
    fname = fname.replace(' ', '')
    f     = open(fname, 'w')

    head_str = 'Searching radius=%s, and minimum salary=%s' % (str(radius), salary)
    f.write(head_str + '\n\n')

    s = 'ORDER: '
    for k in hits.keys():
        s += (k + ', ')

    f.write(s + '\n')

    for i in range(len(terms)):
        s = terms[i] + ','

        for k in hits.keys():
            s += str(hits[k][i][1]) + ','

        f.write(s + '\n')

    f.close()

if __name__ == '__main__':
    main()
        




