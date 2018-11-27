# ============================================================================
# FILE: editorconfig.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

import re
import os
from denite import util
from .base import Base
from ..kind.base import Base as BaseKind

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'editorconfig'
        self.kind = Kind(vim)

    def on_init(self, context):
        templates_path = self.vim.call('ueditorconfig#get_templates_path')

        if not os.path.isdir(templates_path):
            raise Exception('templates dir is not exists, please check plugin is install complete')

        templates_list = os.listdir(templates_path)
        templates_map = {}

        for template in templates_list:
            names = template.split('.')
            tpath = os.path.join(templates_path, template)
            if names[0] in templates_map:
                templates_map[names[0]]['source__paths'].append(tpath)
            else:
                templates_map[names[0]] = {
                        'word': names[0],
                        'source__paths': [tpath]
                    }

        self.__templates_list = [templates_map[template] for template in templates_map]

    def gather_candidates(self, context):
        return self.__templates_list

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'editorconfig'
        self.default_action = 'append'
        self.persist_actions = []
        self.redraw_actions = []

    def action_append(self, context):
        target = context['targets'][0]
        editorconfig = os.path.join(self.vim.call('getcwd'), '.editorconfig')
        if os.path.isfile(editorconfig):
            result = util.input(
                    self.vim, context, '%s exists! (append? Yes/No): ' % editorconfig, '')
        else:
            result = util.input(
                    self.vim, context, 'create %s ? Yes/No: ' % editorconfig, 'yes')
        if re.match('^yes$', result, re.I):
            templates = target['source__paths']
            content = '\n# create by https://github.com/iamcco/universal-editorconfig'
            for p in templates:
                content += '\n### %s ###\n' % os.path.split(p)[-1]
                content += open(p, 'r').read()
            f = open(editorconfig, 'a')
            f.write(content)
            f.close()
