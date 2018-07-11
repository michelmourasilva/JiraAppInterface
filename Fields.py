from JiraClass import jiraconetion

serverjira = jiraconetion()
issues = serverjira.search_issues("project=PEE and issue=PEE-28 order by issue asc", validate_query=True, expand=None, json_result=None, maxResults=1000000)

for issue in issues:
    issue = serverjira.issue(issue)
    #worklogs = serverjira.worklogs(issue.key)
    print('teste')
    pass

