#!/bin/bash
set -x

HOST="http://127.0.0.1:5000"
#HOST="http://tishka17.pythonanywhere.com"
BASE_URL="$HOST/api/v1"

curl "$BASE_URL/auth" -H "Content-Type: application/json" -d @auth.json

curl "$BASE_URL/tags/" -d @post_tag.json
curl "$BASE_URL/tags/" -d @post_tag2.json
curl "$BASE_URL/tags/" -d @post_tag3.json

curl "$BASE_URL/tests/" -d @post_test.json
curl "$BASE_URL/tests/1/tags/Regress" -X POST
curl "$BASE_URL/tests/" -d @post_test.json
curl "$BASE_URL/tests/2/revisions/" -d @post_test2_revision.json
curl "$BASE_URL/tests/2/tags/Regress" -X POST
curl "$BASE_URL/tests/2/tags/Smoke" -X POST

curl "$BASE_URL/testsuites/" -d @post_suite.json
curl "$BASE_URL/testsuites/1/tags/Regress" -X POST
curl "$BASE_URL/testsuites/1/tests/1" -X POST
curl "$BASE_URL/testsuites/1/tests/2" -X POST

curl "$BASE_URL/suiteruns/" -d @post_suite_run.json
curl "$BASE_URL/stepresults/1" -d @put_step_result.json -X PUT
curl "$BASE_URL/testruns/1" -d @patch_test_run.json -X PATCH
#curl "$BASE_URL/testruns/" -d @post_test_run.json
