# -*- coding: latin-1 -*-
from jira import JIRA
import JiraOptions
import util
# import psycopg2


def jira_connection():
    """Connection with Jira server"""
    jira_options = {
        'server': JiraOptions.SERVER, 'verify': False
    }
    server_jira = JIRA(jira_options, basic_auth=(JiraOptions.USERNAME, JiraOptions.PASSWORD), max_retries=10)
    return server_jira


class IssueJira(object):
    """
    """
    def __init__(self, issue='new', project=None, issue_type=None, summary=None,
                 opened_date=None, status='optional', observation=None):
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
            issue_fields = jira_connection().issue(self.issue)  # Check if issue exists
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

    def update_status(self, transition):
        """
        Update a issue status
        :param transition: Possible values (
        Triagem, Em analise, Em atendimento, Avaliacao solicitante, Finalizado, Pendente solicitante, Em Pausa
        )
        :return:  Nothing, it's a void method
        """
        self.return_issue()
        if self.issue is not None:
            if transition in list(self.get_transitions()):
                jira_connection().transition_issue(self.issue, transition)
            else:
                raise Exception('This transitions is not allowed. method: update_status')

    def get_transitions(self):
        """
        :return:  all transitions allowed to use in issues
        """
        jira = jira_connection()
        issue = jira.issue(self.issue)
        transitions = jira.transitions(issue)
        for i in transitions:
            yield i['name']

    def get_option_allowed_values(self, field):
        """
        :param field: issue field key
        :return: all allowed values in field
        """
        jira = jira_connection()
        field_json = jira.createmeta(projectKeys=self.project,
                                     issuetypeNames=self.issue_type,
                                     expand='projects.issuetypes.fields')['projects'][0]['issuetypes'][0]['fields'][
            field]['allowedValues']
        for value in field_json:
            yield value['value']


class IssueJiraSupport(IssueJira):
    """
    """
    def __init__(self, issue, project=None, issue_type=None,
                 summary=None, opened_date=None, status='optional', observation=None,
                 requester=None, complexity=None, service_order=None, necessity=None,
                 necessity_code=None, priority=None):
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
            issue_fields = jira_connection().issue(self.issue)
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

    def get_necessity(self):
        pass


class IssueJiraSupportChild(IssueJira):
    """
    Parent class
    Par�metros Esperados IssueJira class
        issue, project, issue_type, summary, opened_date, status, objservation
    Par�metros Esperados IssueJiraSupportChuild class
         parent, technical_profile, activity, activity_code
    """
    def __init__(self, issue=None, project=None, issue_type=None, summary=None, opened_date=None, status='optional',
                 observation=None, parent=None, technical_profile=None, activity=None, activity_code=None):
        super().__init__(issue, project, issue_type, summary, opened_date, status, observation)
        self.technical_profile = technical_profile
        self.parent = parent
        self.activity = activity
        self.activity_code = activity_code

    def return_issue(self):
        try:
            issue_fields = jira_connection().issue(self.issue)
            self.issue = issue_fields.field.status
            self.project = issue_fields.fields.project
            self.issue_type = issue_fields.fields.issuetype
            self.summary = issue_fields.fields.summary
            self.status = issue_fields.fields.status
            self.parent = issue_fields.fields.parent
        except AttributeError:
            self.issue = None
            self.project = None
            self.issue_type = None
            self.summary = None
            self.status = None
            self.parent = None

    def return_json_add_issue(self):
        issue_dict = {
            'parent': {'key': self.parent},
            'project': self.project,
            'summary': self.summary,
            'issuetype': self.issue_type,
            'customfield_12505': self.observation,  # observation
            'customfield_12511': {'value': self.technical_profile},  # technical profile
            'customfield_12513': {'value': self.activity, 'child': {'value': self.activity_code}},  # activity
        }
        return issue_dict

    def get_activity(self):
        pass


class Work_log(object):
    def __init__(self, issue_name, author, date_start, date_end, time_spent_seconds):
        self.issue_name = issue_name
        self.author = author
        self.date_start = util.returndatetime(date_start)[2]
        self.time_spent_seconds = time_spent_seconds
        self.date_end = util.returndatetime(date_end)[2]

    def add_work_log(self):
        time_spent = (self.date_end-self.date_start).seconds
        jira_connection().add_worklog(user=self.author, issue=self.issue_name,
                                      started=util.returndatetime(self.date_start)[3], timeSpentSeconds=time_spent)


def check_mandatory_fields(object_jira):
    """
    Check all mandatory attributes in class.
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
    return jira_connection().create_issue(fields=issue_dict)


def add_attachment(issue_name, file_path):
    jira_connection().add_attachment(issue=issue_name, attachment=file_path)
