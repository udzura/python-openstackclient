#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import uuid

from openstackclient.tests.functional.volume.v1 import common


class QosTests(common.BaseVolumeTests):
    """Functional tests for volume qos. """

    def test_volume_qos_create_list(self):
        """Test create, list, delete multiple"""
        name1 = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'volume qos create -f json ' +
            name1
        ))
        self.assertEqual(
            name1,
            cmd_output['name']
        )

        name2 = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'volume qos create -f json ' +
            name2
        ))
        self.assertEqual(
            name2,
            cmd_output['name']
        )

        # Test list
        cmd_output = json.loads(self.openstack(
            'volume qos list -f json'
        ))
        names = [x["Name"] for x in cmd_output]
        self.assertIn(name1, names)
        self.assertIn(name2, names)

        # Test delete multiple
        del_output = self.openstack('volume qos delete ' + name1 + ' ' + name2)
        self.assertOutput('', del_output)

    def test_volume_qos_set_show_unset(self):
        """Tests create volume qos, set, unset, show, delete"""

        name = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'volume qos create -f json ' +
            '--consumer front-end '
            '--property Alpha=a ' +
            name
        ))
        self.addCleanup(self.openstack, 'volume qos delete ' + name)
        self.assertEqual(
            name,
            cmd_output['name']
        )

        self.assertEqual(
            "front-end",
            cmd_output['consumer']
        )

        # Test volume qos set
        raw_output = self.openstack(
            'volume qos set ' +
            '--property Alpha=c ' +
            '--property Beta=b ' +
            name,
        )
        self.assertOutput('', raw_output)

        # Test volume qos show
        cmd_output = json.loads(self.openstack(
            'volume qos show -f json ' +
            name
        ))
        self.assertEqual(
            name,
            cmd_output['name']
        )
        self.assertEqual(
            "Alpha='c', Beta='b'",
            cmd_output['properties']
        )

        # Test volume qos unset
        raw_output = self.openstack(
            'volume qos unset ' +
            '--property Alpha ' +
            name,
        )
        self.assertOutput('', raw_output)

        cmd_output = json.loads(self.openstack(
            'volume qos show -f json ' +
            name
        ))
        self.assertEqual(
            name,
            cmd_output['name']
        )
        self.assertEqual(
            "Beta='b'",
            cmd_output['properties']
        )

    # TODO(qiangjiahui): Add tests for associate and disassociate volume type
