from uuid import uuid4
import math
import random
import base64
import urllib2
from json import loads
from xml.dom.minidom import parseString
from gd.model import Contrib

PAIRWISE_SERVER = "http://localhost:4000"
PAIRWISE_USERNAME = 'pairuser'
PAIRWISE_PASSWORD = 'pairpass'

QUESTION_IDS = [1,2,3,4,5]
TOTAL_THEMES = 5

QUESTION_URL = "/questions/%s.xml?visitor_identifier=%s&with_appearance=true&with_prompt=true"

PROMPT_URL = "/questions/%s/prompts/%s.xml?visitor_identifier=%s&with_prompt=true";

VOTE_URL = "/questions/%s/prompts/%s/vote.xml?"
VOTE_PARAMS = "vote[visitor_identifier]=%s&vote[direction]=%s&next_prompt[visitor_identifier]=%s"

SKIP_URL = "/questions/%s/prompts/%s/skip.xml?"
SKIP_PARAMS = "vote[visitor_identifier]=%s&skip[skip_reason]=other&skip[visitor_identifier]=%s&next_prompt[visitor_identifier]=%s";


class Pairwise:
    def __init__(self):
        self.uid =  str(uuid4())
        self.prompts = {}
        self.votes = 0

    def left_contrib(self):
        return Contrib.query.get(self.prompts[self.current_qid]['left'])

    def right_contrib(self):
        return Contrib.query.get(self.prompts[self.current_qid]['right'])

    def http_get(self, path):
        base64string = base64.encodestring('%s:%s' %
                                           (PAIRWISE_USERNAME,
                                            PAIRWISE_PASSWORD))[:-1]
        req = urllib2.Request(PAIRWISE_SERVER + path)
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header('Content-Type', 'application/json')
        return  urllib2.urlopen(req).read()

    def http_post(self, path):
        base64string = base64.encodestring('%s:%s' %
                                           (PAIRWISE_USERNAME,
                                            PAIRWISE_PASSWORD))[:-1]
        req = urllib2.Request(PAIRWISE_SERVER + path)
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header('Content-Type', 'application/json')
        return  urllib2.urlopen(req, '').read()

    def get_pair(self):
        self.init_prompt()
        self.token = str(uuid4())
        return self.left_contrib(), self.right_contrib(), self.token, self.votes

    def init_prompt(self):
        self.choose_question_id()
        if self.current_qid in self.prompts:
            return
        self.lookup_and_load_prompt()

    def lookup_and_load_prompt(self):
        self.lookup_prompt_id()
        self.load_prompt()

    def choose_question_id(self):
        total_questions = len(QUESTION_IDS)
        rnd = int(math.ceil(random.random() * 10))
        #self.current_qid = QUESTION_IDS[rnd % TOTAL_THEMES]
        self.current_qid = QUESTION_IDS[1]

    def lookup_prompt_id(self):
        path = QUESTION_URL % (self.current_qid, self.uid)
        content = self.http_get(path)
        question = parseString(content)
        promptNode =  question.getElementsByTagName('picked_prompt_id')[0]
        self.current_pid = promptNode.childNodes[0].data

    def load_prompt(self):
        path = PROMPT_URL % (self.current_qid, self.current_pid, self.uid)
        content = self.http_get(path)
        self.setup_prompt(content)

    def setup_prompt(self, content):
        c1, c2 = self.unpack_contrib(content)
        self.prompts[self.current_qid] = {'left': c1, 'right': c2}

    def unpack_contrib(self, content):
        promptNode = parseString(content)
        leftNode =  promptNode.getElementsByTagName('left-choice-text')[0]
        rightNode =  promptNode.getElementsByTagName('right-choice-text')[0]
        leftjs = loads(leftNode.childNodes[0].data)
        rightjs = loads(rightNode.childNodes[0].data)
        return leftjs['id'], rightjs['id']

    def vote(self, direction, token):
        if token != self.token:
            raise Exception('Invalid token')
        self.token = ''

        if direction == 'skip':
            path = SKIP_URL % (self.current_qid, self.current_pid)
            path = path + (SKIP_PARAMS % (self.uid, self.uid, self.uid))
        else:
            path = VOTE_URL % (self.current_qid, self.current_pid)
            path = path + (VOTE_PARAMS % (self.uid, direction, self.uid))

        try:
            content = self.http_post(path)
            self.votes = self.votes + 1
            self.setup_prompt(content)
        except:
            # broken connection, unable to find question/choice/prompt
            # also handling 'rapid fire' vote errors
            print "UOPS!"
            self.lookup_and_load_prompt()
