from flask import Flask, render_template, request
import search
from experiments import run_experiments
app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index_version3.html")


@app.route('/explanation', methods=['POST'])
def explanation():
    return render_template("explanation_version3.html")


@app.route('/experiments', methods=['POST'])
def experiments():

    if request.method == 'POST':
        experiments, ortho_avg_diff, phonetic_avg_diff = run_experiments()

        experiment_01 = experiments[0].values
        experiment_02 = experiments[1].values
        experiment_03 = experiments[2].values
        experiment_04 = experiments[3].values

    return render_template("experiments_version3.html",
                           ortho_avg_diff=ortho_avg_diff,
                           phonetic_avg_diff=phonetic_avg_diff,
                           experiment_01=experiment_01,
                           experiment_02=experiment_02,
                           experiment_03=experiment_03,
                           experiment_04=experiment_04)


@app.route('/search', methods=['POST'])
def searcher():

    searchterm = request.form.get('searchterm')
    threshold = request.form.get('threshold')

    if request.method == 'POST':
        sources = request.form.getlist('checkbox_sources')
        print(f'\nThis is the request form with the selected lists: {sources}')
    else:
        return print('We tried')

    data = search.search(searchterm, sources, threshold)
    data = list(data.values)

    return render_template("res_version3.html", data=data, searchterm=searchterm, threshold=threshold)


if __name__ == "__main__":
    app.run(debug=True)
