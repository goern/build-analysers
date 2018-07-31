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

"""Thoth: Build Analysers."""

from thoth_build_analysers.exceptions import EmptyBuildLogException, BuildLogAnalysisException


def analyse(build_log_name: str, build_log_text: str) -> dict:
    """Analyse OpenShift BuildLogs."""
    if (build_log_text is None) or (build_log_text is ''):
        raise EmptyBuildLogException

    result = {'buildLog': build_log_name, 'result': {'status': 'failed'}}
    log_lines = build_log_text.splitlines()

    if 'Push successful' in log_lines[-1]:
        result['hint'] = 'OpenShift Build Log'
        result['result']['status'] = 'successful'
        result['result']['message'] = 'OpenShift Build successful'

        return result

    n = 0
    for line in log_lines:
        if 'pulling image error : manifest unknown: manifest unknown' in line:
            result['hint'] = 'Jenkins Build Log'
            result['result']['message'] = 'OpenShift failed to understand the manifest of S2I Builder Image: '
            return result

        if line.startswith('error: build error: non-zero'):
            result['hint'] = 'OpenShift Build Log'

            if 'non-zero' in line and 'exit code' in line:
                result['result']['message'] = f'S2I Builder {line}'

                if 'AttributeError:' in line[n - 1]:
                    result['result']['message'] = result['result'][
                        'message'] + line[n - 1]

                return result

            return result

        if "Your Pipfile.lock" in line and "is out of date" in line:
            result['hint'] = 'OpenShift Build Log'
            return result

        if line.startswith('Finished: FAILURE'):
            result['hint'] = 'Jenkins Build Log'
            return result

        n = n + 1
    # cant conclude successful or not... PANIC!
    raise BuildLogAnalysisException
