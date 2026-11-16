def predict_match(
    home_goals_scored,
    home_goals_conceded,
    away_goals_scored,
    away_goals_conceded
):
    home_strength = (
        home_goals_scored - away_goals_conceded
    )

    away_strength = (
        away_goals_scored - home_goals_conceded
    )

    home_score = max(1, 10 + home_strength * 2)
    away_score = max(1, 10 + away_strength * 2)

    draw_score = max(
        1,
        10 - abs(home_strength - away_strength) * 2
    )

    total_score = home_score + draw_score + away_score

    home_probability = (
        home_score / total_score
    ) * 100

    draw_probability = (
        draw_score / total_score
    ) * 100

    away_probability = (
        away_score / total_score
    ) * 100

    return {
        "home_win": round(home_probability, 2),
        "draw": round(draw_probability, 2),
        "away_win": round(away_probability, 2)
    }


if __name__ == "__main__":
    result = predict_match(
        2.0, 0.8,
        1.2, 1.5
    )

    print("Home win:", result["home_win"], "%")
    print("Draw:", result["draw"], "%")
    print("Away win:", result["away_win"], "%")
