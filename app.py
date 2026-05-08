from flask import Flask, redirect, url_for, session, jsonify, render_template_string
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = " "

oauth = OAuth(app)

# Configure GitHub OAuth
github = oauth.register(
    name='github',
    client_id='Ov23li5YXo7SE7AhTXfJ',
    client_secret='0294a66e009f2e57cd0b17108a32848c34ab8db5',

    access_token_url='https://github.com/login/oauth/access_token',

    authorize_url='https://github.com/login/oauth/authorize',

    api_base_url='https://api.github.com/',

    client_kwargs={'scope': 'user:email'},
)

#Home Route
@app.route('/')
def home():
    return '<a href="/login">Login with GitHub</a>'

# Login Route
@app.route('/login')
def login():
    return github.authorize_redirect(
        url_for('callback', _external=True)
    )

# Callback Route
@app.route('/callback')
def callback():
    token = github.authorize_access_token()

    user = github.get('user').json()

    session['user'] = user

    return redirect('/profile')

# Protected API
@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401

    user = session['user']

    return render_template_string("""
    <html>
    <head>
        <title>GitHub Profile</title>
    </head>

    <body style="font-family: Arial; text-align:center; margin-top:50px;">

        <h1>Welcome {{ user['login'] }}</h1>

        <img src="{{ user['avatar_url'] }}"
             width="150"
             style="border-radius:50%;">

        <p><strong>GitHub ID:</strong> {{ user['id'] }}</p>

        <p>
            <strong>Profile:</strong>
            <a href="{{ user['html_url'] }}" target="_blank">
                Open GitHub
            </a>
        </p>

        <p>
            <strong>Account Type:</strong>
            {{ user['type'] }}
        </p>

        <br>

        <a href="/logout">
            <button>Logout</button>
        </a>

    </body>
    </html>
    """, user=user)
# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)

    return "Logged out successfully! <a href='/'>Go Home</a>"

# Run Application
if __name__ == '__main__':
    app.run(debug=True)