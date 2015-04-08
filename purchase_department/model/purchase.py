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

from openerp.osv import orm, fields


class purchase_order(orm.Model):

    _inherit = 'purchase.order'

    _columns = {
        'department_id': fields.many2one('hr.department', string='Department'),
    }

    def _get_my_department(self, cr, uid, ids, context=None):
        employee_obj = self.pool.get('hr.employee')
        department_id = False
        employee_ids = employee_obj.search(
            cr, uid, [('user_id', '=', uid)])
        if employee_ids:
            department_id = employee_obj.browse(
                cr, uid, employee_ids[0], context=context).department_id.id
        return department_id

    _defaults = {
        'department_id': _get_my_department,
    }

    def action_invoice_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get('account.invoice')
        inv_id = super(purchase_order, self).action_invoice_create(
            cr, uid, ids, context=context)
        for order in self.browse(cr, uid, ids, context=context):
            for invoice in order.invoice_ids:
                if order.department_id:
                    invoice_obj.write(
                        cr, uid, [invoice.id],
                        {'department_id': order.department_id.id},
                        context=context)
        return inv_id

    def _prepare_order_picking(self, cr, uid, order, context=None):
        if context is None:
            context = {}
        res = super(purchase_order, self)._prepare_order_picking(
            cr, uid, order, context=context)
        if order.department_id:
            res['department_id'] = order.department_id.id
        return res

    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
        if context is None:
            context = {}
        res = super(purchase_order, self)._prepare_order_line_move(
            cr, uid, order, order_line, picking_id, context=context)
        if order.department_id:
            res['department_id'] = order.department_id.id
        return res


class purchase_order_line(orm.Model):
    _inherit = 'purchase.order.line'

    _columns = {
        'department_id': fields.related('order_id',
                                        'department_id', type='many2one',
                                        relation='hr.department',
                                        string='Department', readonly=True),
    }