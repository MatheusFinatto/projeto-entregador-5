<h1>projeto-entregador-5 / Games Library </h1>

<p>Welcome to our Games Library, a Flask app that utilizes the IGDB API to display information about games. Whether you're a games buff or simply looking for something new to play, our app has you covered!</p>

<h2>How to Run the App</h2>
<ol>
    <li>Check if Python and pip are already installed on your machine.  </li>
    <br>
    <ul>
        <li>To check if Python is installed, open a terminal or command prompt and run the command <code>python --version</code>. If Python is not installed, you can download it from the official Python website (https://www.python.org/downloads/), which includes pip by default.</li>
        <li>To check if pip is installed, run the command <code>pip --version</code>. If pip is not installed, you can download and install it from the official website (https://pip.pypa.io/en/stable/installation/) or by using your operating system's package manager.</li>
    </ul>
    <br>
    <li>Download the app's repository to your local machine.</li>
    <li>Open your terminal and navigate to the project directory.</li>
    <li>Run the command <code>pip install -r requirements.txt</code> to install the necessary dependencies.</li>
    <br>
    <ul>
        <li>If that fails, open the  <code>requirements.txt</code> file and run the command <code>pip install</code> followed by the dependencies' names.</li>
        <li>At the moment this is being written, the command would be <code>pip install Flask requests Flask_Session pyyaml ua-parser user-agents</code>, but more dependencies may be added by the moment you are reading it.</li>
    </ul>
    <br>
    <li>Run the command <code>flask run</code> to start the development server.</li>
    <li>Once the server has started, open your web browser and go to the link where the app is being hosted. For
        example, the link might be <code>http://127.0.0.1:5000/</code>.</li>
</ol>
<p>By following these simple steps, you'll be able to run the app locally on your machine.</p>

<h2>API Data - Develop tools </h2>

<h3>Required Access Token:</h3>
<h4>URL:</h4>
<p> https://id.twitch.tv/oauth2/tokenclient_id=tvpgyurlv8vc88kd9dzum9s0ldlbf2&client_secret=mnqonlmblqkyvdzuja2gv8ucls3tt6&grant_type=client_credentials</p>
<h4>Params:</h4>
<p>client_id: tvpgyurlv8vc88kd9dzum9s0ldlbf2</p>
<p>client_secret: mnqonlmblqkyvdzuja2gv8ucls3tt6</p>
<p>grant_type: client_credentials</p>

<h3>Current Access Token:</h3>

<h4>"access_token": "f1fzl61lle5vii2zwca6x2ghswne5z",</h4>
<h4>"expires_in": 4807704,</h4>
<h4>"token_type": "bearer"</h4>

<h3>Request Headers:</h3>
<h4>Client-ID: tvpgyurlv8vc88kd9dzum9s0ldlbf2</h4>
<h4>Authorization: Bearer f1fzl61lle5vii2zwca6x2ghswne5z</h4>
<h4>URL: https://api.igdb.com/v4/[ENDPOINT]</h4>

<h2>How to access database</h2>
<p>Download DB Browser (SQLite) and open the database.db file</p>


