#!/usr/bin/env python3
# Sesheta
# Copyright(C) 2018 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""test..."""

from os import listdir
from os.path import isfile, join

import pytest


FIXTURE_PATH = './fixtures/'


@pytest.fixture()
def all_build_logs():  # Ignore PyDocStyleBear
    all_fixtures = [f for f in listdir(
        FIXTURE_PATH) if isfile(join(FIXTURE_PATH, f))]

    all_build_logs = {}

    for fixture_file in all_fixtures:
        with open(join(FIXTURE_PATH, fixture_file)) as f:
            all_build_logs[fixture_file] = f.read()

    return all_build_logs
