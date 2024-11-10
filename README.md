# Decipher
#### Video Demo:  https://youtu.be/Nf0N3Zf87Hw>
#### Description: Decipher is a web application made using Flask, it allows users to input code they do not understand and then explains that code using OPEN AI's API.
#### Technologies Used: I have used Flask for this along with an SQL database, and HTML and CSS files.


# Flask Session
#### Flask sessions are a way for the server to store local information about a user.
#### flask_session is a file which stores these sessions.

# Static
#### There are 2 png files stored in this folder, one is favicon.png which is the favicon seen on top of the website, home.png is the picture used in the initial launch of the application.
#### styles.css stores the "styles" of the webpage, ranging from colors to fonts to hover animations etc...

# Templates
#### This Folder contains all of the HTML files which are the "Structure of the actual page itself"
## account.html
#### This HTML file is what the user sees when they first run the flask file, it contains a H1 for the title "Decipher", and then some bootstrap code to layout the page nicely, the image "home.png" is displayed on the right and a title and text is displayed on the left, below that are the login and register button.
## error.html
#### This HTML file is what is outputed to the user if there are any errors, e.g. the user tries to register with an email which is already taken. It makes use of Jinja therefore a string is passed to the html file from app.py if a certain condition is met, and then that string is displayed in a nice aesthetic box.
## login.html
#### This HTML file is shown to the user when the login button is pressed from account.html, after the user registers for an account or when the users clicks on "Login Here" on register.html, in summary it is just a form which asks for the email and password and then allows the user to login.
## register.html
#### This HTML file is similar to login.html however it requires the user to type in their name and asks for the password twice.
## home.html
#### This HTML file uses Jinja syntax as well because it is a layout after the user has logged onto the platform. The h1, navbar and footer will always remain there after you are logged on and the only content which gets changed is in the middle. This also uses bootstrap, at the there is a h1 for the title, there is a navbar with links to /explain, to /history and to logout. In the footer there is information about Decipher and an easter egg when the user clicks on the link.
## explain.html
#### This HTML file expands home.html, it consists of a form with textarea inside of it and a submit button which allows the user to submit any code that they do not understand. I have used target="_blank" so that the explanation is in a new tab and I have set the textarea element resize to none so that users cannot change the size of the box, upon submitting users are redirected to either error.html or explained.html depending on the outcome. If the user enters code they have already entered in the past they get an error, this is to reduce wastage of tokens for the API. If it is new code the API request is sent and explained.html is displayed
## explained.html
#### This HTML file also expands home.html, it has a h2 which says "THE EXPLANATION" and a div in which jinja is used to output the string which contains the explanation give from OPENAI
## history.html
#### This HTML file again expands home.html and it contains a table with black borders, this contains the code which is indented, the explanation and the date and time when the request was sent.

# Other Main Files

## project.db
#### This is the database I have made for my application, it consists of 2 tables: accounts and history. Accounts contains the information about people who create accounts: their account id, name, email, hashed password. History contains: the id for the explanation, the code, the explanation, the user_id of who made the request and the date/time.

## app.py
#### This is the python file which is the application's root, db is a variable created which is referring to the database project.db, the next 3 lines are about session configuration: we set the sessions to be stored on the local filesystem and they are not permanent and then they are initialised.
### Login_Required Function
#### This Function requires the user to be logged on to access certain html pages, e.g. the user cannot access explain.html unless logged on.
### after_request Function
#### this is a function to ensure that the responses are not cached
### account Function
#### This function renders account.html when the request method is GET and the route is "/" this is also the default page the user goes to
### login Function
#### This function is ran when the user routes to "/login", the sessions are cleared firstly just as a step just to make sure there are no sessions on the user's local device, if the request method was GET then the login.html page is rendered back to the user, if it is a POST then the email and password are requested from the form which was submitted on login.html and stored in their variables, if somehow the email and password are empty "error.html" is rendered to the user with a custom message inside it, then a SQL query is done to check whether or not a user is registered or not, if not then "error.html" is rendered again, and then we hash the password using a function from werkzeug.security and check it against the hashed password stored in our database for the user, if the passwords do not match "error.html" is rendered with a custom message. The session then is given the user's id from the database and the user is redirected to "/explain"
### register function
##### if the route is "/register" then this function is executed, if the request method was GET then "register.html" is returned/rendered back to the user. If the request method was POST then variables are made to extract the information that the user has inputted into the input elements in the form in "register.html". If the user does not fill an input then an error is returned, if the password is not equal to the password that needs to be repeated another error is shown. If all of this is ok then the password is hashed into a using the generate_hash function into a variable called hashed_pass, an SQL query is ran to find if the email is already taken and if it is an error is returned through "error.html", if not taken then the information given by the user is inserted into the accounts table in the database, and finally you are redirected to "/login"
### explain function
#### if the route is "/explain" and if the user is logged in (because of @login_required) then this function is ran and the user's id is stored in a variable from session because we previously stored the user's id in login. If the request method was GET then "explain.html" is rendered back to user. If the request method was a POST then i make a variable to store my API key for OPENAI, I also extract the code the user inputted into the textarea box in "explain.html", if the text was empty then an error is displayed to user, if the user has not inputted this code before then we use the OPENAI api to run a request to its servers and we store the result in a variable called response, we then only choose a certain part of response by doing "response = (response["choices"][0]["text"])" because we get given a lot of extra information. We then return explained.html to the user with the response in a div. If the piece of code the user inputted was something they have already inputted before then we would return an error. I have done this to stop users from wasting tokens which are given to me by OPEN AI.
### history function
#### if the route is "/history" and if the user is logged in then the information from the history table in project.db is put into a variable called info, then "history.html" is returned with this info inside it to pass it onto the html page to then use jinja to add this information in the table.
### logout function
#### if the route is "/logout" and the user is logged in then by running this function the user gets logged out by clearing the session and return to "/"
