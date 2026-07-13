# -*- coding: utf-8 -*-

from unit3dup.common.trackers.itt import itt_data
from unit3dup.common.trackers.ptt import ptt_data
from unit3dup.common.trackers.sis import sis_data
from unit3dup.common.trackers.ast import ast_data

tracker_list = {'ITT': itt_data, 'SIS': sis_data, 'PTT': ptt_data, 'AST': ast_data}
