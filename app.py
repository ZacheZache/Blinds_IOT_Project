from flask import Flask, render_template
import dynamodb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def get_users():
    users = dynamodb.get_all_users()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run()
