# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from __future__ import absolute_import, print_function

from jsonref import JsonRef
from jsonresolver import JSONResolver
from jsonresolver.contrib.jsonref import json_loader_factory

from invenio_opendefinition.tasks import harvest_licenses


def test_license_jsonref_resolver(app, licenses_example):
    with app.app_context():
        # load test data, mocked to data/opendefinition-licenses.json
        harvest_licenses()
        example_license = {
            'license': {'$ref': 'http://localhost/licenses/MIT'}
        }

        json_resolver = JSONResolver(plugins=[
            'invenio_opendefinition.resolvers'
        ])
        loader_cls = json_loader_factory(json_resolver)
        loader = loader_cls()
        out_json = JsonRef.replace_refs(example_license, loader=loader)
        del out_json['license']['$schema']
        assert out_json['license'] == licenses_example['MIT']