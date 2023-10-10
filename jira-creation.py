import os
from jira import JIRA
import random
import json
from hugchat import hugchat
from hugchat.login import Login

jira_url = 'https://xsaiops.atlassian.net'  
jira_username = 'xsaiops@gmail.com'
jira_api_token = 'ATATT3xFfGF0oqKkaruWu6b-OnjWgTiJ6wJ862NgD0ONyEUM_LavCvN4Mcp173U09L8GOotmkMXCbIfzPocRGjiqhECdNTN1i1CESwiUN_9Vf6zbWnjXhriJ8fYYe7YKQ8FP7vnQphxp34wXeD_tQLQ3p0PeaxBISWDz_9hKlDv54_OF01bBSY4=BFE83F4D'

project_key = 'ISSUE'
group_name = "AIOps"

members_list = []
file_path = 'output.json'
id_file_path = 'podId.txt'

def check_id_in_file(file_path, pod_id):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == pod_id:
                    return True
    except FileNotFoundError:
        return False
    return False

def add_id_to_file(file_path, pod_id):
    with open(file_path, 'a') as file:
        file.write(pod_id + '\n')

sign = Login("priyarohitsharma20@gmail.com", "Priya@200000")
cookies = sign.login()

# Save cookies to the local directory

cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

# load json file and read its contents

if os.path.exists(file_path):
    with open(file_path, "r") as jsonf:
        data = json.load(jsonf)
        for info in data:
            for poddata in data["pod_data"]:
                id = poddata["pod_id"]
                pod = poddata["pod_name"]
                namespace = poddata["namespace"]
                pod_status = poddata["pod_status"]
                pod_state = poddata["pod_state"]
                description = poddata["logs"]

                if not check_id_in_file(id_file_path, id):
                    add_id_to_file(id_file_path, id)
                    SUMMARY = f"Error Message: {pod_status} in Pod: {pod}  Namespace: {namespace}"
                    last_words_after_colon = description.split(":")[-1].strip()
                    DESCRIPTION = f"Namespace Name: {namespace}\n Pod: {pod}\n \n Error: {description}"

                    # create ticket format from the json data
                    issue_dict = {
                        'project': {'key': project_key},
                        'summary': SUMMARY,
                        'description': DESCRIPTION,
                        'issuetype': {'name': 'Task'},
                }
                    try:
                        jira = JIRA(server=jira_url, basic_auth=(jira_username, jira_api_token))
                        new_issue = jira.create_issue(fields=issue_dict)
                        print('Jira ticket created successfully:', new_issue.key)

                    except Exception as e:

                        print('An error occurred while creating the Jira ticket:', str(e))

                    group = jira.group_members(group_name)
                    for username in group:
                        user = jira.user(username)
                        user_name = user.displayName
                        account_Id = user.accountId
                        members_list.append(account_Id)
                    chosen_member_id = random.choice(members_list)

                    # Assign the Jira ticket to the randomly chosen member
                    new_issue.update(assignee={'accountId': chosen_member_id})
                    print('Jira ticket {} assigned to: {}'.format(new_issue.key, chosen_member_id))
                    query_result = chatbot.query(f"Give small explanation and solution for this error: {description} and don't say sure or sorry to hear that just give answer and start first line with this error message indicates that: ")
                    query_result_text = str(query_result)

                    jql_query = 'project = "Incident" ORDER BY created DESC'

                    issues = jira.search_issues(jql_query)
                    issue = issues[0]
                    if issues:
                        issue = issues[0]
                        comment_text = f"Here is an issue in a Kubernetes pod named {pod} Specifically, it's indicating that the container is waiting to start, and the problem seems to be related to pulling the container image."
                        jira.add_comment(issue, query_result_text)
                        print(f"Comment added to issue {issue.key}: {query_result_text}")