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


import http
import json
import os
import sys
from datetime import datetime
from typing import TypeVar, ClassVar
from airflow import DAG
from airflow.models import TaskInstance

sys.path.append(f"{os.getenv('AIRFLOW_SRC_DIR')}/plugins")
sys.path.append(f"{os.getenv('AIRFLOW_SRC_DIR')}/dags")
sys.path.insert(0, './')

from osdu_ingestion.libs.exceptions import PipelineFailedError
import pytest
import requests
import mock_providers
from functools import lru_cache

from file_paths import (
    MANIFEST_WELLBORE_VALID_PATH,
    SEARCH_VALID_RESPONSE_PATH, MANIFEST_GENERIC_SCHEMA_PATH, MANIFEST_BATCH_WELLBORE_VALID_PATH)
from osdu_airflow.operators.process_manifest_r3 import ProcessManifestOperatorR3, SchemaValidator, \
    ManifestProcessor
from osdu_airflow.operators.update_status import UpdateStatusOperator
from osdu_ingestion.libs.handle_file import FileHandler
from mock_responses import MockWorkflowResponse

CustomOperator = TypeVar("CustomOperator")


class MockDagRun:
    def __init__(self, conf):
        self.conf = conf


class MockStorageResponse(requests.Response):

    def json(self, **kwargs):
        return {"recordIds": ["test"]}


class TestOperators(object):

    def _create_batch_task(self, operator: ClassVar[CustomOperator]) -> (CustomOperator, dict):
        with open(MANIFEST_BATCH_WELLBORE_VALID_PATH) as f:
            conf = json.load(f)
        dag = DAG(dag_id='batch_osdu_ingest', start_date=datetime.now())
        task: CustomOperator = operator(dag=dag, task_id='anytask')
        ti = TaskInstance(task=task, execution_date=datetime.now())

        context = ti.get_template_context()
        context["dag_run"] = MockDagRun(conf)
        return task, context

    def _create_task(self, operator: ClassVar[CustomOperator]) -> (CustomOperator, dict):
        with open(MANIFEST_WELLBORE_VALID_PATH) as f:
            conf = json.load(f)
        dag = DAG(dag_id='Osdu_ingest', start_date=datetime.now())
        task: CustomOperator = operator(dag=dag, task_id='anytask')
        ti = TaskInstance(task=task, execution_date=datetime.now())

        context = ti.get_template_context()
        context["dag_run"] = MockDagRun(conf)
        return task, context

    def test_process_manifest_r3_operator(self, monkeypatch):

        @lru_cache()
        def _get_common_schema(*args, **kwargs):
            with open(MANIFEST_GENERIC_SCHEMA_PATH) as f:
                manifest_schema = json.load(f)
            return manifest_schema

        monkeypatch.setattr(SchemaValidator, "get_schema", _get_common_schema)
        monkeypatch.setattr(SchemaValidator, "_validate_against_schema", lambda *args, **kwargs: None)
        monkeypatch.setattr(SchemaValidator, "validate_manifest", lambda obj, entities: entities)
        monkeypatch.setattr(ManifestProcessor, "save_record_to_storage",
                            lambda obj, headers, request_data: MockStorageResponse())
        monkeypatch.setattr(FileHandler, "upload_file",
                            lambda *args, **kwargs: "test")

        task, context = self._create_task(ProcessManifestOperatorR3)
        task.pre_execute(context)
        task.execute(context)

    def test_process_manifest_r3_operator_batch(self, monkeypatch):

        def _get_common_schema(*args, **kwargs):
            with open(MANIFEST_GENERIC_SCHEMA_PATH) as f:
                manifest_schema = json.load(f)
            return manifest_schema

        monkeypatch.setattr(SchemaValidator, "get_schema", _get_common_schema)
        monkeypatch.setattr(SchemaValidator, "_validate_against_schema", lambda *args, **kwargs: None)
        monkeypatch.setattr(SchemaValidator, "validate_manifest", lambda obj, entities: (entities, []))
        monkeypatch.setattr(ManifestProcessor, "save_record_to_storage",
                            lambda obj, headers, request_data: MockStorageResponse())
        monkeypatch.setattr(FileHandler, "upload_file",
                            lambda *args, **kwargs: "test")

        task, context = self._create_batch_task(ProcessManifestOperatorR3)
        task.pre_execute(context)
        task.execute(context)

    def _test_update_status_operator(self, monkeypatch, status: UpdateStatusOperator.prev_ti_state):
        monkeypatch.setattr(UpdateStatusOperator, "get_previous_ti_statuses",
                            lambda obj, context: status)
        monkeypatch.setattr(requests, "put", lambda *args, **kwargs: MockWorkflowResponse(
            status_code=http.HTTPStatus.OK, json="test"))

        task, context = self._create_task(UpdateStatusOperator)
        task.pre_execute(context)
        task.execute(context)

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param(
                UpdateStatusOperator.prev_ti_state.NONE
            ),
            pytest.param(
                UpdateStatusOperator.prev_ti_state.SUCCESS
            )
        ]
    )
    def test_update_status_operator(self, monkeypatch, status):
        self._test_update_status_operator(monkeypatch, status)

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param(
                UpdateStatusOperator.prev_ti_state.FAILED
            )
        ]
    )
    def test_update_status_operator_failed(self, monkeypatch, status):
        """
        Test if operator raises PipeLineFailedError if any previous task failed.
        """
        with pytest.raises(PipelineFailedError):
            self._test_update_status_operator(monkeypatch, status)
