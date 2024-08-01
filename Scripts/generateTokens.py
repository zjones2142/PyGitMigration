import requests
import json
import base64
import csv

def generate_access_token(username, password, note, scopes):
  """Generates a personal access token for a GitHub user.

  Args:
    username: The GitHub username.
    password: The GitHub password.
    note: A description for the token.
    scopes: A list of scopes for the token.

  Returns:
    The generated access token.
  """

  url = "https://api.github.com/authorizations/clients/new"
  headers = {"Authorization": f"Basic {base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')}"}
  data = {"scopes": scopes, "note": note}

  response = requests.post(url, headers=headers, json=data)
  response.raise_for_status()

  token = response.json()["token"]
  return token

def generate_tokens_for_orgs(username, password, scopes, orgs, output_file):
  """Generates access tokens for multiple GitHub organizations and stores them in a CSV file.

  Args:
    username: The GitHub username.
    password: The GitHub password.
    note: A description for the token.
    scopes: A list of scopes for the token.
    orgs: A list of GitHub organization names.
    output_file: The path to the output CSV file.
  """

  with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['orgName', 'token']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for org in orgs:
      # Generate a token for the organization using the provided username and password
      token = generate_access_token(username, password, f"Token for {org}", scopes)
      writer.writerow({'orgName': org, 'token': token})

if __name__ == "__main__":
  username = "your_username"
  password = "your_password"  # Replace with secure password storage
  scopes = ["repo", "admin:repo_hook"]  # Adjust scopes as needed
  orgsString = "" #comma seperated list of org names
  orgs = orgsString.split(',')
  output_file = "org_tokens.csv"

  generate_tokens_for_orgs(username, password, scopes, orgs, output_file)