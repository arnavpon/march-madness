import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

from ..models import search
from ..helpers import string_formatting as sf
from .form import SeedForm, TeamForm


app = Flask(__name__)
with open(os.path.join(os.getcwd(), "march_madness/web/keys.txt")) as f:
    app.config['SECRET_KEY'] = f.read()
Bootstrap(app)


@app.route('/')
def index():
    """
    Creates simple web form allowing user to input a seed or team
    :return:
    """
    return render_template("index.html")


@app.route('/team', methods=['GET', 'POST'])
def team_form():
    form = TeamForm()
    message = ""
    if form.validate_on_submit():
        team = form.team.data
        return redirect(f"/team/result/{team}")
    else:
        message = "Please enter a team name"
    return render_template("team_form.html", form=form, message=message)


@app.route('/team/result/<team>')
def search_by_team(team):
    best_round = "1000"
    best_years = ""
    other_results = []
    results = search.search_for_team(team)
    sorted_keys = sorted(results.keys())  # sort low -> high (best -> worst finishes)
    counter = 0
    if len(sorted_keys) > 1:  # check that team has some wins
        for round_number in sorted_keys:
            years = results[round_number]
            formatted_round = search.format_round_number(round_number, len(sorted_keys))
            if formatted_round != "":  # ignore empty result, continue loop
                y = [f"{yr}" for yr in years]
                if counter == 0:
                    best_round = formatted_round
                    best_years = ', '.join(y)
                else:
                    other_results.append((formatted_round, ', '.join(y)))
            counter += 1
    return render_template("team_result.html", team=sf.format_string_for_display(team), best_round=best_round, best_years=best_years, other=other_results)


@app.route('/seed', methods=['GET', 'POST'])
def seed_form():
    form = SeedForm()
    message = ""
    if form.validate_on_submit():
        seed = form.seed.data
        return redirect(f"/seed/result/{seed}")
    else:
        message = "Please input a seed between 1 and 16"
    return render_template('seed_form.html', form=form, message=message)


@app.route('/seed/result/<seed>')
def search_by_seed(seed):
    best_round = "1000"
    best_teams = []
    other_results = []
    results = search.search_for_seed(int(seed))
    sorted_keys = sorted(results.keys())  # sort low -> high (best -> worst finishes)
    counter = 0
    if len(sorted_keys) > 1:  # at least one team has won a game
        for round_number in sorted_keys:
            format_round = search.format_round_number(round_number, 2)
            years_by_team = results[round_number]  # { team_name: [years] }
            if format_round != "":
                if counter == 0:  # first run == best
                    best_round = format_round
                    for team, years in years_by_team.items():
                        y = [f"{yr}" for yr in years]
                        best_teams.append((sf.format_string_for_display(team), ', '.join(y)))
                else:  # other runs
                    running_ls = []
                    for team, years in years_by_team.items():
                        y = [f"{yr}" for yr in years]
                        t = (sf.format_string_for_display(team), ', '.join(y))
                        running_ls.append(t)
                    other_results.append((format_round, running_ls))
            counter += 1
    return render_template("seed_result.html", seed=seed, best_round=best_round, best_teams=best_teams, other_results=other_results)