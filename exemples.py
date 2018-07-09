# -*- coding: latin-1 -*-
import JiraClass

# Connection
jira_connection = JiraClass.jiraconetion()

# --------------------------------------------------------------

# object JiraClass
# object_jira_class = JiraClass.IssueJira(
#     issue='new'
#     , project='PEE'
#     , issue_type='Sustentação AD'
#     , summary='Sumario'
#     , opened_date='2018-06-05 01:01:01'
#     , status=None
#     , observation='Observação'
# )
# # append jira
# object_jira_class.append_artifact('ARTEFATO1')
# object_jira_class.append_artifact('ARTEFATO2')

# return issue
# object_jira_class_return = JiraClass.IssueJira(issue='PEE-27')
# object_jira_class_return.return_issue()

# --------------------------------------------------------------

# object JiraClass
object_jira_class_support = JiraClass.IssueJiraSupport(
    issue='new'
    , project='PEE'
    , issue_type='Sustentação AD'
    , summary='Sumario'
    , opened_date='2018-06-05 01:01:01'
    , observation='Observação'
    , requester='Jansen'
    , complexity='Media' #Baixa, Alta, Media, None
    , service_order='OS1'
    , necessity='Realizar Roteiro e Teste de Dados'
    , necessity_code='BIN016'
    , priority='Emergencia' #Emergencia, Normal

)
# append jira
object_jira_class_support.append_thematic({'RAIS', 'ENEM'})

# prepare dict to insert issue
support_json = object_jira_class_support.return_json_add_issue()
print(support_json)

# prepare dict to insert issue
print('Jira issue created. Name Issue:'.format(JiraClass.add_issue(support_json)))


# return issue support
# object_jira_class_support_return = JiraClass.IssueJiraSupport(issue='PEE-27')
# object_jira_class_support_return.return_issue()

print('')

