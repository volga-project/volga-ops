# -*- coding: utf-8 -*-

import json

from locust import FastHttpUser, task, between
import random
import json

default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

NUM_KEYS = 10000
API_ROUTE = 'on_demand_compute'


class Requester(FastHttpUser):

    @task
    def get_feature(self):
        i = random.randint(0, NUM_KEYS)
        req = {
            'args': [{
                'feature_name': 'test_feature',
                'serve_or_udf': True,
                'keys': {
                    'key': f'key_{i}'
                }
            }]
        }
        req_json = json.dumps(req)
        self.client.client.clientpool.close() # not to reuse connections/keep-alive
        self.client.get(f'{API_ROUTE}/{req_json}', headers=default_headers)
        