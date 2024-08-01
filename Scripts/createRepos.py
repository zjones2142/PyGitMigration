import os
import requests
import json
import csv
import time

def create_repositories(org_name, repo_names, github_token):
    """
    Creates repositories from a list of names on a specified organization.

    Args:
        org_name (str): The name of the organization.
        repo_names (list): A list of repository names to create.
        github_token (str): A valid GitHub personal access token.
    """

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }

    base_url = "https://api.github.com/orgs/{org}/repos"
    url = base_url.format(org=org_name)

    for repo_name in repo_names:
        data = {
            "name": repo_name,
            "private": False  # Set to True for private repositories
        }
        time.sleep(2)
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            print(f"Repository {repo_name} created successfully in organization {org_name}.")
        else:
            print(f"Error creating repository {repo_name} in organization {org_name}: {response.text}\n")

def main():
    org_keys_file = 'FILEPATH of token file'
    org_token_dict = {}
    org_name_dict = {}

    # Read org and token pairs from CSV
    with open(org_keys_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for org, token in reader:
            org_token_dict[org.lower().replace('-de', '')] = token
            org_name_dict[org.lower().replace('-de', '')] = org

    root_dir = 'FILEPATH to root directory where repos are stored'

    for group_dir in os.listdir(root_dir):
        if group_dir == '.git':
            continue
        group_name = group_dir.lower()
        if group_name in org_token_dict:
            org_name = org_name_dict[group_name]
            repo_names = [f for f in os.listdir(os.path.join(root_dir, group_dir))]
            #create_repositories(org_name, repo_names, org_token_dict[group_name])
            if(not repo_names):
                print(f"No repositories to create for {group_name} in {org_name}")
            else:
                print(f"Creating repositories for {group_name} in {org_name}")
                create_repositories(org_name, repo_names, org_token_dict[group_name])
                #for repo in repo_names:
                    #print(f"\tCreating repo: {repo}")
        else:
            print(f"Token not found for group {group_dir}, skipping...\n")


if __name__ == "__main__":
    main()
