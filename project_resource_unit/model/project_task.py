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


class project_task(orm.Model):
    
    _inherit = 'project.task'

    _columns = {
        'product_quantity': fields.float('End product quantity',
                                         required=False),
        'product_uom_id': fields.many2one('product.uom', 'End product UoM',
                                          required=False),
        'resource_unit_ids': fields.one2many(
            'project.task.resource.unit', 'task_id', 'Resource units',
            ondelete='cascade'),
        'resource_plan_line_ids': fields.one2many(
            'analytic.resource.plan.line', 'task_id', 'Resource plan lines',
            ondelete='cascade', readonly=True),
    }

    def write(self, cr, uid, ids, vals, context=None):
        """
        When task gets updated, handle the associated resource plan lines.
        """
        if context is None:
            context = {}
        rpl_obj = self.pool.get('analytic.resource.plan.line')

        if isinstance(ids, (long, int)):
            ids = [ids]

        for task in self.browse(cr, uid, ids, context=context):
            if 'project_id' in vals and task.resource_plan_line_ids:
                rpl_ids = []
                for rpl in task.resource_plan_line_ids:
                    rpl_ids.append(rpl.id)
                rpl_obj.write(
                    cr, uid, rpl_ids,
                    {'account_id': task.project_id.analytic_account_id.id},
                    context=context)
            if 'product_quantity' in vals:
                for runit in task.resource_unit_ids:
                    total_quantity = \
                        vals['product_quantity'] * runit.unit_quantity
                    rpl_obj.write(
                        cr, uid, [runit.resource_plan_line_id.id],
                        {'unit_amount': total_quantity}, context=context)

        return super(project_task, self).write(cr, uid, ids, vals, context)


class project_task_resource_unit(orm.Model):
    _name = "project.task.resource.unit"
    _description = "Resource Unit"

    def _get_totals(self, cr, uid, ids, name, args, context=None):
        res = dict.fromkeys(ids, False)
        task_obj = self.pool.get('project.task')
        for record in self.browse(cr, uid, ids, context=context):
            task = task_obj.browse(cr, uid, record.task_id.id, context=context)
            total_quantity = task.product_quantity * record.unit_quantity
            total_cost = total_quantity * record.unit_cost
            res[record.id] = {
                'total_quantity': total_quantity,
                'total_cost': total_cost,
                'cost': record.unit_quantity*record.unit_cost,
            }
        return res

    _columns = {
        'task_id': fields.many2one(
            'project.task', 'Task', ondelete='cascade', required=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True),
        'uom_id': fields.related('product_id', 'uom_id', string="UoM",
                                 type='many2one', relation='product.uom',
                                 readonly=True),
        'unit_cost': fields.related('product_id', 'standard_price',
                                    string='Unit cost', type='float',
                                    store=False, readonly=True),
        'unit_quantity': fields.float('Unit quantity'),
        'cost': fields.function(_get_totals, type='float',
                                multi='totals', string='Cost'),
        'total_cost': fields.function(_get_totals, type='float',
                                      multi='totals', string='Total cost'),
        'total_quantity': fields.function(_get_totals, type='float',
                                          multi='totals',
                                          string='Total quantity'),
        'resource_plan_line_id': fields.many2one(
            'analytic.resource.plan.line', 'Related Resource Plan Line',
            ondelete='set null'),
    }

    def _create_resource_plan_lines(self, cr, uid, vals, context):
        """Create the resource plan line from worcenter actual work"""
        rpl_obj = self.pool.get('analytic.resource.plan.line')
        task_obj = self.pool.get('project.task')
        product_obj = self.pool.get('product.product')
        vals_line = {}
        task = task_obj.browse(cr, uid, vals['task_id'], context=context)
        if task.project_id:
            vals_line['account_id'] = task.project_id.analytic_account_id.id
        else:
            return False
        vals_line['name'] = task.name
        vals_line['product_id'] = vals['product_id']
        product = product_obj.browse(cr, uid, vals['product_id'],
                                     context=context)
        vals_line['product_uom_id'] = product.uom_id.id
        vals_line['unit_amount'] = \
            vals['unit_quantity'] * task.product_quantity
        vals_line['task_id'] = vals['task_id']
        return rpl_obj.create(cr, uid, vals=vals_line,
                              context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """
        When resource unit gets updated, handle its resource plan line.
        """
        if context is None:
            context = {}
        rpl_obj = self.pool.get('analytic.resource.plan.line')
        task_obj = self.pool.get('project.task')
        product_obj = self.pool.get('product.product')

        if isinstance(ids, (long, int)):
            ids = [ids]

        for resource_unit in self.browse(cr, uid, ids, context=context):
            line_id = resource_unit.resource_plan_line_id
            if not line_id:
                # if a record is deleted from resource plan line,
                # the line_id will become
                # null because of the foreign key on-delete=set null
                continue
            vals_line = {}
            if 'task_id' in vals:
                task_id = vals['task_id']
                vals_line['task_id'] = task_id
            else:
                task_id = resource_unit.task_id.id

            task = task_obj.browse(cr, uid, task_id,
                                   context=context)
            if 'product_id' in vals:
                product = product_obj.browse(cr, uid, vals['product_id'],
                                             context=context)
                vals_line['product_id'] = vals['product_id']
                vals_line['product_uom_id'] = product.uom_id.id
            if 'unit_quantity' in vals:
                vals_line['unit_amount'] = \
                    vals['unit_quantity']*task.product_quantity
            if 'task_id' in vals:
                vals_line['task_id'] = task_id
                vals_line['name'] = task.name
                if task.project_id:
                    vals_line['account_id'] = \
                        task.project_id.analytic_account_id.id
                else:
                    continue

            if vals_line:
                rpl_obj.write(cr, uid, [line_id.id], vals_line,
                              context=context)

        return super(project_task_resource_unit, self).write(
            cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, *args, **kwargs):
        rpl_obj = self.pool.get('analytic.resource.plan.line')
        rpl_ids = []
        for resource_unit in self.browse(cr, uid, ids):
            if resource_unit.resource_plan_line_id:
                rpl_ids.append(
                    resource_unit.resource_plan_line_id.id)
        if rpl_ids:
            rpl_obj.unlink(cr, uid, rpl_ids, *args, **kwargs)
        return super(project_task_resource_unit, self).unlink(
            cr, uid, ids, *args, **kwargs)

    def create(self, cr, uid, vals, *args, **kwargs):
        context = kwargs.get('context', {})
        if not context.get('no_resource_plan_line_entry', False):
            vals['resource_plan_line_id'] = \
                self._create_resource_plan_lines(cr, uid, vals,
                                                 context=context)
        return super(project_task_resource_unit, self).create(
            cr, uid, vals, *args, **kwargs)