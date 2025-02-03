# -*- coding: utf-8 -*-

import json

from locust import FastHttpUser, task, between, constant_throughput, LoadTestShape
import random
import json
import math

default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

NUM_KEYS = 10000
API_ROUTE = 'on_demand_compute'
RPS_PER_USER = 10
TEST_FEATURE_NAME = 'test_feature'


class Requester(FastHttpUser):
    wait_time = constant_throughput(RPS_PER_USER)

    @task
    def get_feature(self):
        i = random.randint(0, NUM_KEYS)
        req = {
            'args': [{
                'feature_name': TEST_FEATURE_NAME,
                'serve_or_udf': True,
                'keys': {
                    'key': f'key_{i}'
                }
            }]
        }
        req_json = json.dumps(req)
        # self.client.client.clientpool.close() # not to reuse connections/keep-alive
        self.client.get(f'{API_ROUTE}/{req_json}', headers=default_headers)


class StepLoadShape(LoadTestShape):
    use_common_options = True
    # step_time = 120 # how long to hold each step in seconds
    # step_load = 10 # how many users to add each step as well as how many users to start with
    # spawn_rate = 10 # what rate to spawn the users per second
    # time_limit = 300 # how long to run the test in seconds

    def tick(self):
        # Returns how long the test has been running for in seconds
        run_time = self.get_run_time()
        time_limit = self.runner.environment.parsed_options.run_time
        step_load = self.runner.environment.parsed_options.users
        
        # this is a hack - we pass step_time as a spawn_rate param from locust client (same on client)
        step_time = self.runner.environment.parsed_options.spawn_rate

        if run_time > time_limit:
            return None

        # Figure out which step we are currently on.
        current_step = math.floor(run_time / step_time) + 1
        
        # How many users should be running right now,
        # and how fast to spawn users if we need to add additional users.
        # By making the step_load == spawn_rate the users for each step
        # will be spawned immediately once required
        return current_step * step_load, step_load

        