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
from openerp.tools.translate import _


class stock_move(orm.Model):
    _inherit = 'stock.move'

    _columns = {
        'department_id': fields.many2one('hr.department', string='Department'),
    }

    def _get_department(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if 'department_id' in context:
            return context.get('department_id', False)
        employee_obj = self.pool.get('hr.employee')
        department_id = False
        employee_ids = employee_obj.search(
            cr, uid, [('user_id', '=', uid)])
        if employee_ids:
            department_id = employee_obj.browse(
                cr, uid, employee_ids[0], context=context).department_id.id
        return department_id

    _defaults = {
        'department_id': _get_department,
    }


    def onchange_department_id(self, cr, uid, ids, department_id,
                               context=None):
        context = context or {}
        res = {}
        for move in self.browse(cr, uid, ids, context=context):
            if move.picking_id and move.picking_id.department_id \
                    and department_id != move.picking_id.department_id.id:
                raise orm.except_orm(
                    _('Error!'),
                    _("The department of the stock move and picking must be "
                      "the same"))
        return res

    def onchange_picking_id(self, cr, uid, ids, picking_id,
                            context=None):
        context = context or {}
        res = {}
        picking = self.pool.get('stock.picking').browse(cr, uid, picking_id,
                                                        context=context)
        if picking.department_id:
            res['department_id'] = picking.department_id.id
        return res


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

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

    def onchange_department_id(self, cr, uid, ids, department_id,
                               context=None):
        context = context or {}
        move_obj = self.pool.get('stock.move')
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for move in picking.move_lines:
                move_ids.append(move.id)
            if move_ids:
                move_obj.write(cr, uid, move_ids,
                               {'department_id': department_id},
                               context=context)
        return res

    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id,
                         context=None):
        invoice_vals = super(stock_picking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.department_id:
            invoice_vals['department_id'] = picking.department_id.id
        return invoice_vals


class stock_picking_in(orm.Model):

    _inherit = "stock.picking.in"

    def __init__(self, pool, cr):
        super(stock_picking_in, self).__init__(pool, cr)
        self._columns['department_id'] = \
            self.pool['stock.picking']._columns['department_id']

    def onchange_department_id(self, cr, uid, ids, department_id,
                               context=None):
        return self.pool.get('stock.picking').onchange_department_id(
            cr, uid, ids, department_id, context=context)


class stock_picking_out(orm.Model):

    _inherit = "stock.picking.out"

    def __init__(self, pool, cr):
        super(stock_picking_out, self).__init__(pool, cr)
        self._columns['department_id'] = \
            self.pool['stock.picking']._columns['department_id']

    def onchange_department_id(self, cr, uid, ids, department_id,
                               context=None):
        return self.pool.get('stock.picking').onchange_department_id(
            cr, uid, ids, department_id, context=context)