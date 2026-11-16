from flask import Flask, render_template, request
from datetime import datetime

from database import (
    create_database,
    add_sample_fixtures,
    get_fixtures,
    get_leagues
)

from prediction import predict_match

app = Flask(__name__)

create_database()
add_sample_fixtures()


@app.route("/")
def home():
    selected_league = request.args.get("league", "")

    if selected_league:
        fixtures = get_fixtures(selected_league)
    else:
        fixtures = get_fixtures()

    leagues = get_leagues()

    predictions = {}

    for match in fixtures:
        predictions[match["id"]] = predict_match(
            2.0, 0.8, 1.2, 1.5
        )

    today = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        "index.html",
        fixtures=fixtures,
        leagues=leagues,
        selected_league=selected_league,
        predictions=predictions,
        today=today
    )


if __name__ == "__main__":
    app.run(debug=True)
