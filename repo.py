import requests
import csv

# GitHub API endpoint for repositories
repos_url_template = "https://api.github.com/users/{username}/repos"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer YOUR_GITHUB_TOKEN"  # Replace with your GitHub token
}

# Function to fetch repositories for a user
def fetch_repositories(username):
    repos = []
    params = {"sort": "pushed", "direction": "desc", "per_page": 100}  # Get the most recently pushed repos, up to 100 per page
    page = 1

    while len(repos) < 500:  # Fetch up to 500 repositories
        params["page"] = page
        response = requests.get(repos_url_template.format(username=username), headers=headers, params=params)
        user_repos = response.json()

        # Stop if there are no more repositories
        if not user_repos or response.status_code != 200:
            break

        repos.extend(user_repos)
        page += 1

    return repos[:500]  # Return only the top 500 repositories

# Open repositories.csv for writing
with open("repositories.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", 
                     "language", "has_projects", "has_wiki", "license_name"])

    # Read users from users.csv
    with open("github_users_bangalore_detailed.csv", mode="r", newline='') as users_file:
        users_reader = csv.DictReader(users_file)
        for user in users_reader:
            username = user["Login"]
            repos = fetch_repositories(username)

            # Write each repository's information to the CSV
            for repo in repos:
                writer.writerow([
                    username,
                    repo.get("full_name", "N/A"),
                    repo.get("created_at", "N/A"),
                    repo.get("stargazers_count", 0),
                    repo.get("watchers_count", 0),
                    repo.get("language", "N/A"),
                    repo.get("has_projects", False),
                    repo.get("has_wiki", False),
                    repo.get("license", {}).get("key", "N/A")  # License name
                ])

print("Data saved to repositories.csv")
