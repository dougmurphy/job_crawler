import career_builder
import sys

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

d = career_builder.main(sys.argv[1], 1)['jobs']
d = sort_by_company(d)

for co in d:
    print
    print co.upper(), ':', len(co), 'jobs'

    for j in d[co]:
        print '  - ', j[0]
