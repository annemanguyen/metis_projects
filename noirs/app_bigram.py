from flask import Flask, url_for, redirect, request, render_template
import pickle
import random

cdictfile = open('/home/amn34/metis/stuff/cdict.pkl','r')  
cdict = pickle.load(cdictfile)

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods=['POST'])
def text():
   
	lines = int(request.form['lines'])
	
	start = random.choice(cdict.keys())

	while (start[0][0].islower()) or (start[0][0] != '"'):
		start = random.choice(cdict.keys())

	output = []
	output.extend(start)

	startposs = [i for i in cdict.keys() if i[0] == start[1]]

	output.append(random.choice(startposs)[1])

	punct = ['?','.','!','?"','."','!"']

	for i in range(1,lines):
	    nextword = (output[-2], output[-1])
	    if nextword in cdict.keys():
	        output.append(random.choice(cdict[nextword]))
	        
	while output[-1][-1] not in punct:
		nextword = (output[-2], output[-1])
		if nextword in cdict.keys():
			output.append(random.choice(cdict[nextword]))

	result = ' '.join(output)

	return render_template('text.html', result=result)

if __name__ == '__main__':
	app.run()