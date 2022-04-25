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


import json
import http
import requests


class MockResponse(requests.Response):
    """
    Mock response is used for monkey patching requests' methods.
    Example usage: monkeypatch.setattr(
                        requests, "get", lambda *args, **kwargs: MockResponse(http.HTTPStatus.OK)
                   )
    """

    def __init__(self, status_code: http.HTTPStatus):
        super(MockResponse, self).__init__()
        self.status_code = status_code
        self.url = "Test"
        self.reason = "Test"

    @property
    def text(self):
        return None


class MockWorkflowResponse(MockResponse):

    def __init__(self, json: str = "", status_code: http.HTTPStatus = http.HTTPStatus.OK):
        super().__init__(status_code)
        self._json = json

    def json(self):
        return self._json
