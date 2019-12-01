from scrapy.crawler import CrawlerProcess
from tinydb import Query
import os
import json
import pytest
from multiprocessing import Process

from main_spider import MainSpider
from db import init_db


@pytest.mark.skip(reason='Helper function to remove db file')
def remove_path(path):
    if os.path.exists(path):
        os.remove(path)

@pytest.mark.skip(reason='Helper function to create a new process')
def create_process(url_items, db):
    def crawl():
        crawler = CrawlerProcess(settings={
            'LOG_ENABLED': False,
            'TELNETCONSOLE_ENABLED': False,
        })

        crawler.crawl(MainSpider, url_items=url_items, db=db)
        crawler.start()

    process = Process(target=crawl)
    process.start()
    process.join()



def test_normal():
    db_path = 'test_normal.json'
    remove_path(db_path)
    db = init_db(db_path)

    correct_output = {
        'url': 'http://motherfuckingwebsite.com/',
        'regex': 'light(weight)?',
        'matches': [
            {
                'text': 'lightweight',
                'start': 573,
                'end': 584,
            },
            {
                'text': 'lightweight',
                'start': 1554,
                'end': 1565,
            },
        ],
    }

    url_items = [
        {
            'url': 'http://motherfuckingwebsite.com/',
            'regex': 'light(weight)?',
        }
    ]

    create_process(url_items, db)
    output_items = db.all()

    assert(len(output_items) > 0)
    item = output_items[0]
    assert(len(correct_output['matches']) == len(item['matches']))

    for i in range(len(item['matches'])):
        for key in item['matches'][i].keys():
            assert(correct_output['matches'][i][key] == item['matches'][i][key])

    remove_path(db_path)


def test_pattern_not_found():
    db_path = 'test_normal.json'
    remove_path(db_path)
    db = init_db(db_path)

    url_items = [
        {
            'url': 'http://motherfuckingwebsite.com/',
            'regex': 'Finland',
        }
    ]

    create_process(url_items, db)

    output_items = db.all()
    assert(len(output_items) > 0)
    item = output_items[0]
    assert(len(item['matches']) == 0)

    remove_path(db_path)

def test_wrong_url():
    db_path = 'test_404_page.json'
    remove_path(db_path)
    db = init_db(db_path)

    url_items = [
        {
            'url': 'http://cuchidatluaanhhung.com/',
            'regex': 'Finland',
        }
    ]

    create_process(url_items, db)

    output_items = db.all()

    assert(len(output_items) == 0)
    remove_path(db_path)

def test_redirect_url():
    db_path = 'test_redirect_url.json'
    remove_path(db_path)
    db = init_db(db_path)

    url_items = [
        {
            'url': 'https://about.google.com/', # 301 HTTP code
            'regex': 'Policy',
        }
    ]

    correct_output = {
        'matches': [
            {
                'text': 'Policy',
                'start': 24355,
                'end': 24361,
            }
        ],
    }



    create_process(url_items, db)

    output_items = db.all()
    assert(len(output_items) > 0)

    item = output_items[0]
    assert(len(correct_output['matches']) == len(item['matches']))

    for i in range(len(item['matches'])):
        for key in item['matches'][i].keys():
            assert(correct_output['matches'][i][key] == item['matches'][i][key])

    remove_path(db_path)


def test_shorten_url():
    db_path = 'test_shorten_url.json'
    remove_path(db_path)
    db = init_db(db_path)

    url_items = [
        {
            'url': 'https://shorturl.at/giAL4', # 301 HTTP code
            'regex': 'dribbble',
        }
    ]

    correct_output = {
        'matches': [
            {
                'text': 'dribbble',
                'start': 2628,
                'end': 2636,
            },
        ],
    }



    create_process(url_items, db)

    output_items = db.all()
    assert(len(output_items) > 0)

    item = output_items[0]
    assert(len(correct_output['matches']) == len(item['matches']))

    for i in range(len(item['matches'])):
        for key in item['matches'][i].keys():
            assert(correct_output['matches'][i][key] == item['matches'][i][key])

    remove_path(db_path)

test_shorten_url()
