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


class account_move_line(orm.Model):
    _inherit = "account.move.line"

    def _check_segment_to_account(self, cr, uid, ids, context=None):
        for ml in self.browse(cr, uid, ids, context):
            if ml.company_segment_id and ml.account_id not in \
                    ml.company_segment_id.account_ids:
                return False
        return True

    _columns = {
        'company_segment_id': fields.many2one('company.segment',
                                              'Company segment',
                                              required=False),
        'account_ids': fields.many2many(
            'account.account', 'company_segment_account_account',
            'company_segment_id', 'account_id', 'Allowed accounts',
            required=False),
    }

    constraints = [(_check_segment_to_account,
                    'Segment can only be assigned to allowed accounts!',
                    ['company_segment_id', 'account_id'])]
