from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline():
    # Mockup data
    posts = [
        {'Majed': 'manager1', 'rate': '30/50'},
        {'Nizar': 'manager2', 'rate': '6/50!'},
        {'Nour': 'manager3', 'rate': '17/50'},
    ]

    return render_template('timeline.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
