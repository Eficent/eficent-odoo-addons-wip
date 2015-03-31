# -*- coding: utf-8 -*-
# Authors: Leonardo Pistone, Jordi Ballester Alomar
# Copyright 2014 Camptocamp SA (http://www.camptocamp.com)
# Copyright 2015 Eficent (http://www.eficent.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public Lice
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.tests.common import TransactionCase


class TestPropagateDepartment(TransactionCase):
    def setUp(self):
        super(TestPropagateDepartment, self).setUp()

        self.po_model = self.registry('purchase.order')
        self.inv_model = self.registry('account.invoice')

        self.po = self.po_model.create(
                    self.cr, self.uid,
                    {'company_id': })
        self.dep_rd = self.browse_ref('hr.dep_rd')

    def test_it_propagates_empty_department(self):
        inv_id = self.po_model.action_invoice_create(
            self.cr, self.uid, self.po.id)
        inv = self.inv_movel.browse(self.cr, self.uid, inv_id)

        self.assertFalse(inv.department_id)

    def test_it_propagates_a(self):
        po = self.po_model.browse(self.cr, self.uid, self.po)
        po.department_id.id = self.dep_rd.id
        inv_id = self.po_model.action_invoice_create(
            self.cr, self.uid, self.po.id)
        inv = self.inv_movel.browse(self.cr, self.uid, inv_id)

        self.assertEqual(self.dep_rd.id, inv.department_id)