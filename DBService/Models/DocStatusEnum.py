
class DocStatusEnum(object):
    Created    = 'Created'     # First created but not crawled
    Cached     = 'Cached'      # Item is saved in cached
    Unselected = 'Unselected'  # Unselected items
    Selected   = 'Selected'    # Selected to crawl
    Queuing    = 'Queuing'     # Push to queue
    Crawling   = 'Crawling'    # Object are crawling
    Crawled    = 'Crawled'     # Finish crawled
    Pending    = 'Pending'     # Crawling but force to stop
    Recrawl    = 'Recrawl'     # Need to recrawl because the previous crawl is fail
    Error      = 'Error'       # Error happened when crawling
    Analyzing  = 'Analyzing'   # Object are analyzing
    Analyzed   = 'Analyzed'    # Object are analyzed
    Failed   = 'Failed'    # Object are analyzed
    Expired   = 'Expired'    # Object are analyzed

