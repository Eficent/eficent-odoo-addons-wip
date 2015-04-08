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

from openerp.osv import fields, orm


class product_pricelist_version(orm.Model):

    _inherit = 'product.pricelist.version'

    _columns = {
        'purchase_organization_id': fields.many2one('purchase.organization',
                                                    'Purchase Organization',
                                                    required=False),
    }

    def _check_date(self, cursor, user, ids, context=None):
        for pricelist_version in self.browse(cursor, user, ids, context=context):
            if not pricelist_version.active:
                continue
            where = []
            if pricelist_version.date_start:
                where.append("((date_end>='%s') or (date_end is null))" % (pricelist_version.date_start,))
            if pricelist_version.date_end:
                where.append("((date_start<='%s') or (date_start is null))" % (pricelist_version.date_end,))

            if pricelist_version.purchase_organization_id:
                where.append(("(purchase_organization_id='%s')" % (
                    pricelist_version.purchase_organization_id.id,)))
            cursor.execute('SELECT id ' \
                    'FROM product_pricelist_version ' \
                    'WHERE '+' and '.join(where) + (where and ' and ' or '')+
                        'pricelist_id = %s ' \
                        'AND active ' \
                        'AND id <> %s', (pricelist_version.pricelist_id.id,
                                         pricelist_version.id,))
            if cursor.fetchall():
                return False
        return True

    _constraints = [
        (_check_date, 'You cannot have 2 pricelist versions that overlap!',
            ['date_start', 'date_end'])
    ]

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        if context is None:
            context = {}
        res = []
        ids = super(product_pricelist_version, self).search(
            cr, uid, args, offset, limit, order, context=context,
            count=count)
        if 'purchase_organization_id' in context \
                and context['purchase_organization_id']:
            for pricelist_version in self.browse(cr, uid, ids,
                                                 context=context):
                if pricelist_version.purchase_organization_id.id == \
                        context['purchase_organization_id']:
                    res.append(pricelist_version.id)
        else:
            res = ids
        return res
