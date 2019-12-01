import argparse
from scrapy.crawler import CrawlerProcess
import json
import schedule
import time

from main_spider import MainSpider
from db import init_db
from validation import is_url, is_regex


parser = argparse.ArgumentParser(description='Crawl an url and find matching regex')

parser.add_argument(
    '--db-path',
    default='db.json',
    help='Database path, default to db.json',
)
parser.add_argument(
    '-u',
    required=True,
    metavar='URL',
    action='append',
    help='URL to crawl',
)
parser.add_argument(
    '-r',
    required=True,
    metavar='REGEX',
    action='append',
    help='Regex to search in this URL',
)
parser.add_argument(
    '--input-path',
    default=[],
    help='(optional) The path to the JSON file contains urls and regexes',
)

args = parser.parse_args()

db = init_db(args.db_path)

# Create url_items
url_items = []
# url_items is a list of item {url: 'http://google.com', regex: 'google'}

if len(args.u) != len(args.r):
    print('Error: Number of URLs and number of regexes are not the same')
    exit(1)

for i in range(0, len(args.u)):
    url_items.append({
        'url': args.u[i],
        'regex': args.r[i],
    })

# If the input path is provided
if args.input_path:
    with open(args.input_path) as f:
        url_items += json.load(f)

# Validation
for item in url_items:
    if not is_url(item['url']):
        print('Invalid URL:', item['url'])
        exit(1)

    if not is_regex(item['regex']):
        print('Invalid Regex:', item['regex'])
        exit(1)

def start_crawl():
    process = CrawlerProcess(settings={})
    process.crawl(MainSpider, url_items=url_items, db=db)
    process.start()

# run crawler every day at 00:00
try:
    schedule.every().day.at('00:00').do(start_crawl)
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    for job in schedule.jobs:
        schedule.cancel_job(job)
