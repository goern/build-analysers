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

"""Thoth: Build Analyses Controller."""

import os
import tempfile
import time
import logging
import json
import yaml
from datetime import datetime

import requests
import daiquiri
from kubernetes import client, config, watch

from thoth_build_analysers import openshift


DEBUG = bool(os.getenv('DEBUG', True))
API_GROUP = 'thoth-station.ninja'
PLURAL = 'buildanalysises'
VERSION = 'v1alpha1'

daiquiri.setup(level=logging.DEBUG, outputs=('stdout', 'stderr'))
_LOGGER = daiquiri.getLogger(__name__)


def analyse_build(crds, obj):
    """Get the given BuildLog and analyse it."""
    metadata = obj.get("metadata")
    namespace = metadata.get("namespace")
    name = metadata.get("name")

    time.sleep(10)

    obj['status']['phase'] = 'Running'
    obj['status'] = {'conditions': {'type': 'Downloaded', 'status': False}}

    _LOGGER.debug(
        f"downloading BuildLog from {obj['spec']['buildlog']['url']}")
    # Use the TemporaryFile context manager for easy clean-up
    response = requests.get(obj['spec']['buildlog']['url'])
    # TODO exception handling of HTTP

    obj['status']['conditions'].append({'type': 'Downloaded', 'status': True})

    with tempfile.TemporaryFile() as tmp:
        tmp.write(response.content)

        result = openshift.analyse(name, response.content)

        obj['result'] = result

    # downloaded['lastTransitionTime'] = datetime.utcnow()

    obj['status']['phase'] = 'Finished'

    crds.replace_namespaced_custom_object(
        API_GROUP, VERSION, namespace, PLURAL, name, obj)


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    configuration = client.Configuration()
    configuration.assert_hostname = False

    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)

    crds = client.CustomObjectsApi(api_client)

    _LOGGER.info("Waiting for new Build Analysis to come up...")

    resource_version = ''
    while True:
        stream = watch.Watch().stream(
            crds.list_namespaced_custom_object, API_GROUP,
            VERSION, 'myproject', PLURAL, resource_version=resource_version)

        for event in stream:
            _LOGGER.debug(event)
            obj = event["object"]
            operation = event['type']
            spec = obj.get('spec')

            if not spec:
                continue

            metadata = obj.get('metadata')
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            _LOGGER.debug(
                f"Handling {operation} on {name}.resource_version={resource_version}")

            status = obj.get('status')

            if status and status['phase'].lower() == 'finished':
                continue

            if operation == 'DELETED':
                continue

            analyse_build(crds, obj)
