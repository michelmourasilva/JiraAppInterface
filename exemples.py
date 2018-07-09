# -*- coding: latin-1 -*-
import JiraClass

# Connection
# jira_connection = JiraClass.jiraconetion()

# --------------------------------------------------------------

# # object JiraClass
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
# object_jira_class_support = JiraClass.IssueJiraSupport(
#     issue='new'
#     , project='PEE'
#     , issue_type='Sustentação AD'
#     , summary='Sumario'
#     , opened_date='2018-06-05 01:01:01'
#     , observation='Observação'
#     , requester='Jansen'
#     , complexity='Media' # Baixa, Alta, Media, None
#     , service_order='OS1'
#     , necessity='Realizar Roteiro e Teste de Dados'
#     , necessity_code='BIN016'
#     , priority='Emergencia' # Emergencia, Normal
# )
# # append thematic jira
# object_jira_class_support.append_thematic({'RAIS', 'ENEM'})

# # prepare dict to insert issue
# support_json = object_jira_class_support.return_json_add_issue()
# print(support_json)

# # prepare dict to insert issue
# new_issue = JiraClass.add_issue(support_json)

# # return issue support
# object_jira_class_support_return = JiraClass.IssueJiraSupport(issue='PEE-27')
# object_jira_class_support_return.return_issue()

# --------------------------------------------------------------

# object JiraClass
# object_jira_class_child = JiraClass.IssueJiraSupportChild(
#       issue='PEE-29'
#     , project='PEE'
#     , issue_type='Apoiar a Administração de Ferramenta ETL'
#     , summary='Sumario'
#     , observation='Observação'
#     , parent='PEE-29'
#     , technical_profile='AD'
#     , activity='Apoiar a Administração de Ferramenta ETL'
#     , activity_code='BIA001'
# )
# # # prepare dict to insert issue
# child_json = object_jira_class_child.return_json_add_issue()
# print(child_json)

# # prepare dict to insert issue
# new_sub_issue = JiraClass.add_issue(child_json)

# --------------------------------------------------------------

## Worklog

# worklog = JiraClass.Worklog( issue_name='PEE-30', author='Michel Moura Silva'
#                   , date_start='2018-06-09 19:16:01', date_end='2018-06-09 22:16:01', time_spent_seconds=0)

# worklog.add_work_log()

# --------------------------------------------------------------
# JiraClass.add_attachment('PEE-29', 'C:\FILES\TO.PNG')