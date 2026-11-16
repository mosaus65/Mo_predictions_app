import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def get_league_teams(league_id, season):
    if not API_KEY:
        print("API key not found. Check your .env file.")
        return []

    parameters = {
        "league": league_id,
        "season": season
    }

    try:
        response = requests.get(
            f"{BASE_URL}/teams",
            headers=HEADERS,
            params=parameters,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        if data.get("errors"):
            print("API error:", data["errors"])
            return []

        teams = data.get("response", [])

        print("\nPREMIER LEAGUE TEAMS")
        print("----------------------")

        for item in teams:
            team_id = item["team"]["id"]
            team_name = item["team"]["name"]

            print(f"Team ID: {team_id} | Team: {team_name}")

        print("----------------------")
        print("Total teams:", len(teams))

        return teams

    except requests.exceptions.RequestException as error:
        print("Could not retrieve teams:", error)
        return []


def get_upcoming_fixtures(league_id, season, count=5):
    if not API_KEY:
        print("API key not found. Check your .env file.")
        return []

    parameters = {
        "league": league_id,
        "season": season,
        "from": "2024-08-01",
        "to": "2024-08-31",
        "timezone": "Africa/Lagos"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/fixtures",
            headers=HEADERS,
            params=parameters,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        if data.get("errors"):
            print("API error:", data["errors"])
            return []

        fixtures = data.get("response", [])

        return fixtures[:count]

    except requests.exceptions.RequestException as error:
        print("Could not retrieve fixtures:", error)
        return []


def get_team_statistics(league_id, season, team_id):
    if not API_KEY:
        print("API key not found. Check your .env file.")
        return None

    parameters = {
        "league": league_id,
        "season": season,
        "team": team_id
    }

    for attempt in range(1, 4):
        try:
            response = requests.get(
                f"{BASE_URL}/teams/statistics",
                headers=HEADERS,
                params=parameters,
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            if data.get("errors"):
                print("API error:", data["errors"])
                return None

            stats = data.get("response")

            if not stats:
                print("No team statistics found.")
                return None

            fixtures = stats["fixtures"]
            goals = stats["goals"]

            print("\nTEAM STATISTICS")
            print("----------------------")

            print("Team:", stats["team"]["name"])
            print("League:", stats["league"]["name"])
            print("Season:", stats["league"]["season"])

            print("\nMatches played:", fixtures["played"]["total"])
            print("Wins:", fixtures["wins"]["total"])
            print("Draws:", fixtures["draws"]["total"])
            print("Losses:", fixtures["loses"]["total"])

            print("\nGoals scored:", goals["for"]["total"]["total"])
            print("Goals conceded:", goals["against"]["total"]["total"])

            print("----------------------")

            return stats

        except requests.exceptions.Timeout:
            print(f"Request timed out. Attempt {attempt}/3")

        except requests.exceptions.RequestException as error:
            print("Could not retrieve statistics:", error)
            return None

    print("Failed after 3 attempts.")
    return None


def get_all_team_statistics(league_id, season):
    teams = get_league_teams(league_id, season)

    if not teams:
        print("No teams found.")
        return []

    all_statistics = []

    print("\nRETRIEVING ALL TEAM STATISTICS")

    for item in teams:
        team_id = item["team"]["id"]
        team_name = item["team"]["name"]

        print(f"\nGetting statistics for {team_name}...")

        stats = get_team_statistics(
            league_id,
            season,
            team_id
        )

        if stats:
            all_statistics.append(stats)
        else:
            print(f"Skipping {team_name}. Moving to the next team.")

    print("\n======================")
    print("STATISTICS SUMMARY")
    print("======================")
    print("Total teams found:", len(teams))
    print("Successful statistics:", len(all_statistics))
    print("Failed statistics:", len(teams) - len(all_statistics))
    print("======================")

    return all_statistics


if __name__ == "__main__":
    all_stats = get_all_team_statistics(39, 2024)
