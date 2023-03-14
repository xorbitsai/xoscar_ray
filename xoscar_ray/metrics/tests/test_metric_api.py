# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from xoscar.metrics import api
from xoscar.metrics.api import init_metrics, shutdown_metrics

from ..backends import ray

del ray


@pytest.fixture
def init():
    init_metrics()


def test_init_metrics():
    init_metrics("ray")
    assert api._metric_backend == "ray"
    shutdown_metrics()
