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

from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class Product(orm.Model):
    _inherit = "product.product"

    _columns = {
        'max_sale_discount': fields.float(
            'Maximum Discount (%)',
            digits_compute=dp.get_precision('Discount'),
            help="Maximum sales discount defined for this product. Sales "
                 "quotations containing products where the discount of the "
                 "line exceeds the discount defined in the product will be "
                 "blocked.")
    }

    _defaults = {
        'max_sale_discount': 0.0
    }
