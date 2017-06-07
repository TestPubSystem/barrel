#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os

SERVER = "http://127.0.0.1:5000"
BASE_URL = SERVER + "/api/v1"
EXAMPLES_PATH = os.path.join(os.path.pardir, "examples")

headers = {
    "Content-Type": "application/json"
}

files = {}

for s in os.listdir(EXAMPLES_PATH):
    if s.endswith(".json"):
        with open(os.path.join(EXAMPLES_PATH, s), encoding="utf-8") as f:
            files[s[:-5]] = f.read().encode("utf-8")

access_token = None
session = requests.session()
session.headers["Content-Type"] = "application/json"

resp = session.post(BASE_URL + "/auth", data=files["auth"])
content = json.loads(resp.content.decode())
session.headers["Authorization"] = "JWT " + content["access_token"]

resp = session.get(BASE_URL + "/tags")
tags = json.loads(resp.content.decode())["data"]
if not tags:
    resp = requests.post(BASE_URL + "/tags/", data=files["post_tag"], headers=headers)
    resp = requests.post(BASE_URL + "/tags/", data=files["post_tag2"], headers=headers)
    resp = requests.post(BASE_URL + "/tags/", data=files["post_tag3"], headers=headers)

resp = requests.post(BASE_URL + "/tests/", data=files["post_test"])
test1_id = json.loads(resp.content.decode())["data"]["id"]
requests.post(BASE_URL + "/tests/%s/tags/%s" % (test1_id, "Regress"))

resp = requests.post(BASE_URL + "/tests/", data=files["post_test"])
test2_id = json.loads(resp.content.decode())["data"]["id"]
requests.post(BASE_URL + "/tests/%s/revisions/" % test2_id, data=files["post_test2_revision"])
requests.post(BASE_URL + "/tests/%s/tags/%s" % (test2_id, "Regress"))
requests.post(BASE_URL + "/tests/%s/tags/%s" % (test2_id, "Smoke"))

resp = requests.post(BASE_URL + "/testsuites/", data=files["post_suite"])
test_suite1_id = json.loads(resp.content.decode())["data"]["id"]
requests.post(BASE_URL + "/testsuites/%s/tags/%s" % (test_suite1_id, "Regress"))
requests.post(BASE_URL + "/testsuites/%s/tests/%s" % (test_suite1_id, test1_id))
requests.post(BASE_URL + "/testsuites/%s/tests/%s" % (test_suite1_id, test2_id))

resp = requests.post(BASE_URL + "/suiteruns/", data=files["post_suite_run"])
suiterun = json.loads(resp.content.decode())["data"]
requests.put(
    BASE_URL + "/stepresults/%s" % suiterun["test_runs"][0]["step_results"][0]["id"],
    data=files["post_suite_run"]
)
requests.patch(
    BASE_URL + "/testruns/%s" % suiterun["test_runs"][0]["id"],
    data=files["post_suite_run"]
)
