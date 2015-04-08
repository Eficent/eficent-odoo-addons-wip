# -*- coding: utf-8 -*-
##############################################################################
#
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

from openerp.tools.translate import _
from openerp.osv import fields, orm


class analytic_resource_plan_line(orm.Model):

    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'task_id': fields.many2one('project.task', 'Task', required=False,
                                   ondelete='cascade',
                                   readonly=True),
    }

    def create(self, cr, uid, vals, *args, **kwargs):
        context = kwargs.get('context', {})
        task_obj = self.pool.get('project.task')

        if 'task_id' in vals and vals['task_id']:
            task = task_obj.browse(cr, uid, vals['task_id'], context=context)
            vals['account_id'] = \
                task.project_id \
                and task.project_id.analytic_account_id \
                and task.project_id.analytic_account_id.id \
                or False
        return super(analytic_resource_plan_line, self).create(cr, uid, vals, *args, **kwargs)


analytic_resource_plan_line()
