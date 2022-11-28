from os import getenv
import argparse

from github import Github
from dotenv import load_dotenv

# Load GitHub token from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser()

# Enable deletion of forks with no additional contributions
parser.add_argument(
    "--delete",
    help="Deletes the forks with no commits from the authenticated user",
    action="store_true",
)

# Enable deletion of all forks
parser.add_argument("--delete-all", help="Deletes all forks", action="store_true")

# Parse arguments
args = parser.parse_args()

# Initialize GitHub endpoint
g = Github(getenv("GITHUB_ACCESS_TOKEN"))

# Count forks
count_forks: int = 0

# Count forks with no contributions from myself
count_forks_no_commits: int = 0

print("Logged in with", g.get_user().login)

# Make sure the user understands the destructive nature of the script
if args.delete_all:
    print(
        "This will delete all forks, even forks you contributed to. Are you sure? (y/n)"
    )
    if input() != "y":
        exit()
if args.delete:
    print(
        "This will delete forks with no commits from the authenticated user. Are you sure? (y/n)"
    )
    if input() != "y":
        exit()

for repo in g.get_user().get_repos(type="forks"):
    # If the authenticated user is not the owner, skip
    if (repo.owner.login == g.get_user().login) is False:
        continue

    if repo.fork:
        count_forks += 1
        if repo.get_commits(author=g.get_user()).totalCount == 0:
            count_forks_no_commits += 1

            # Delete the fork if the user has specified the --delete flag
            if args.delete:
                print("Deleting", repo.full_name)

                try:
                    # Uncomment the following line to delete the repository
                    repo.delete()
                except Exception as e:
                    print("Failed to delete", repo.full_name)
                    print("Unexpected: ", e)
            else:
                print("Can delete", repo.full_name)
        else:
            # Delete the fork if the user has specified the --delete-all flag
            if args.delete_all:
                print("Deleting", repo.full_name)

                try:
                    # Uncomment this line to actually delete the repository
                    # repo.delete()
                    pass
                except Exception as e:
                    print("Failed to delete", repo.full_name)
                    print("Unexpected: ", e)

print("Total forks: ", count_forks)
print("Total forks with no commits by the authenticated user: ", count_forks_no_commits)
