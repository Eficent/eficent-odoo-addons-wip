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


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

    _columns = {
        'operating_unit_id': fields.many2one(
            'operating.unit', string='Operating Unit'),
    }

    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id,
                         context=None):
        invoice_vals = super(stock_picking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.operating_unit_id:
            invoice_vals['operating_unit_id'] = \
                picking.operating_unit_id.id
        return invoice_vals


class stock_picking_in(orm.Model):

    _inherit = "stock.picking.in"

    def __init__(self, pool, cr):
        super(stock_picking_in, self).__init__(pool, cr)
        self._columns['operating_unit_id'] = \
            self.pool['stock.picking']._columns['operating_unit_id']


class stock_picking_out(orm.Model):

    _inherit = "stock.picking.out"

    def __init__(self, pool, cr):
        super(stock_picking_out, self).__init__(pool, cr)
        self._columns['operating_unit_id'] = \
            self.pool['stock.picking']._columns['operating_unit_id']