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

from openerp.osv import fields, orm
from openerp.tools.translate import _
import time


class Project(orm.Model):
    _inherit = "project.project"

    def update_progress_measurement(self, cr, uid, ids,
                                    context=None):
        meas_type_obj = self.pool['progress.measurement.type']
        meas_obj = self.pool['project.progress.measurement']

        for project in self.browse(cr, uid, ids, context=context):
            account_id = project.analytic_account_id.id
            # Look for the total cost associated to tasks completed
            cr.execute("""SELECT sum(PL.amount)
            FROM analytic_resource_plan_line as RPL
            JOIN account_analytic_line_plan PL
            ON PL.resource_plan_id = RPL.id
            JOIN project_task T
            ON RPL.task_id = T.id
            WHERE RPL.account_id = %s
            AND T.state = 'done'""", (account_id, ))
            res = cr.fetchone()
            total_done = 0.0
            if res:
                total_done = res[0]

            cr.execute("""SELECT sum(PL.amount)
            FROM analytic_resource_plan_line as RPL
            JOIN account_analytic_line_plan PL
            ON PL.resource_plan_id = RPL.id
            JOIN project_task T
            ON RPL.task_id = T.id
            WHERE RPL.account_id = %s
            AND T.state NOT IN ('cancel', 'done')""",
                       (account_id, ))
            res = cr.fetchone()
            total_open = 0.0
            if res:
                total_open = res[0]

            # Determine the progress
            total = total_open + total_done
            try:
                progress_value = total_done / total * 100
            except ZeroDivisionError:
                progress_value = 0.0

            # Search default progress measurement
            meas_types = meas_type_obj.search(
                cr, uid, [('is_default', '=', True)],
                context=context)
            if not meas_types:
                raise orm.except_orm(_('Error!'),
                                     _('No default progress measurement type '
                                       'defined.'))
            meas_type = meas_type_obj.browse(cr, uid, meas_types[0],
                                             context=context)
            progress_value -= progress_value % meas_type.precision
            current_date = time.strftime('%Y-%m-%d')
            meas_vals = {
                'project_id': project.id,
                'communication_date': current_date,
                'progress_measurement_type': meas_type.id,
                'value': progress_value,
            }
            # Search for an existing progress measurement for current date
            meas_ids = meas_obj.search(
                cr, uid, [('project_id', '=', project.id),
                          ('communication_date', '=', current_date),
                          ('progress_measurement_type', '=', meas_types[0])],
                context=context)
            # Create or update today's progress measurement
            if meas_ids:
                meas_obj.write(cr, uid, meas_ids, meas_vals, context=context)
            else:
                meas_obj.create(cr, uid, meas_vals, context=context)


class Task(orm.Model):

    _inherit = "project.task"

    def write(self, cr, uid, ids, vals, context=None):
        project_obj = self.pool['project.project']
        res = super(Task, self).write(cr, uid, ids, vals, context=context)
        if vals.get('stage_id', False):
            for task in self.browse(cr, uid, ids, context=context):
                if task.project_id:
                    project_obj.update_progress_measurement(
                        cr, uid, [task.project_id.id], context=context)

        return res
