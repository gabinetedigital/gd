# -*- coding:utf-8 -*-
#
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Thiago Silva <thiago@metareload.com>
#   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4
import math
import random
import base64
import urllib2
from json import loads
from xml.dom.minidom import parseString

from gd import conf
from gd.model import Contrib


PAIRWISE_VERSION = '3'

QUESTION_IDS = [1, 2, 3, 4, 5]

QUESTION_URL = "/questions/%s.xml?" + \
    "visitor_identifier=%s&with_appearance=true&with_prompt=true"

PROMPT_URL = "/questions/%s/prompts/%s.xml?" + \
    "visitor_identifier=%s&with_prompt=true"

VOTE_URL = "/questions/%s/prompts/%s/vote.xml?"

VOTE_PARAMS = "vote[visitor_identifier]=%s&vote[direction]=%s&" + \
    "next_prompt[visitor_identifier]=%s"

SKIP_URL = "/questions/%s/prompts/%s/skip.xml?"

SKIP_PARAMS = "vote[visitor_identifier]=%s&skip[skip_reason]=other&" + \
    "skip[visitor_identifier]=%s&next_prompt[visitor_identifier]=%s"


def _request(path, data=None):
    """Abstraction for some bureaucracy of urllib

    We'll do a post instead of a get if the `data' attribute is not
    None. Just like urllib2 does.
    """
    base64string = base64.encodestring(
        '%s:%s' % (conf.PAIRWISE_USERNAME, conf.PAIRWISE_PASSWORD))[:-1]
    req = urllib2.Request(conf.PAIRWISE_SERVER + path)
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header('Content-Type', 'application/json')
    return urllib2.urlopen(req, data).read()


class Pairwise(object):
    """Binding to the Pairwise API provided by allourideas
    """
    def __init__(self):
        self.uid =  str(uuid4())
        self.prompts = {}
        self.votes = 0
        self.token = None # will be filled out when calling `get_pair()'
        self.question_seq = 0
        self.current_qid = None

    def _get_contrib(self, pos):
        return Contrib.query.get(self.prompts[self.current_qid][pos])

    def get_pair(self):
        self.init_prompt()
        self.token = str(uuid4())
        return {
            'left': self._get_contrib('left'),
            'right': self._get_contrib('right'),
            'token': self.token,
            'votes': self.votes,
        }

    def init_prompt(self):
        self.choose_question_id()
        if self.current_qid in self.prompts:
            return
        self.lookup_and_load_prompt()

    def choose_question_id(self):
        self.current_qid = QUESTION_IDS[self.question_seq % len(QUESTION_IDS)]
        self.question_seq += 1

    def lookup_and_load_prompt(self):
        path = QUESTION_URL % (self.current_qid, self.uid)
        question = parseString(_request(path))
        promptnode =  question.getElementsByTagName('picked_prompt_id')[0]
        pid = promptnode.childNodes[0].data
        self.load_prompt(pid)

    def load_prompt(self, pid):
        path = PROMPT_URL % (self.current_qid, pid, self.uid)
        content = _request(path)
        self.setup_prompt(content)

    def setup_prompt(self, content):
        pid, c1, c2 = self.unpack_prompt(content)
        self.prompts[self.current_qid] = {'pid': pid, 'left': c1, 'right': c2}

    def unpack_prompt(self, content):
        promptNode = parseString(content)
        pid = promptNode.getElementsByTagName('id')[0].childNodes[0].data
        leftNode =  promptNode.getElementsByTagName('left-choice-text')[0]
        rightNode =  promptNode.getElementsByTagName('right-choice-text')[0]
        leftjs = loads(leftNode.childNodes[0].data)
        rightjs = loads(rightNode.childNodes[0].data)
        return pid, leftjs['id'], rightjs['id']

    def vote(self, direction, token):
        if token != self.token:
            raise Exception('Invalid token')
        self.token = ''

        pid = self.prompts[self.current_qid]['pid']

        if direction == 'skip':
            path = SKIP_URL % (self.current_qid, pid)
            path = path + (SKIP_PARAMS % (self.uid, self.uid, self.uid))
        else:
            path = VOTE_URL % (self.current_qid, pid)
            path = path + (VOTE_PARAMS % (self.uid, direction, self.uid))

        content = _request(path, '')
        self.votes = self.votes + 1
        self.setup_prompt(content)
