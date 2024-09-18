import argparse
import requests
import sys

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    
    if response.status_code == 404:
        print(f"Error: Usuario '{username}' no encontrado.")
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: No se pudo obtener la actividad del usuario. Código de estado: {response.status_code}")
        sys.exit(1)
    
    return response.json()

def display_activity(events):
    for event in events:
        event_type = event['type']
        repo_name = event['repo']['name']
        
        if event_type == 'PushEvent':
            commits = len(event['payload']['commits'])
            print(f"Pushed {commits} commits to {repo_name}")
        elif event_type == 'IssuesEvent':
            action = event['payload']['action']
            print(f"{action.capitalize()} a new issue in {repo_name}")
        elif event_type == 'WatchEvent':
            print(f"Starred {repo_name}")
        else:
            print(f"{event_type} in {repo_name}")

def main():
    parser = argparse.ArgumentParser(description="Obtener la actividad reciente de un usuario de GitHub.")
    parser.add_argument("username", help="Nombre de usuario de GitHub")
    args = parser.parse_args()
    
    username = args.username
    events = fetch_github_activity(username)
    display_activity(events)

if __name__ == "__main__":
    main()