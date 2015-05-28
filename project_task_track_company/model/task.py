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


class Task(orm.Model):

    _inherit = 'project.task'

    def _get_stage_id_new(self, cr, uid, obj, context=None):
        stage_obj = self.pool['project.task.type']
        if not obj['stage_id']:
            return False
        stage = stage_obj.browse(cr, uid, obj['stage_id'][0], context=context)
        if stage.sequence <= 1:
            return True
        else:
            return False

    def _get_stage_id_not_new(self, cr, uid, obj, context=None):
        stage_obj = self.pool['project.task.type']
        if not obj['stage_id']:
            return False
        stage = stage_obj.browse(cr, uid, obj['stage_id'][0], context=context)
        if stage.sequence > 1:
            return True
        else:
            return False

    _track = {
        'stage_id': {
            # this is only an heuristics; depending on your particular stage configuration it may not match all 'new' stages
            'project.mt_task_new': _get_stage_id_new,
            'project.mt_task_stage': _get_stage_id_not_new,
        },
    }

    _columns = {
        'company_id': fields.many2one('res.company', 'Company',
                                      track_visibility='always'),
    }
