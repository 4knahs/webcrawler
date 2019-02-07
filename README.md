# Web Crawler

Python app to crawl websites.

## Design decisions

I decided to implement a producer/consumer model:

* The producer has a task queue where only new urls are queued.
* Consumers fetch a task consisting of an url, and reply with a list of its inner urls.
* The producer is constantly waiting on new replies, it does not wait for all consumers to be done.
* When it receives a reply it filters known urls and adds the new ones to the task queue.
* The producer signals for the termination of all consumers when there are no more urls to process.

This system has a mix of cpu and i/o, for parsing pages and fetching urls.
While i/o bound systems tend to do ok with python "threads" (GIL), 
I decided to use processes for true parallelism.

For further optimizations one could profile the observed workload and task execution time
and potentially batch tasks to reduce inter-process communication and the queue lock acquisition time.

## Compatibility and dependencies

This project was tested with Python 3.5.

To install the dependencies:

```
pip install tldextract
pip install beautifulsoup4
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
usage: crawler.py [-h] [-w W] [-l] [-v] url

Crawls webpages for URLs

positional arguments:
  url         URL to crawl

optional arguments:
  -h, --help  show this help message and exit
  -w W        Number of processes (default: 2 * cpu_count())
  -l          If set crawls only domain specific URLs
  -v          Enable verbose
```

## Testing

This project includes a set of tests to validate potential URLs, check `test_crawler.py`
to get a feeling for the supported URL formats.

To run the tests:

```
python test_crawler.py
```