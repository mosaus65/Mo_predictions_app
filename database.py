import sqlite3

DATABASE = "fixtures.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            match_date TEXT NOT NULL,
            match_time TEXT NOT NULL,
            league TEXT NOT NULL
        )
    """)

    columns = [
        column[1]
        for column in connection.execute(
            "PRAGMA table_info(fixtures)"
        ).fetchall()
    ]

    if "api_fixture_id" not in columns:
        connection.execute("""
            ALTER TABLE fixtures
            ADD COLUMN api_fixture_id INTEGER
        """)

    connection.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_fixtures_api_fixture_id
        ON fixtures(api_fixture_id)
    """)

    connection.commit()
    connection.close()


def add_sample_fixtures():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    sample_matches = [
        ("Arsenal", "Chelsea", "2026-11-20", "18:00", "Premier League"),
        ("Barcelona", "Real Madrid", "2026-11-22", "19:00", "La Liga"),
        ("Juventus", "Inter Milan", "2026-11-23", "20:00", "Serie A"),
        ("Bayern Munich", "Dortmund", "2026-11-24", "19:00", "Bundesliga"),
        ("PSG", "Marseille", "2026-11-24", "20:00", "Ligue 1"),
        ("Liverpool", "Manchester City", "2026-11-21", "20:00", "Premier League"),
        ("Real Madrid", "Bayern Munich", "2026-11-25", "20:00", "Champions League"),
        ("Enyimba", "Rangers", "2026-11-22", "16:00", "NPFL"),
        ("LA Galaxy", "Inter Miami", "2026-11-23", "19:00", "MLS"),
        ("Al Hilal", "Al Nassr", "2026-11-24", "20:00", "Saudi Pro League")
    ]

    for match in sample_matches:
        cursor.execute("""
            SELECT id FROM fixtures
            WHERE home_team = ?
            AND away_team = ?
            AND match_date = ?
            AND league = ?
        """, (match[0], match[1], match[2], match[4]))

        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO fixtures
                (home_team, away_team, match_date, match_time, league)
                VALUES (?, ?, ?, ?, ?)
            """, match)

    connection.commit()
    connection.close()


def save_api_fixtures(fixtures):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    saved_count = 0

    for match in fixtures:
        fixture_id = match["fixture"]["id"]
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]
        match_date = match["fixture"]["date"]

        date = match_date[:10]
        time = match_date[11:16]
        league = match["league"]["name"]

        cursor.execute("""
            INSERT OR IGNORE INTO fixtures (
                home_team,
                away_team,
                match_date,
                match_time,
                league,
                api_fixture_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            home_team,
            away_team,
            date,
            time,
            league,
            fixture_id
        ))

        if cursor.rowcount > 0:
            saved_count += 1

    connection.commit()
    connection.close()

    return saved_count


def get_fixtures(league=None):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    if league:
        fixtures = connection.execute("""
            SELECT * FROM fixtures
            WHERE league = ?
            ORDER BY match_date, match_time
        """, (league,)).fetchall()

    else:
        fixtures = connection.execute("""
            SELECT * FROM fixtures
            ORDER BY match_date, match_time
        """).fetchall()

    connection.close()

    return fixtures


def get_leagues():
    connection = sqlite3.connect(DATABASE)

    leagues = connection.execute("""
        SELECT DISTINCT league FROM fixtures
        ORDER BY league
    """).fetchall()

    connection.close()

    return [row[0] for row in leagues]


if __name__ == "__main__":
    create_database()
    add_sample_fixtures()

    matches = get_fixtures()

    print("Total fixtures:", len(matches))

    for match in matches:
        print(
            match["home_team"],
            "vs",
            match["away_team"],
            "|",
            match["match_date"],
            "|",
            match["league"]
        )
