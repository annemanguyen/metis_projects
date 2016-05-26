from flask import Flask, url_for, redirect, request, render_template
import pickle
import random

c3dictfile = open('/home/amn34/metis/stuff/c3dict.pkl','r')  
cdict = pickle.load(c3dictfile)

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods=['POST'])
def text():
   
	lines = int(request.form['lines'])
	
	while True:
		start = random.choice(cdict.keys())
		if (start[0][0].isupper()) or (start[0][0] == '"'):
			break

	output = []
	output.extend(start)

	startposs = [i for i in cdict.keys() if (i[0],i[1]) == (start[1],start[2])]

	output.append(random.choice(startposs)[2])

	punct = ['?','.','!','?"','."','!"']

	for i in range(1,lines):
	    nextword = (output[-3],output[-2], output[-1])
	    if nextword in cdict.keys():
	        output.append(random.choice(cdict[nextword]))
	        
	while output[-1][-1] not in punct:
		nextword = (output[-3], output[-2], output[-1])
		if nextword in cdict.keys():
			output.append(random.choice(cdict[nextword]))

	result = ' '.join(output)

	return render_template('text.html', result=result)

if __name__ == '__main__':
	app.run()