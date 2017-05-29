#!/bin/bash

HOST="http://127.0.0.1:5000"
BASE_URL="$HOST/api/v1"

curl "$BASE_URL/tags/" -d @post_tag.json
curl "$BASE_URL/tags/" -d @post_tag2.json
curl "$BASE_URL/tags/" -d @post_tag3.json

curl "$BASE_URL/tests/" -d @post_test.json
curl "$BASE_URL/tests/1/tags/Regress" -X POST
curl "$BASE_URL/tests/" -d @post_test.json
curl "$BASE_URL/tests/2/revisions/" -d @post_test2.json
curl "$BASE_URL/tests/2/tags/Regress" -X POST
curl "$BASE_URL/tests/2/tags/Smoke" -X POST

curl "$BASE_URL/testsuites/" -d @post_suite.json
curl "$BASE_URL/testsuites/1/tags/Regress" -X POST
curl "$BASE_URL/testsuites/1/tests/1" -X POST
curl "$BASE_URL/testsuites/1/tests/2" -X POST

