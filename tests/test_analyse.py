#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   thoth-build-analysers
#   Copyright(C) 2018 Christoph Görn
#
#   This program is free software: you can redistribute it and / or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Thoth Build Analysers feature tests."""


import os
import pytest

from thoth_build_analysers import openshift


@pytest.fixture
def pytestbdd_feature_base_dir():  # Ignore PyDocStyleBear
    return '.'


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../fixtures',
)


class TestOpenShiftBuildAnalysers(object):  # Ignore PyDocStyleBear
    def test_openshift_build_logs(self, all_build_logs):  # Ignore PyDocStyleBear
        for build_log in all_build_logs.keys():
            result = openshift.analyse(build_log, all_build_logs[build_log])
            print(f"fixture: {build_log}: {result}")
