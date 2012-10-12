# note: my publisher id is not valid yet...

indeed_params = { 'publisher' : '8192576990306980', # api id
                  'v'         : '2', # Version.
                  'format'    : '', # xml or json
                  'callback'  : '', # ?
                  'q'         : '', # Query. By default terms are ANDed.
                  'l'         : '', # Location. Use a postal code or a "city, state/province/region" combination.
                  'sort'      : '', #	Sort by relevance or date. Default is relevance.
                  'radius'    : '', # miles?
                  'st'        : '', # Site type. for job boards use 'jobsite'. for direct employer websites, use 'employer'.
                  'jt'        : '', # Job type. Allowed values: "fulltime", "parttime", "contract", "internship", "temporary".
                  'start'     : '', # start results at this result number, beginning with 0. Default is 0.
                  'limit'     : '', # Maximum number of results returned per query. Default is 10
                  'fromage'   : '', # Number of days back to search.
                  'highlight' : '', # 1 will bold terms
                  'filter'    : '', # filter duplicate results. 0 turns off duplicate job filtering. Default is 1.
                  'latlong'   : '', # If latlong=1, returns latitude and longitude information for each job result. Default is 0.
                  'co'        : '', # country
                  'chnl'      : '', # ?Channel Name: Group API requests to a specific channel
                  'userip'    : '', # The IP number of the end-user to whom the job results will be displayed. This field is required.
                  'useragent' : '', # required from HTTP
                  }
