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

import os

DATA_PATH_PREFIX = f"{os.path.dirname(__file__)}/data"

MANIFEST_GENERIC_SCHEMA_PATH = f"{DATA_PATH_PREFIX}/manifests/schema_Manifest.1.0.0.json"

MANIFEST_WELLBORE_VALID_PATH = f"{DATA_PATH_PREFIX}/master/Wellbore.0.3.0.json"
MANIFEST_BATCH_WELLBORE_VALID_PATH = f"{DATA_PATH_PREFIX}/master/batch_Wellbore.0.3.0.json"

SEARCH_VALID_RESPONSE_PATH = f"{DATA_PATH_PREFIX}/other/SearchResponseValid.json"
