# -*- coding: latin-1 -*-
from jira import JIRA
from datetime import timedelta, datetime
import JiraOptions
from io import StringIO
import util
# import psycopg2
import pandas as pd

def jiraconetion():
    """Connection with Jira server"""
    jira_options = {
        'server': JiraOptions.SERVER, 'verify': False
    }
    server_jira = JIRA(jira_options, basic_auth=(JiraOptions.USERNAME, JiraOptions.PASSWORD), max_retries=10)
    return server_jira


class IssueJira(object):
    """
    Parâmetros Esperados
    issue, project, issue_type, summary, opened_date, status, objservation
    """
    def __init__(self, issue, project=None, issue_type=None, summary=None
                 , opened_date=None, status='optional', objservation=None):
        self.issue = issue
        self.project = project
        self.issue_type = issue_type
        self.summary = summary
        self.opened_date = opened_date
        self.status = status
        self.observation = objservation
        self.artefact = []

    def appendartefact(self, artefact):
        """
        Apend string in list named artefact
        :param artefact: Receive a string value
        :return: Nothing, it's a void method
        """
        self.artefact.append(artefact)

    def returnissue(self):
        """
        Get values of a issue from Jira Rest API
        If issue not exists in Jira Rest API methods return None for all fields
        """
        try:
            issue_fields = jiraconetion().issue(self.issue)  # Check if issue exists
            self.project = issue_fields.fields.project
            self.issue_type = issue_fields.fields.issuetype
            self.summary = issue_fields.fields.summary
            self.opened_date = issue_fields.fields.customfield_11221
            self.status = issue_fields.fields.status
        except Exception as e:
            print(e)
            self.issue = None
            self.project = None
            self.issue_type = None
            self.summary = None
            self.opened_date = None
            self.status = None

    def updatestatus(self):
        """
        Update a issue status, but is necessary identify all status that a users can use
        Method for check a status
            jira = conexaoJira()
            issue = jira.issue('PEE-27')
            transitions = jira.transitions(issue)
            for i in transitions:
                print(i)
        :return:  Nothing, it's a void method
        """
        self.returnissue()
        if self.issue is not None:
            jiraconetion().transition_issue(self.issue, 151)


class IssueJiraSupport(IssueJira):
    """
    Parent class
    Parâmetros Esperados IssueJira class
        issue, project, issue_type, summary, opened_date, status, objservation
    Parâmetros Esperados IssueJiraSupport class
        requester, complexity, service_order, necessity, necessity_code, priority
    """
    def __init__(self, issue, project=None, issue_type=None,
                 summary=None, opened_date=None, status='optional', objservation=None
                 , requester=None, complexity=None, service_order=None, necessity=None
                 , necessity_code=None, priority=None):
        super().__init__(issue, project, issue_type, summary, opened_date, status, objservation)
        self.priority = priority
        self.requester = requester
        self.complexity = complexity
        self.service_order = service_order
        self.necessity = necessity
        self.necessity_code = necessity_code
        self.thematic = []

    def appendthematic(self, thematics):
        """
        Append a string value into thematic field class
        :param thematics: String value
        :return: Nothing, it's a void method
        """
        for value in thematics:
            dictionary = {'value': value}
            self.thematic.append(dictionary)

    def returnissue(self):
        """
        Get values of a issue from Jira Rest API
        If issue not exists in Jira Rest API methods return None for all fields
        """
        try:
            issue_fields = jiraconetion().issue(self.issue)
            self.project = issue_fields.fields.project
            self.issue_type = issue_fields.fields.issuetype
            self.summary = issue_fields.fields.summary
            self.opened_date = issue_fields.fields.customfield_11221
            self.status = issue_fields.field.status
            self.issue = issue_fields.field.issue
            self.priority = issue_fields.field.customfield_12501
            self.requester = issue_fields.field.customfield_12504
            self.complexity = issue_fields.field.customfield_11302
            self.service_order = issue_fields.field.customfield_12506
            self.necessity = issue_fields.field.customfield_12512.value
            self.necessity_code = issue_fields.field.customfield_12512.child.value
        except BaseException as e:
            self.project = None
            self.issue_type = None
            self.summary = None
            self.opened_date = None
            self.status = None
            self.issue = None
            self.priority = None
            self.requester = None
            self.complexity = None
            self.service_order = None
            self.necessity = None
            self.necessity_code = None

    def returjsonaddissue(self):
        """
        Return a json dict with all necessary fields filled in for add method.
        If issue name don't exists, return a json dict empty
        :return: Json dict
        """
        if checkmandatoryfields is True:
            issue_dict = {
                'project': self.project,
                'summary': self.summary,
                'issuetype': self.issue_type,
                'customfield_12504': self.requester,  # requester
                'customfield_12501': {'value': self.priority},  # priority
                'customfield_11302': {'value': self.complexity},  # complexity
                'customfield_12506': self.service_order,  # service order
                'customfield_11221': self.opened_date,  # issue open
                'customfield_12505': self.observation,  # observation
                'customfield_12512': {'value': self.necessity, 'child': {'value': self.necessity_code}},  # necessity
                'customfield_12608': self.thematic,  # thematic - value=text, child=code
            }
        else:
            issue_dict = {}
        return issue_dict


