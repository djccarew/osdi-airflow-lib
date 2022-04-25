# OSDU Airflow Library

OSDU Airflow Library is the package providing Airflow specific logic.

## Contents

* [Getting Started](#getting-started)
* * [Backward Compatibility](#backward-compatibility)
* * [Installation from source](#installation-from-source)
* * [Installation from Package Registry](#installation-from-package-registry)
* [Package Lifecycle](#package-lifecycle)
* [Licence](#licence)

# Getting Started

## Backward Compatibility
Airflow 1.10.15 is as a “bridge” release but in OSDU Airflow 1.10.10 version should be supported.


## Installation from source


1. Pull the latest changes from https://community.opengroup.org/osdu/platform/data-flow/ingestion/osdu-airflow-lib

2. Use Python 3.6. Also, it is highly recommended using an isolated virtual environment for development purposes
  (Creation of virtual environments: https://docs.python.org/3.6/library/venv.html)

3.  Make sure you have setuptools and wheel installed
```sh
pip install --upgrade setuptools wheel
```

4.  Change directory to the root of the project

```sh
cd path/to/osdu-airflow-lib
```

5. Make sure osdu-airflow isn't already installed
```sh
pip uninstall osdu-airflow
````

6. Install OSDU Airflow

```sh
python setup.py install
```

Example import after installing:

```python
from osdu_airflow.backward_compatibility.default_args import update_default_args
```

## Installation from Package Registry

```sh
pip install 'osdu-airflow' --extra-index-url=https://community.opengroup.org/api/v4/projects/668/packages/pypi/simple
```

# Package Lifecycle
The project can be deleted once Airflow 1.10.10 version support will be deprecated and no any additional logic will be added.

## Licence
Copyright © Google LLC
Copyright © EPAM Systems

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
A package to interface with OSDU microservices
