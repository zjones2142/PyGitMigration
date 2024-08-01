import json
import gitlab
from gitlab import Gitlab

#this file retrieves any/all info desired from a gitlab instance

# Replace with your actual access token and GitLab domain URL
access_token = ""
gitlab_url = ""

def test_connection():
  """Tests connection to the GitLab API using python-gitlab."""
  try:
    # Create a Gitlab instance
    gl = Gitlab(gitlab_url, private_token=access_token)
    return True

  except gitlab.exceptions.GitlabGetError as e:
    print(f"Error connecting to GitLab: {e}")
    return False
    
def get_projects_toJSON(filename):
  #Retrieves info from gitlab API
  if(filename == ''):
    filename="gitlab-projects.json"

  gl = Gitlab(gitlab_url, private_token=access_token)

  total_pages = 16  # Replace with actual total pages if known

  with open(filename, "w") as file:
  # Initialize an empty list to store all project info
      all_projects = []

      # Loop through page numbers
      for page_number in range(1, total_pages + 1):
        # Retrieve projects for current page
        page = gl.projects.list(per_page=20, page=page_number)

        # Append project info to the list for each project on the page
        for project in page:
          project_name_no_spaces = project.name.replace(" ", "_")
          project_info = {
              "url": project.web_url,
              "name": project_name_no_spaces
          }
          all_projects.append(project_info)
            # Write the entire list of projects as JSON data with indentation
      json.dump(all_projects, file, indent=2)

  print(f"Project information written to: {filename}")

def get_projects_toCSV(filename):
  #Retrieves information about projects from the GitLab API and exports to CSV.
  if(filename == ''):
      filename="gitlab-projects.csv"

  gl = Gitlab(gitlab_url, private_token=access_token)

  # Use Projects API endpoint with pagination
  page_number = 1
  all_projects = []
  while True:
    # Retrieve projects for current page
    page = gl.projects.list(per_page=20, page=page_number)

    # Check if any projects retrieved
    if not page:
      break

    # Append project information to list with name and URL separated by comma
    for project in page:
      project_info = f"{project.name},{project.web_url}"
      all_projects.append(project_info)

    page_number += 1

  # Write the entire list of projects to CSV with each line having name and URL
  with open(filename, "w") as file:
    if not all_projects:
      print("No projects found. Try checking your GitLab URL or access token.")
    else:
      file.write("\n".join(all_projects))  # Join project info with newlines
      print(f"Project information written to: {filename}")

def get_projects_FromGrouptoJSON(filename, group):
  #Retrieves info from gitlab API
  if(filename == ''):
    filename=f"FILEPATH\\{group.name}-projects.json"

  with open(filename, "w") as file:
  # Initialize an empty list to store all project info
      all_projects = []

      # Retrieve projects for current page
      groupProjects = group.projects.list(all=True)

      # Append project info to the list for each project on the page
      for project in groupProjects:
        project_name_no_spaces = project.name.replace(" ", "_")
        project_info = {
            "url": project.web_url,
            "name": project_name_no_spaces
        }
        all_projects.append(project_info)
          # Write the entire list of projects as JSON data with indentation
      json.dump(all_projects, file, indent=2)

  print(f"Project information written to: {filename}")

def get_users_toJSON(isExternal,filename):
  #Retrieves information about users from the GitLab API.
  
  if(filename == ''):
      filename="gitlab-users.json"

  gl = Gitlab(gitlab_url, private_token=access_token)

  # Use Users API endpoint with pagination
  page_number = 1
  all_users = []
  while True:
    # Retrieve users for current page
    page = gl.users.list(per_page=20, page=page_number)

    # Check if any users retrieved
    if not page:
      break

    # Append user information to the list for each user
    for user in page:
      user_info = {
          "name": user.name,
          "email": user.email  # Include user ID for further use
          # Add other user properties as needed (e.g., email)
      }
      if(user.external == isExternal):
        all_users.append(user_info)

    page_number += 1

  # Write the entire list of users as JSON data with indentation
  with open(filename, "w") as file:
    if not all_users:
      print("No users found with filter. Try something else.")
    else:
      json.dump(all_users, file, indent=2)
      print(f"User information written to: {filename}")

def get_users_toCSV(isExternal, filename):
  #Retrieves information about users from the GitLab API and exports to CSV.

  if(filename == ''):
      filename="gitlab-users.csv"

  gl = Gitlab(gitlab_url, private_token=access_token)

  # Use Users API endpoint with pagination
  page_number = 1
  all_users = []
  while True:
    # Retrieve users for current page
    page = gl.users.list(per_page=20, page=page_number)

    # Check if any users retrieved
    if not page:
      break

    # Append user information to list for each user with matching external state
    for user in page:
      if user.external == isExternal:
        user_info = f"{user.name},{user.email}"  # Combine name and email with comma separator
        all_users.append(user_info)

    page_number += 1

  # Write the entire list of users to CSV with each line having name and email
  with open(filename, "w") as file:
    if not all_users:
      print("No users found with filter. Try something else.")
    else:
      file.write("\n".join(all_users))  # Join user info with newlines
      print(f"User information written to: {filename}")

