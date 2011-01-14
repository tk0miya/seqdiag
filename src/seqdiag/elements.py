#!bin/py
# -*- coding: utf-8 -*-

import re
import sys
from blockdiag.elements import *
from blockdiag.utils.XY import XY

DiagramNodeBase = DiagramNode


class DiagramNode(DiagramNodeBase):
    def __init__(self, id):
        DiagramNodeBase.__init__(self, id)

        self.activity = []
        self.activities = []

    def activate(self, height, index):
        if len(self.activity) <= index:
            self.activity.insert(index, [])

        if len(self.activity[index]) > 0 and \
           self.activity[index][-1] != height - 1:
            self.deactivate(index)

        self.activity[index].append(height)

    def deactivate(self, index=None):
        if index is None:
            for i in range(len(self.activity)):
                self.deactivate(i)
            return

        if self.activity[index]:
            self.activities.append(self.activity[index])

        self.activity[index] = []


DiagramEdgeBase = DiagramEdge


class DiagramEdge(DiagramEdgeBase):
    return_label = None

    def __init__(self, node1, node2):
        DiagramEdgeBase.__init__(self, node1, node2)

        self.height = 1
        self.y = 0
        self.async = False
        self.diagonal = False
        self.return_label = ''

    def setAttributes(self, attrs):
        attrs = list(attrs)
        for attr in list(attrs):
            value = unquote(attr.value)

            if attr.name == 'return':
                self.return_label = value
                attrs.remove(attr)
            elif attr.name == 'diagonal':
                self.diagonal = True
                self.height = 1.5
                attrs.remove(attr)
            elif attr.name == 'async':
                self.dir = 'forward'
                attrs.remove(attr)
            elif attr.name == 'dir':
                dir = value.lower()
                if dir in ('back', 'both', 'forward'):
                    self.dir = dir
                elif dir == '=>':
                    self.dir = 'both'
                elif dir in ('->', '->>', '-->', '-->>'):
                    self.dir = 'forward'

                    if re.search('--', dir):
                        self.style = 'dashed'
                    else:
                        self.style = None

                    if re.search('>>', dir):
                        self.async = True
                    else:
                        self.async = False
                elif dir in ('<-', '<<-', '<--', '<<--'):
                    self.dir = 'back'

                    if re.search('--', dir):
                        self.style = 'dashed'
                    else:
                        self.style = None

                    if re.search('<<', dir):
                        self.async = True
                    else:
                        self.async = False
                else:
                    msg = "WARNING: unknown edge dir: %s\n" % dir
                    sys.stderr.write(msg)

                attrs.remove(attr)

        DiagramEdgeBase.setAttributes(self, attrs)