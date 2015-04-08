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

from openerp.tools.translate import _
from openerp.osv import fields, orm
from openerp import SUPERUSER_ID, tools


class purchase_order(orm.Model):

    _inherit = 'purchase.order'

    _columns = {
        'purchase_organization_id': fields.many2one('purchase.organization',
                                                    'Purchase Organization',
                                                    required=True),
    }

    def _get_default_purchase_organization(self, cr, uid, context=None):
        context = context or {}
        po_id = self.pool.get('res.users').purchase_organization_default_get(
            cr, uid, uid, context=context)
        context['purchase_organization_id'] = po_id
        return po_id

    _defaults = {
        'purchase_organization_id': lambda self, cr, uid, c: self.pool.get(
            'res.users').purchase_organization_default_get(cr, uid, uid,
                                                           context=c),
    }

    def onchange_purchase_organization(self, cr, uid, ids,
                                       purchase_organization_id,
                                       context=None):
        context = context or {}
        res = {}
        context['purchase_organization_id'] = purchase_organization_id
        return res


class purchase_order_line(orm.Model):
    _inherit = 'purchase.order.line'

    _columns = {
        'purchase_organization_id': fields.related(
            'order_id', 'purchase_organization_id', type='many2one',
            relation='purchase.organization', string='Purchase Organization',
            readonly=True),
    }