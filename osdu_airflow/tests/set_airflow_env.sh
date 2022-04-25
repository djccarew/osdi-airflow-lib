#  Copyright 2020 Google LLC
#  Copyright 2020 EPAM Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
pip uninstall osdu-api -y
pip install --upgrade google-api-python-client
pip install dataclasses
pip install jsonschema
pip install google
pip install toposort
pip install google-cloud-storage
pip install deepdiff
pip install azure-identity
pip install azure-keyvault-secrets
pip install msal
pip install python-keycloak
pip install osdu-api==0.12.0.dev213 --extra-index-url https://community.opengroup.org/api/v4/projects/148/packages/pypi/simple
pip install osdu-ingestion==0.12.0.dev20 --extra-index-url https://community.opengroup.org/api/v4/projects/823/packages/pypi/simple

export WORKFLOW_URL="http://127.0.0.1:5000"
export UPDATE_STATUS_URL="http://127.0.0.1:5000/wf/us"
export STORAGE_URL="http://127.0.0.1:5000/st"
export SEARCH_URL="http://127.0.0.1:5000/sr/qr"
export LOCALHOST="http://127.0.0.1:5000"
export SEARCH_CONN_ID="http://127.0.0.1:5000"
export WORKFLOW_CONN_ID="http://127.0.0.1:5000"
export DATALOAD_CONFIG_PATH="/usr/local/airflow/dags/configs/dataload.ini"
export SA_FILE_PATH="test"

airflow initdb > /dev/null 2>&1

# exclude testing DAGS
sed -i 's/load_examples = True/load_examples = False/'  /usr/local/airflow/airflow.cfg
# turn on all dags
sed -i 's/dags_are_paused_at_creation = True/dags_are_paused_at_creation = False/'  /usr/local/airflow/airflow.cfg

airflow variables -s core__service__storage__url $STORAGE_URL
airflow variables -s core__provider gcp
airflow variables -s core__service__workflow__host $WORKFLOW_URL
airflow variables -s core__service__file__host $LOCALHOST
airflow variables -s core__service__workflow__url $UPDATE_STATUS_URL
airflow variables -s core__service__search__url $SEARCH_URL
airflow variables -s core__service__schema__url  $LOCALHOST
airflow variables -s core__config__dataload_config_path $DATALOAD_CONFIG_PATH
airflow variables -s core__auth__access_token test
airflow variables -s core__ingestion__batch_count 3

airflow connections -a --conn_id workflow --conn_uri $WORKFLOW_CONN_ID
airflow connections -a --conn_id google_cloud_storage --conn_uri $LOCALHOST

mkdir -p /usr/local/airflow/dags/
mkdir -p /usr/local/airflow/plugins/

# Copying folders as the tests expect the dags/operator files to follow existing structure
# cp -r src/osdu_dags/osdu_manifest/hooks /usr/local/airflow/plugins/
# cp -r src/osdu_dags/osdu_manifest/operators /usr/local/airflow/plugins/

# cp -r src/osdu_dags/osdu_manifest/configs /usr/local/airflow/dags/
# cp -r src/osdu_dags/osdu_manifest/libs /usr/local/airflow/dags/
# cp -r src/osdu_dags/osdu_manifest/providers /usr/local/airflow/dags/
# cp -r src/osdu_dags/*.py /usr/local/airflow/dags/

# Changing import statements for existing tests to work
# for f in $(find /usr/local/airflow/dags -name '*.py'); do sed -i 's/osdu_manifest.//g' $f; done
# for f in $(find /usr/local/airflow/plugins -name '*.py'); do sed -i 's/osdu_manifest.//g' $f; done

# cp -r tests/end-to-end-tests/mock-external-apis /mock-server
# cp -r tests/end-to-end-tests/mock-data /mock-server/mock-data

# cp tests/end-to-end-tests/{test-osdu-ingest-r2-success.sh,test-osdu-ingest-r2-fail.sh} /mock-server/
# cp tests/end-to-end-tests/osdu_api_config.yaml /mock-server/
cp tests/*.py /mock-server/

chmod +x /mock-server/{test-osdu-ingest-r2-success.sh,test-osdu-ingest-r2-fail.sh}
