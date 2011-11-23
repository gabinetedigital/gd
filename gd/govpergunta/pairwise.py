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

class Pairwise:
    def __init__(self):
        self.user_id = str(uuid4())

    def get_pair(self):
        qid, pid = self.get_prompt_id()
        path = PROMPT_URL % (qid, pid, self.user_id)

        content = self.http_get(path)
        promptNode = parseString(content)
        leftNode =  promptNode.getElementsByTagName('left-choice-text')[0]
        rightNode =  promptNode.getElementsByTagName('right-choice-text')[0]
        leftjs = loads(leftNode.childNodes[0].data)
        rightjs = loads(rightNode.childNodes[0].data)
        c1 = Contrib.query.get(leftjs['id'])
        c2 = Contrib.query.get(rightjs['id'])
        return c1,c2

    def http_get(self, path):
        base64string = base64.encodestring('%s:%s' %
                                           (PAIRWISE_USERNAME,
                                            PAIRWISE_PASSWORD))[:-1]
        req = urllib2.Request(PAIRWISE_SERVER + path)
        req.add_header("Authorization", "Basic %s" % base64string)
        return  urllib2.urlopen(req).read()

    def get_prompt_id(self):
        total_questions = len(QUESTION_IDS)
        rnd = int(math.ceil(random.random() * 10))
        qid =  QUESTION_IDS[rnd % TOTAL_THEMES]
        path = QUESTION_URL % (qid, self.user_id)
        content = self.http_get(path)
        question = parseString(content)
        promptNode =  question.getElementsByTagName('picked_prompt_id')[0]
        return qid, promptNode.childNodes[0].data

    def vote(self):
        pass
