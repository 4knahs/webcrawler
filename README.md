# Web Crawler

Python app to crawl websites.

## Design decisions

I decided to implement a producer/consumer model:

* The producer has a task queue where only new urls are queued.
* Consumers fetch a task consisting of an url, and replies with a list of its inner urls.
* The producer is constantly waiting on new replies, it does not wait for all consumers to be done.
* When it receives a reply it filters known urls and adds the new ones to the task queue.
* The producer signals for the termination of all consumers when there are no more urls to process.

This system has a mix of cpu and i/o, for parsing pages and fetching urls.
While i/o bound systems tend to do ok with python "threads" (GIL), 
I decided to use processes for true parallelism.

For further optimizations one could profile the observed workload and task execution time
and potentially batch tasks to reduce inter-process communication and the queue lock acquisition time.
Note that for a highly scalable system you would likely need to reduce synchronization, e.g., by implement bloom filters to detect already visited pages.

## Compatibility and dependencies

This project was tested with Python 3.5.

To install the dependencies:

```bash
pip install tldextract # proper url suffix handling
pip install beautifulsoup4 # xml/html parsing
pip install robotexclusionrulesparser # Proper robot.txt support
```

## How to run

The standard way to execute is to call:

```
python crawler.py -l <url>
```

By default the crawler will launch twice as many processes as your CPU count.
If you want a different CPU count you can change it using the `-w` option.
For limiting the crawl domain to the domain of the provided URL use the `-l` option.

For further commands check the `--help` option:

```
$ python3 crawler.py -h
usage: crawler.py [-h] [-w W] [-l] [-v] [-r] [-sd] [-s] url

Crawls webpages for URLs

positional arguments:
  url         URL to crawl

optional arguments:
  -h, --help  show this help message and exit.
  -w W        Number of processes (default: 2 * cpu_count()).
  -l          If set crawls only domain specific URLs.
  -v          Enable verbose.
  -r          Enable robots.txt url blocking and throttling. Superseedes -w.
              and forces workers to 1.
  -sd         Single depth url crawl.
  -s          Silent. Superseedes -v and disables logging.
```

## Respecting robots.txt

To execute with `robots.txt` support use the `-r` parameter. Note that for now this forces
single process processing to account for `robots.txt` based throttling.

E.g., how to run with `robots.txt` support:

```
python crawler.py <url> -r
```

Additionally, to allow only one depth of url crawling and print only the `robot.txt` allowed new urls:

```
python crawler.py <url> -r -sd -s
```

## Testing

This project includes a set of tests to validate potential URLs, check `test_crawler.py`
to get a feeling for the supported URL formats.

To run the tests:

```
python test_crawler.py
```

## Happy crawling

![The crawler](https://media.giphy.com/media/8TweT7thDuT6ybPL9L/giphy.gif "The crawler")
