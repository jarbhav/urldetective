from flask import Flask, render_template, request
import requests
import pickle
from preprocessing import *
from deepchecks import *

app = Flask(__name__)
model = pickle.load(open('RFCmodelfin.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    # RFC Model
    sus_url = request.form.get('suslink')

    try:
        if "http" in sus_url or "https" in sus_url:
            suslink = sus_url
        else:
            suslink = "http://" + sus_url

        response = requests.get(suslink)
        testing = applyall(sus_url)
    
        p_rfc = model.predict(testing)
        output_rfc = p_rfc[0]
    
        if (output_rfc == 'good'):
            deepresults = deepcheck(sus_url)
            if (deepresults < 0 and deepresults >= -2):
                output = "Phishy"
            elif (deepresults < -2):
                output = "Malacious"
            else:
                output = "Safe"
        else:
            deepresults = domain_check(sus_url)
            if (deepresults == 1):
                pathres = check_path(sus_url)
                if(pathres > 0):
                    output = "Safe"
                else:
                    output = "Phishy"
            else:
                output = "Malacious"

    except requests.ConnectionError as exception:

        output = "Invalid (Please Check your spelling)"

    return render_template('index.html', prediction_text='The URL is {}'.format(output))

'''
@app.route('/results', methods=['GET', 'POST'])
def showres():
    data = request.get_json(force=True)
    prediction = model.predict()
'''
if __name__ == '__main__':
    app.run(debug=True) 