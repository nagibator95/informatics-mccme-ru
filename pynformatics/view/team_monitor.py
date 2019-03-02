import requests
from pyramid.encode import urlencode
from pyramid.view import view_config
from pynformatics.model import User, EjudgeContest, Run, Comment, EjudgeProblem, Problem, Statement
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.view.utils import *
import sys, traceback
#import jsonpickle, demjson
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
import transaction
#import jsonpickle, demjson
import json
from pynformatics.models import DBSession
#from webhelpers.html import *
from xml.etree.ElementTree import ElementTree

@view_config(route_name='team_monitor.get', renderer='string')
def get_team_monitor(request):
    try:
        statement_id = int(request.matchdict['statement_id'])
    
        user = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        statement = DBSession.query(Statement).filter(Statement.id == statement_id).first()
#        checkCapability(request)
        res = ""
        for k, v in statement.problems.items():
            res = res + "[" + str(k) + "] " + v.name
        return statement.name + " " + res
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


class MonitorApi:
    def __init__(self, request):
        self.request = request
        self.view_name = 'Monitor'

    @view_config(route_name='monitor_create', request_method='GET')
    def get_monitor(self):
        internal_link = urlencode(self.request.params)

        try:
            data = self._get_monitor(internal_link)
        except Exception as e:
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

        if data is None:
            return {"result": "error", "message": 'Something was wrong'}

        return data

    @classmethod
    def _get_monitor(cls, internal_link) -> dict:
        url = 'http://localhost:12346/monitor?{}'.format(internal_link)
        try:
            resp = requests.get(url, timeout=30)
            context = resp.json()
        except Exception as e:
            print('Request to :12346 failed!')
            raise
        return context