class IssueJiraSupportChild(IssueJira):
    """
    Parent class
    Parâmetros Esperados IssueJira class
        issue, project, issue_type, summary, opened_date, status, objservation
    Parâmetros Esperados IssueJiraSupportChuild class
         parent, technical_profile, activity, activity_code
    """
    def __init__(self, issue, project, issue_type, summary, opened_date, status, objservation, parent,
                 technical_profile, activity, activity_code):
        super().__init__(issue, project, issue_type, summary, opened_date, status, objservation)
        self.technical_profile = technical_profile
        self.parent = parent
        self.activity = activity
        self.activity_code = activity_code

    def returnissue(self):
        try:
            issue_fields = jiraconetion().issue(self.issue)
            self.issue = issue_fields.field.status
            self.project = issue_fields.fields.project
            self.issue_type = issue_fields.fields.issuetype
            self.summary = issue_fields.fields.summary
            self.opened_date = issue_fields.fields.customfield_11221
            self.status = issue_fields.field.status
            self.parent = issue_fields.field.parent
        except Exception:
            self.issue = None
            self.project = None
            self.issue_type = None
            self.summary = None
            self.opened_date = None
            self.status = None
            self.parent = None

    def returjsonaddissue(self):
        issue_dict = {
            'parent': self.parent,
            'project': self.project,
            'summary': self.summary,
            'issuetype': self.issue_type,
            'customfield_12505': self.observation,  # observation
            'customfield_11221': self.opened_date,  # issue open
            'customfield_12511': self.technical_profile,  # techinical profile
            'customfield_12513': {'value': self.activity, 'child': {'value': self.activity_code}},  # activity - value=text, child=code
        }
        return issue_dict


class Worklog(object):
    def __init__(self, issue_name, author, date_start, time_spent_seconds):
        self.worklog = []
        self.issue_name = issue_name
        self.author = author
        self.date_start = date_start
        self.time_spent_seconds = time_spent_seconds

    def appendworklog(self, author, date_start, time_spent_seconds):
        date_end = date_start + timedelta(hours=time_spent_seconds)
        self.worklog.append([author, date_start, date_end, time_spent_seconds])


def checkmandatoryfields(object):
    """
    Check all atributes in class.
    """
    check_return = 0
    for i in object.__dict__:
        if getattr(object, i) is not None:
            check_return += 1
    if object.__dict__.__len__() != check_return:
        return False
    else:
        return True


def addissue(issue_dict):
    """
        #Parent
        #issueparent = IssueJiraSupportChild(
        #                                       issue='New'
        #                                     , priority='Emergencia' #Emergencia, Normal
        #                                     , requester='jansen'
        #                                     , complexity='Media' #Baixa, Alta, Media, None
        #                                     , service_order='OS1'
        #                                     , necessity='Realizar Roteiro e Teste de Dados'
        #                                     , necessity_code='BIN016'
        #                                     , project='PEE'
        #                                     , objservation = 'OBS'
        #                                     , issue_type='Sustentação AD'
        #                                     , opened_date=util.returndatetime('2018-06-05 01:01:01')[3]
        #                                     , summary='sumario')
        #Child
        #issueparent = IssueJiraSupportParent(
        #                                       issue='New'
        #                                     , priority='Emergencia' #Emergencia, Normal
        #                                     , requester='jansen'
        #                                     , complexity='Media' #Baixa, Alta, Media, None
        #                                     , service_order='OS1'
        #                                     , necessity='Realizar Roteiro e Teste de Dados'
        #                                     , necessity_code='BIN016'
        #                                     , project='PEE'
        #                                     , issue_type='Sustentação AD'
        #                                     , opened_date=util.returndatetime('2018-06-05 01:01:01')[3]
        #                                     , summary='sumario')


        #issueparent.appendthematic(['ENEM', 'RAIS'])
        #jsonreturn = issueparent.returjsonaddissue()
        #print(jsonreturn)
        #newissue = addissue(jsonreturn)
    """
    return jiraconetion().create_issue(fields=issue_dict)



#def addaattachment(issue):
#    # upload file from `/some/path/attachment.txt`
#    jiraconetion().add_attachment(issue=issue, attachment='/some/path/attachment.txt')
#
#    # read and upload a file (note binary mode for opening, it's important):
#    with open('/some/path/attachment.txt', 'rb') as f:
#        jiraconetion().add_attachment(issue=issue, attachment=f)
#
#    # attach file from memory (you can skip IO operations). In this case you MUST provide `filename`.
#    attachment = StringIO.StringIO()
#    attachment.write()
#    jiraconetion().add_attachment(issue=issue, attachment=attachment, filename='content.txt')

#issueparent = IssueJiraSupportParent(
#                                       priority='Emergencia' #Emergencia, Normal
#                                     , requester='jansen'
#                                     , complexity='Media' #Baixa, Alta, Media, None
#                                     , service_order='OS1'
#                                     , necessity='Realizar Roteiro e Teste de Dados'
#                                     , necessity_code='BIN016'
#                                     , project='PEE'
#                                     , issue_type='Sustentação AD'
#                                     , opened_date=util.returndatetime('2018-06-05 01:01:01')[3]
#                                     , summary='sumario')

#issueparent.appendthematic(['ENEM', 'RAIS'])
#jsonreturn = issueparent.returjsonaddparentissue()
#print(jsonreturn)
#newissue = addissue(jsonreturn)


issue = IssueJiraSupport(issue='New'
                       , priority='Emergencia' #Emergencia, Normal
                        , requester='jansen'
                        , complexity='Media' #Baixa, Alta, Media, None
                        , service_order='OS1'
                        , necessity='Realizar Roteiro e Teste de Dados'
                        , necessity_code='BIN016'
                        , project='PEE'
                        , objservation = 'OBS'
                        , issue_type='Sustentação AD'
                        , opened_date=util.returndatetime('2018-06-05 01:01:01')[3]
                        , summary='sumario')
print(checkmandatoryfields(issue))


"""
def addworklog(issue):
    jiraconetion().add_worklog(user=self.worklog[0]
                               , issue=self.name
                               , started=self.worklog[1]
                               , timeSpent=self.worklog[3])
"""


