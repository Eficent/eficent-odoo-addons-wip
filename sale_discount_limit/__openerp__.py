# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Sistemas Adhoc
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
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
    'name': 'Sale Discount Limit',
    'version': '1.0',
    'description': """
Sale Discount Limit
===================
This module was created to extend the sales process. It allows to
set a maximum permitted sales discount % on each product on a sale quotation.

A sales user cannot approve a sales quotation if any of the items contain a
sales discount % above the maximum allowed.

A user can manually initiate the maximum discount limit check when the quote
is in status draft or sent.

Users belonging to the group 'Sales Quotation Discount Block Releaser' will
have the permission to override this rule and approve the sales quotation.


Installation
============

No specific installation steps are required.

Configuration
=============

No specific configuration steps are required.

Usage
=====

No specific usage instructions are required.


Known issues / Roadmap
======================

No issues have been identified with this module.

Credits
=======

Contributors
------------

* Jordi Ballester Alomar <jordi.ballester@eficent.com>
    """,
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'depends': ['sale'],
    'init_xml': [],
    'update_xml': [
        'security/sale_discount_limit_security.xml',
        'security/ir.model.access.csv',
        'view/sale_workflow.xml',
        'view/sale_view.xml',
        'view/product_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
}