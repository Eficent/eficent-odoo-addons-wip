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


class res_users(orm.Model):

    _inherit = 'res.users'

    _columns = {
        'purchase_organization_ids': fields.many2many(
            'purchase.organization', 'purchase_organization_users_rel',
            'user_id', 'poid',
            'Purchase organizations'),
        'default_purchase_organization_id': fields.many2one(
            'purchase.organization', 'Default Purchase Organization')
    }

    def purchase_organization_default_get(self, cr, uid, uid2, context=None):
        if not uid2:
            uid2 = uid
        user = self.pool.get('res.users').browse(cr, uid, uid2, context)
        return user.default_purchase_organization_id.id or False