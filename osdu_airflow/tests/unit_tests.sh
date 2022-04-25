pip uninstall enum34 -y
pip install pytest
pip install pytest-mock
pip install responses
pip install strict-rfc3339
pip install --upgrade google-api-python-client
chmod +x ./osdu_airflow/tests/set_airflow_env.sh
export AIRFLOW_SRC_DIR="/usr/local/airflow/"
export CLOUD_PROVIDER="provider_test"
./osdu_airflow/tests/./set_airflow_env.sh > /dev/null  2>&1
pytest -s || EXIT_CODE=$?
exit $EXIT_CODE
