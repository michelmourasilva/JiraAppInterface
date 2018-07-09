# -*- coding: latin-1 -*-
from jira import JIRA
from datetime import timedelta
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
    """
    def __init__(self, issue='new', project=None, issue_type=None, summary=None
                 , opened_date=None, status='optional', observation=None):
        self.issue = issue
        self.project = project
        self.issue_type = issue_type
        self.summary = summary
        self.opened_date = util.returndatetime(opened_date)[3]
        self.status = status
        self.observation = observation
        self.artifact = []

    def append_artifact(self, artifact):
        """
        Apend string in list named artifact
        :param artifact: Receive a string value
        :return: Nothing, it's a void method
        """
        self.artifact.append(artifact)

    def return_issue(self):
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

    def update_status(self):
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
        self.return_issue()
        if self.issue is not None:
            jiraconetion().transition_issue(self.issue, 151)


class IssueJiraSupport(IssueJira):
    """
    """
    def __init__(self, issue, project=None, issue_type=None,
                 summary=None, opened_date=None, status='optional', observation=None
                 , requester=None, complexity=None, service_order=None, necessity=None
                 , necessity_code=None, priority=None):
        super().__init__(issue, project, issue_type, summary, opened_date, status, observation)
        self.priority = priority
        self.requester = requester
        self.complexity = complexity
        self.service_order = service_order
        self.necessity = necessity
        self.necessity_code = necessity_code
        self.thematic = []

    def append_thematic(self, thematics):
        """
        Append a string value into thematic field class
        :param thematics: String value
        :return: Nothing, it's a void method
        """
        for value in thematics:
            dictionary = {'value': value}
            self.thematic.append(dictionary)

    def return_issue(self):
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
            self.status = issue_fields.fields.status
            self.priority = issue_fields.fields.customfield_12501
            self.requester = issue_fields.fields.customfield_12504
            self.complexity = issue_fields.fields.customfield_11302
            self.service_order = issue_fields.fields.customfield_12506
            self.necessity = issue_fields.fields.customfield_12512.value
            self.necessity_code = issue_fields.fields.customfield_12512.child.value
            for list_thematic in issue_fields.fields.customfield_12608:
                self.append_thematic(list_thematic.value)
        except BaseException as e:
            print(e)
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

    def return_json_add_issue(self):
        """
        Return a json dict with all necessary fields filled in for add method.
        If issue name don't exists, return a json dict empty
        :return: Json dict
        """
        if check_mandatory_fields(self) is True:
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
    def __init__(self, issue, project, issue_type, summary, opened_date, status, observation, parent,
                 technical_profile, activity, activity_code):
        super().__init__(issue, project, issue_type, summary, opened_date, status, observation)
        self.technical_profile = technical_profile
        self.parent = parent
        self.activity = activity
        self.activity_code = activity_code

    def return_issue(self):
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

    def return_json_add_issue(self):
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

    def append_worklog(self, author, date_start, time_spent_seconds):
        date_end = date_start + timedelta(hours=time_spent_seconds)
        self.worklog.append([author, date_start, date_end, time_spent_seconds])


def check_mandatory_fields(object_jira):
    """
    Check all atributes in class.
    """
    check_return = 0
    for i in object_jira.__dict__:
        field_value = getattr(object_jira, i)
        if field_value is not None:
            check_return += 1
        else:
            print('Parameter {0} is None.'.format(i))
    if object_jira.__dict__.__len__() != check_return:
        print('There are a {0} fields in with value None'.format(object_jira.__dict__.__len__()-check_return))
        return False
    else:
        return True


def add_issue(issue_dict):
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


#issue = IssueJiraSupport(issue='New'
#                       , priority='Emergencia' #Emergencia, Normal
#                        , requester='jansen'
#                        , complexity='Media' #Baixa, Alta, Media, None
#                        , service_order='OS1'
#                        , necessity='Realizar Roteiro e Teste de Dados'
#                        , necessity_code='BIN016'
#                        , project='PEE'
#                        , objservation = 'OBS'
#                        , issue_type='Sustentação AD'
#                        , opened_date=util.returndatetime('2018-06-05 01:01:01')[3]
#                        , summary='sumario')
#print(checkmandatoryfields(issue))
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
"""
def addworklog(issue):
    jiraconetion().add_worklog(user=self.worklog[0]
                               , issue=self.name
                               , started=self.worklog[1]
                               , timeSpent=self.worklog[3])
"""


