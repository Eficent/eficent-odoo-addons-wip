# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "HR Configuration",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "HR",
    "depends": ["hr"],
    "description": """
HR Configuration
================
This module adds a new user group 'HR Configuration' that is allowed to
create, change and delete the objects that are classified under the menu
'configuration'.

The other groups in HR cannot perform the create, change and delete actions
on these objects.

    """,
    "init_xml": [],
    "update_xml": [        
        'security/hr_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
    'certificate': '',
}