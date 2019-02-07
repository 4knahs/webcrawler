import multiprocessing
from consumer import Consumer
from crawler_task import CrawlerTask
from url import Url
from logger import warn, info, debug, error, set_verbose, logger_to_stdout, set_silent
import sys
import argparse
from robot import Robot
from time import sleep

site_tree = {}

# For long running crawls might be beneficial to store hashed values in terms of memory
def is_new_url(url):
    """Returns true if its a new URL.

    Keyword arguments:
    url -- the url to check for freshness
    """
    u = site_tree.get(url, None)

    if u == None:
        site_tree[url] = 1
        return True
    else:
        site_tree[url] += 1
        return False

def crawl(url, workers=None, limit_to_domain=True, robot=False, single=False):
    """Crawls a given url to determine its link tree.
    
    Keyword arguments:
    url -- the url to crawl
    workers -- the number of processes to spawn (default cpu_count() * 2)
    limit_to_domain -- if the crawler should be limited to the url domain (default True)
    """
    u = Url(url)
    domain = u.domain()

    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    if robot:
        rob = Robot(u.url())
        num_consumers = 1
    elif workers:
        num_consumers = workers
    else:
        num_consumers = multiprocessing.cpu_count() * 2
    
    debug('Creating {} consumers'.format(num_consumers))
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]

    for w in consumers:
        w.start()
    
    num_jobs = 1
    tasks.put(CrawlerTask(url))

    # Keeps executing while there are URLs to process
    while num_jobs > 0:

        debug("Number of jobs: {}".format(num_jobs))

        debug("Fetching results")

        result = results.get()

        debug("Got results")

        if limit_to_domain:
            # Filter urls based on domain (this could be merged to previous filter)
            domain_urls = list(filter(lambda x: x.domain() == domain, result['urls']))
        else:
            domain_urls = result['urls']

        # Filter urls based on freshness (i.e., do not parse repeated urls)
        new_urls = list(filter(lambda x: is_new_url(x.url()), domain_urls))

        # Print 
        [(lambda x: info("{} -> {}".format(result['parent'], x.url())))(r) for r in new_urls]

        debug("URL stats: Total {} Domain {} New {}".format(len(result['urls']), len(domain_urls), len(new_urls)))

        for r in new_urls:

            if robot and rob.should_block(r):
                info("Blocked access to {}".format(r.url()))
                continue 

            if not single:
                debug('Scheduling: {}'.format(r.url()))

                tasks.put(CrawlerTask(r.url()))
                
                if robot and rob.throttle_time():
                    info('Sleeping {} seconds'.format(rob.throttle_time()))
                    sleep(rob.throttle_time())

                num_jobs += 1

        num_jobs -= 1

        debug("Done scheduling")

    # This stops all the processes
    for i in range(num_consumers):
        tasks.put(None)

    # Waits for the correct killing of the processes
    tasks.join()

    debug("Done")

def main():
    # Handle command line inputs
    parser = argparse.ArgumentParser(description="Crawls webpages for URLs")
    parser.add_argument('-w', type=int, help='Number of processes (default: 2 * cpu_count()).')
    parser.add_argument('-l', dest='domain', action='store_true', help='If set crawls only domain specific URLs.')
    parser.add_argument('url', help='URL to crawl.')
    parser.add_argument('-v', help='Enable verbose.', dest='verbose', action='store_true')
    parser.add_argument('-r', help='Enable robots.txt url blocking and throttling. Superseedes -w and forces workers to 1.', dest='robot', action='store_true')
    parser.add_argument('-sd', help='Single depth url crawl.', dest='single', action='store_true')
    parser.add_argument('-s', help='Silent. Superseedes -v and disables logging.', dest='silent', action='store_true')
    parser.set_defaults(limit=False, robot=False, domain=False, single=False, silent=False)
    args = parser.parse_args()

    logger_to_stdout()

    if args.verbose:
        set_verbose()

    if args.silent:
        set_silent()

    if args.w:
        # TODO: do proper conversion check for the workers input
        crawl(args.url, workers=args.w, limit_to_domain=args.domain, robot=args.robot, single=args.single)
    else:
        crawl(args.url, limit_to_domain=args.domain, robot=args.robot, single=args.single)


if __name__ == '__main__':
    main()

            