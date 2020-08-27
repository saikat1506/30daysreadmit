from flask import Flask, render_template, request
import sklearn
import pickle
import warnings
import bz2
import sys
        
def warns(*args, **kwargs):
    pass
warnings.warn = warns
app = Flask(__name__)
@app.route('/')


def loader():
    """
    Load from filename using pickle
    @param filename: name of file to load from
    @type filename: str
    """
    try:
        f = bz2.BZ2File("rm2.pbz2", 'rb')
    except IOError:
        sys.stderr.write('File ' + "rm2.pbz2" + ' cannot be read\n')
        return

    myobj = pickle.load(f)
    f.close()
    return myobj
        
model = loader()

def Home():
    return render_template('index.html')
@app.route("/predict", methods=['POST'])

def predict():
    if request.method == 'POST':
        try:
            time_in_hospital = int(request.form['time_in_hospital'])
            num_lab_procedures = int(request.form['num_lab_procedures'])
            age = int(request.form['age'])
            num_medications = int(request.form['num_medications'])
            num_procedures = int(request.form[ 'num_procedures'])
            number_diagnoses = int(request.form[ 'number_diagnoses'])

            prediction = models.predict([[time_in_hospital, num_lab_procedures, age, num_medications,num_procedures,
               number_diagnoses]])
            output =round(prediction[0],1)
            if output==0:
                return render_template('index.html', prediction_text="The patient will not be readmitted after 30 days")
            elif output==1:
                return render_template('index.html', prediction_text="The patient will be readmitted after 30 days")
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
