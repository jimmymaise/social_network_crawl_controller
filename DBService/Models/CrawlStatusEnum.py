
class CrawlStatusEnum(object):
    Created = 'Created'  # First created but not crawled
    Unselected = 'Unselected'  # Unselected items
    Selected = 'Selected'  # Selected to crawl
    Cached = 'Cached'  # Object are stored in cache
    Queuing = 'Queuing'  # Push to queue
    Crawling = 'Crawling'  # Object are crawling
    Analyzing = 'Analyzing'  # Object are analyzing
    Analyzed = 'Analyzed'  # Object are analyzed
    Crawled = 'Crawled'  # Finish crawled
    Pending = 'Pending'  # Crawling but force to stop
    Recrawl = 'Recrawl'  # Need to recrawl because the previous crawl is fail
    Error = 'Error'  # Error happened when crawling

