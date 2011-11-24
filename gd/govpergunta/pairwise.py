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


class Pairwise:
    def __init__(self):
        self.uid =  str(uuid4())

    def unpack_contrib(self, content):
        promptNode = parseString(content)
        leftNode =  promptNode.getElementsByTagName('left-choice-text')[0]
        rightNode =  promptNode.getElementsByTagName('right-choice-text')[0]
        leftjs = loads(leftNode.childNodes[0].data)
        rightjs = loads(rightNode.childNodes[0].data)
        c1 = Contrib.query.get(leftjs['id'])
        c2 = Contrib.query.get(rightjs['id'])
        return c1, c2

    def get_pair(self):
        self.current_qid, self.current_pid = self.choose_prompt()

        path = PROMPT_URL % (self.current_qid, self.current_pid, self.uid)
        content = self.http_get(path)
        c1, c2 = self.unpack_contrib(content)

        self.current_match_token = str(uuid4())

        return c1, c2, self.current_match_token

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

    def get_a_question_id(self):
        total_questions = len(QUESTION_IDS)
        rnd = int(math.ceil(random.random() * 10))
        return QUESTION_IDS[rnd % TOTAL_THEMES]

    def choose_prompt(self):
        qid =  self.get_a_question_id()
        path = QUESTION_URL % (qid, self.uid)
        content = self.http_get(path)
        question = parseString(content)
        promptNode =  question.getElementsByTagName('picked_prompt_id')[0]
        return qid, promptNode.childNodes[0].data

    def vote(self, direction, token):
        if token != self.current_match_token:
            raise Exception('Invalid token')

        path = VOTE_URL % (self.current_qid, self.current_pid)
        path = path + (VOTE_PARAMS % (self.uid, direction, self.uid))
        self.http_post(path)