def get_groups_toCSV_Wsubgroups(filename):
  #Retrieves information about top-level groups and their subgroups from the GitLab API and exports to CSV.

  if(filename == ''):
      filename="gitlab-groups.csv"

  gl = Gitlab(gitlab_url, private_token=access_token)

  # Use Groups API endpoint with top_level_only parameter
  all_groups = gl.groups.list(all=True, top_level_only=True)

  # Check if any groups retrieved
  if not all_groups:
    print("No groups found. Try checking your GitLab URL or access token.")
    return

  # Prepare header row for CSV
  header_row = "Group: Subgroups\n\n"

  # List to store processed group data
  group_data = []

  for group in all_groups:
    all_subgroups = group.subgroups.list(all=True)
    group_data.append(f"{group.name}:"+", ".join(str(subgroup.name) for subgroup in all_subgroups))

  # Write header and group info to CSV
  with open(filename, "w") as file:
    file.write(header_row + "\n".join(group_data))
    print(f"Group information with subgroups written to: {filename}")

def get_groups_toCSV(filename):
  #Retrieves information about top-level groups and their subgroups from the GitLab API and exports to CSV.

  if(filename == ''):
      filename="gitlab-groups.csv"

  gl = Gitlab(gitlab_url, private_token=access_token)

  # Use Groups API endpoint with top_level_only parameter
  all_groups = gl.groups.list(all=True)

  # Check if any groups retrieved
  if not all_groups:
    print("No groups found. Try checking your GitLab URL or access token.")
    return

  # Prepare header row for CSV
  header_row = "Group Names:\n\n"

  # List to store processed group data
  group_data = []

  for group in all_groups:
    group_data.append(f"{group.name},")

  # Write header and group info to CSV
  with open(filename, "w") as file:
    file.write(header_row + "\n".join(group_data))
    print(f"Group information with subgroups written to: {filename}")

def UserExportType(isExternal,file):
  fileType = input("json(1) or csv(2)? ")
  if fileType == "1":
    get_users_toJSON(isExternal,file)
  elif fileType == "2":
    get_users_toCSV(isExternal,file)
  else:
    print("Invalid input, try again.\n")
    UserExportType(isExternal,file)

def ProjectExportType(file):
  fileType = input("json(1) or csv(2)? ")
  if fileType == "1":
    get_projects_toJSON(file)
  elif fileType == "2":
    get_projects_toCSV(file)
  else:
    print("Invalid input, try again.\n")
    ProjectExportType(file)

def UserExternal_or_Internal(file):
  data1 = input("External(1) or Internal(2)? ")
  if data1 == "1":
    UserExportType(True,file)
  elif data1 == "2":
    UserExportType(False,file)
  else:
    print("Invalid Input, try again.")
    UserExternal_or_Internal(file)

def whatGroup(file):
  groupName = input("Enter the name of the group: ")
  gl = Gitlab(gitlab_url, private_token=access_token)
  groups = gl.groups.list(all=True)
  for group in groups:
    if group.name == groupName:
      group1 = group
  if not group1:
    print("Group not found, try again.\n")
    whatGroup(file)
  else:
    get_projects_FromGrouptoJSON(file,group1)

def subGroupOrNo(file):
  subGroup = input("Subgroups listed? (1=No, 2=Yes)")
  if subGroup == "1":
    get_groups_toCSV(file)
  elif subGroup == "2":
    get_groups_toCSV_Wsubgroups(file)
  else:
    print("Invalid Input, try again.")
    subGroupOrNo(file)

def User_Proj_Group(file):
  type = input("Retrieve Users(1), Projects(2), Groups(3), or Proj from Group(4)? ")
  match type:
        case "1":
            UserExternal_or_Internal(file)
        case "2":
            ProjectExportType(file)
        case "3":
            subGroupOrNo(file)
        case "4":
            whatGroup(file)
        case _:
            print("Invalid Input, try again.\n")
            User_Proj_Group(type, file)

"""below functions can be uncommented if extra logic is needed"""
# def is_project_empty(project):
#   try:
#     tree = project.repository_tree(project.id, recursive=False)
#   except:
#     return True
#   return not tree

# def is_group_empty(group):
#   # Checks if a group has no projects
#   # Check for projects
#   for project in group.projects.list(get_all=True):
#     if not is_project_empty(project):
#       return False  # Project is not empty, so group is not empty
#   return True  # Group is empty

def main():
  if test_connection():
    print("Connected to GitLab server.")
    file = input("Name for export file (leave empty for default): ")
    User_Proj_Group(file)
  else:
    print("Failed to connect to GitLab server.")

if __name__ == "__main__":
  main()