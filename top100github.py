import requests
import csv

# GitHub API endpoints
search_url = "https://api.github.com/search/users"
user_url = "https://api.github.com/users/"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer YOUR_GITHUB_TOKEN"  # Replace with your GitHub token
}

page = 1
# Search parameters for users in Bangalore with over 100 followers
search_params = {
    "q": "location:bangalore followers:>=100",
    "per_page": 100  # Limit per page (adjust if you want more results),
    "page":page
}

def clean_company_name(company_name):
    # Trim whitespace, remove leading @, and convert to uppercase
    return company_name.strip().lstrip('@').upper()

# Get search results (up to 100 users per page)

header = true
# Open CSV file for writing
with open("github_users_bangalore_detailed.csv", mode="w", newline='') as file:
while True:
    response = requests.get(search_url, headers=headers, params=search_params)
    if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
    users_data = response.json().get("items", [])
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Login", "Name", "Company", "Location", "Email", "Hireable", "Bio", 
                     "Public Repos", "Followers", "Following", "Created At"])
    header=false
    # Loop through each user in the search results
    for user in users_data:
        # Get detailed user data from /users/{username} endpoint
        user_response = requests.get(user_url + user["login"], headers=headers)
        user_info = user_response.json()

        # Retrieve and process user data
        login = user_info.get("login", "N/A")
        name = user_info.get("name", "N/A")
        company = clean_company_name(user_info.get("company", "N/A") or "")
        location = user_info.get("location", "N/A")
        email = user_info.get("email", "N/A")
        hireable = user_info.get("hireable", "N/A")
        bio = user_info.get("bio", "N/A")
        public_repos = user_info.get("public_repos", 0)
        followers = user_info.get("followers", 0)
        following = user_info.get("following", 0)
        created_at = user_info.get("created_at", "N/A")

        # Write row to CSV
        writer.writerow([login, name, company, location, email, hireable, bio, 
                         public_repos, followers, following, created_at])
    link_header = response.headers.get("Link", "")
    if 'rel="next"' not in link_header:
            break  # Exit loop if no more pages
    page += 1
print("Data saved to github_users_bangalore_detailed.csv")
