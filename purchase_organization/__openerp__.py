# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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
    "name": "Purchase organization",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Purchase Management",
    "depends": ["purchase", "product"],
    "description": """
Purchase organization
=====================

This module provides an organizational unit for procurement-related activities.
Define purchasing organizations according to the following criteria:
    - Business units
    - Procurement policies
    - Geographical areas
    - Products procured
    - The ability to maintain purchasing-specific data, such as prices.

    """,
    "init_xml": [],
    "update_xml": [
        "view/purchase_organization.xml",
        "view/res_users.xml",
        "view/purchase_order.xml",
        "view/purchase_order_line.xml",
        "view/pricelist.xml",
        "security/purchase_organization_security.xml",
        "security/ir.model.access.csv",
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
