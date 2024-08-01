import csv
import json
import requests

def get_repo_urls_from_github(csv_file, output_file):
    """Retrieves repository URLs from GitHub for organizations listed in a CSV.

    Args:
        csv_file (str): Path to the CSV file containing org names and access tokens.
        output_file (str): Path to the output JSON file.
    """

    org_repos = {}

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            org_name, access_token = row
            org_repos[org_name] = []

            page = 1
            while True:
                url = f"https://{access_token}@api.github.com/orgs/{org_name}/repos?per_page=100&page={page}" #adding auth headers to url
                response = requests.get(url)
                if response.status_code == 200:
                    repos = response.json()
                    if not repos:
                        break
                    for repo in repos:
                        org_repos[org_name].append({'repoName': repo['name'], 'url': repo['html_url']})
                    page += 1
                else:
                    print(f"Error fetching repos for {org_name}: {response.text}")
                    break

    with open(output_file, 'w') as f:
        json.dump(org_repos, f, indent=2)

if __name__ == "__main__":
    csv_file = 'FILEPATH to token file'
    output_file = 'output json filename (specify path if wanted in certain directory such as; C:\\User\\Jsons\\AllProjects\\output.json)'
    get_repo_urls_from_github(csv_file, output_file)
