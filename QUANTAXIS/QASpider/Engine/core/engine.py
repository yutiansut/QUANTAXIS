#!/usr/bin/env python3
# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: MIT License
# File   : engine.py
# Date   : 2016-12-24 03:03
# Version: 0.0.3
# Description: the core engine of this crawler, which schedules the downloader to handle requests
# in the queue. Besides, it invokes corresponding parser of different spiders to process responses
# in the other queue.

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pprint import pformat
from queue import Queue, Empty
from random import randint

import pybloom
import requests

from ..spider import Request
from ..spider import Response
from ..utils.url import url_fingerprint


__all__ = ['CrawlerEngine']

# Disable the log of requests lib.
logging.getLogger('requests').setLevel(logging.CRITICAL)


class CrawlerEngine(object):
    def __init__(self, concurrent_requests=128,
                 download_delay=0, download_timeout=5, retry_on_timeout=False,
                 queue_size=1024):
        """
        Crawler engine, the brain of this crawler.

        :param concurrent_requests: how many requests you want to handle simultaneously
        :param download_delay: download delay for two batches, default is 0
        :param download_timeout: download timeout
        :param retry_on_timeout: failed requests on timeout will be retried when set to True
        :param queue_size: the size of responses and requests queue
        """
        self.logger = logging.getLogger(__name__)
        self.status = False
        self.concurrent_requests = concurrent_requests
        self.download_delay = download_delay
        self.engine_idle_timeout = 1.5 * download_timeout
        self.download_timeout = download_timeout
        self.retry_on_download_timeout = retry_on_timeout
        self._requests_queue = Queue(queue_size)
        self._responses_queue = Queue(queue_size)
        self._spiders = {}

        # filter duplicate requests in the queue, we use BloomFilter instead of a set container
        self._seen = pybloom.ScalableBloomFilter()

    def start(self):
        """
        Start the engine.
        """
        self._engine_started()
        self.status = True

        self._init_seed_requests()

        # start download scheduler thread in background
        threading.Thread(target=self._sch_download, daemon=True).start()

        # process all the responses in foreground
        self._process_queued_responses()

    def shutdown(self):
        """
        Shutdown the engine.
        """
        self.status = False
        self._engine_stopped()

    def submit(self, spider_cls, *args, **kwargs):
        """
        Submit a new crawling task.

        :param spider_cls: class of spider
        :param args: args for spider
        :param kwargs: key-word args for spider
        :return: None
        """
        spider = spider_cls(*args, crawler=self, **kwargs)

        # Make sure the names of different spiders are unique
        if spider.name in self._spiders:
            raise Exception('Spider {} exists, change your spider name if you want to proceed.'.format(spider.name))

        self._spiders[spider.name] = spider

    def crawl(self, request, spider):
        """
        Crawl next request.

        :param request: `Request` object
        :param spider: spider instance
        :return:
        """
        self._enqueue_request(request, spider)

    def _engine_idle(self):
        """
        This method will be invoked when there's no more requests in the queue.
        :return: None
        """
        self.logger.debug('Crawler engine is in idle mode')

        # tell the spiders that the engine is in idle mode
        self.__call_func_in_spiders('spider_idle')

    def _engine_started(self):
        """
        This method will be invoked when the engine starts.
        :return: None
        """
        self.logger.info('Crawler engine started')

        # tell all the spiders that the engine starts successfully.
        self.__call_func_in_spiders('spider_started')

    def _engine_stopped(self):
        """
        This method will be invoked when the engine is down.
        :return: None
        """
        self.logger.info('Crawler engine stopped')

        # tell all the spiders that the engine is down
        self.__call_func_in_spiders('spider_stopped')

    def _init_seed_requests(self):
        """
        Initial requests to be handled.
        """
        for spider in self._spiders.values():
            try:
                [self.crawl(request, spider) for request in self.__call_func_in_spider(spider, 'start_requests')]
            except Exception as err:
                self.logger.error(err, exc_info=True)

    def _process_request(self, request, spider):
        """
        Process a new request for a spider
        :param request: `Request` object
        :param spider: a spider instance
        :return: None
        """
        self.logger.debug('[{}][{}] Processing request: {}'.format(spider.name, self._requests_queue.qsize(), request))
        self.__call_func_in_spider(spider, 'process_request', request)

    def _enqueue_request(self, request, spider):
        if request:
            if not request.dont_filter and self.__request_seen(request):
                self.logger.debug('[{}] Ignore duplicated request {}'.format(spider.name,
                                                                             request))
                return

        self._requests_queue.put((request, spider))

    def _process_response(self, response, spider):
        """
        Process a new response for a spider.
        """
        self.logger.debug(
            '[{}][{}] Processing response: {}'.format(spider.name, self._responses_queue.qsize(), response))
        self.__call_func_in_spider(spider, 'process_response', response)
        try:
            # get the specific callback method or the default one
            parse = getattr(response.request, 'callback', None) or getattr(spider, 'parse')
            result = parse(response)
            if result is None:
                return

            for r in parse(response):
                if r is None:
                    continue

                if isinstance(r, dict):
                    # item is dict type
                    self._process_item(r, spider)
                elif isinstance(r, Request):
                    # new requests will be put in the queue to be crawled in some time
                    self.crawl(r, spider)
                else:
                    self.logger.error('Expected types are `dict`, `Request` and `None`')

        except Exception as err:
            self.logger.error(err, exc_info=True)

    def _process_item(self, item, spider):
        """
        Process one item for a spider

        :param item: item in dict type
        :param spider: a spider instance
        :return: None
        """
        self.logger.debug('[{}] Scraped item: {}'.format(spider.name, pformat(item)))
        self.__call_func_in_spider(spider, 'process_item', item)

    def _process_queued_responses(self):
        """
        Process all the queued responses until the queue is empty.
        """
        while self.status:
            try:
                response, spider = self._responses_queue.get(timeout=self.engine_idle_timeout)
                self._process_response(response, spider)
            except Empty:
                self.shutdown()

            time.sleep(0.05)

    def _sch_download(self):
        """
        Scheduler processes all the requests in the queue.
        """
        with ThreadPoolExecutor(self.concurrent_requests) as executor:
            while self.status:
                futures = [executor.submit(self._download, req, spider) for req, spider in self._next_requests_batch()]
                _ = futures
                # for f in as_completed(futures):
                #     # wait until all the requests in this batch are downloaded
                #     _ = f

                time.sleep(self.download_delay * randint(1, 5))

        self.logger.debug('Stop downloaders.')
        executor.shutdown(False)

    def _download(self, request, spider):
        def _retry():
            if self.retry_on_download_timeout:
                self.logger.debug('Read timed out, retry request {}'.format(request))
                self.crawl(request, spider)

        try:
            self._process_request(request, spider)

            if request is None:
                return

            method = request.method.upper()

            resp = None
            kw_params = {
                'timeout': self.download_timeout,
                'cookies': request.cookies,
                'headers': request.headers,
                'proxies': {
                    'http': request.proxy,
                    'https': request.proxy
                }
            }

            self.logger.debug('[{}]<{} {}>'.format(spider.name, method, request.url))

            if method == 'GET':
                resp = requests.get(request.url, **kw_params)
            elif method == 'POST':
                resp = requests.post(request.url, request.data, **kw_params)

            self._responses_queue.put((Response(resp.url, resp.status_code, resp.content, request,
                                                resp.cookies), spider))
        except (requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError):
            _retry()
        except Exception as err:
            self.logger.error(err, exc_info=True)

    def _next_requests_batch(self):
        for i in range(self.concurrent_requests):
            try:
                yield self._requests_queue.get(timeout=1)
            except Empty:
                self._engine_idle()

    def __call_func_in_spider(self, spider, name, *args, **kwargs):
        try:
            if hasattr(spider, name):
                return getattr(spider, name)(*args, **kwargs)
        except Exception as err:
            self.logger.error(err, exc_info=True)

    def __call_func_in_spiders(self, name, *args, **kwargs):
        for s in self._spiders.values():
            self.__call_func_in_spider(s, name, *args, **kwargs)

    def __request_seen(self, request):
        fp = self.__request_fingerprint(request)
        if fp in self._seen:
            return True
        self._seen.add(fp)

    @staticmethod
    def __request_fingerprint(request):
        return url_fingerprint(request.url)
