from flask import Flask, render_template, request
import search
from experiments import experiments

app = Flask(__name__, template_folder='templates')

# mypath = '/home/alexsmc/poca/'
# mypath = '/Users/nicolasperez/PycharmProjects/app_poca'
mypath = 'C:/Users/pen/PycharmProjects/poca_app'


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index_version3.html")


@app.route('/explanation', methods=['POST'])
def explanation():
    return render_template("explanation_version3.html")


@app.route('/experiments', methods=['POST'])
def experiments():

    if request.method == 'POST':
        experiment_01 = experiments()
        experiment_01 = list(experiment_01.values)

    return render_template("experiments_version3.html", experiment_01=experiment_01)


@app.route('/search', methods=['POST'])
def searcher():

    print('in search')
    searchterm = request.form.get('searchterm')
    threshold = request.form.get('threshold')

    if request.method == 'POST':
        print('DONE')
        print(request.form.getlist('checkbox_sources'))
        sources = request.form.getlist('checkbox_sources')
    else:
        return print('We tried')

    data = search.search(searchterm, sources, threshold)
    data = list(data.values)

    return render_template("res_version3.html", data=data, searchterm=searchterm, threshold=threshold)


if __name__ == "__main__":
    app.run(debug=True)
