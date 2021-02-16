## Docker Instantiation
- docker-compose up --build -d
- docker-compose up
### service can be invoked on localhost 8000 .

## likeTwitter

### Twitter like API Application in django using djangorestframework
~~~
This application is only the backend part exposing a number of API's given below.
~~~

#### Run migrations by
- python3 manage.py makemigrations
- python3 manage.py migrate
#### Run the server 
- python3 manage.py runserver

### API Endpoints 

#### 1. Create User
~~~
endpoint - http://127.0.0.1:8000/user 
Methods - GET, POST
/user POST Sample request body (all keys necessary) -

{
	"username": "test_user",
	"first_name": "test",
  "last_name": "user",
	"password": "test123",
	"email": "testuser@gmail.com"
}
~~~
Sample responses -
~~~
201 - User successfully created.
400 - Invalid request body.
409 - Username already present.
~~~
Note: - ALL endpoints furthur than this require username in URL for authentication. No API below will work if the user is not logged in.

### 2. Follow a user
~~~
endpoint - http://127.0.0.1:8000/follow 
Methods - POST

{
  "user_name": "test_user",
	"follow_user": "user_xyz"
}
Sample responses -

201 - Followed successfully.
400 - Invalid request or Invalid Username or Can't follow self.
409 - Already followed.
~~~
### 3. Unfollow a user
~~~
endpoint - http://127.0.0.1:8000/follow 
Methods - DELETE

{
  "user_name": "test_user",
	"follow_user": "user_xyz"
}
Sample responses -

201 - Unfollowed successfully.
400 - Invalid request. (missing parameters or username)
400 - Cannot unfollow self.
400 - Invalid username or unfollow_user.
409 - Already unfollowed.
~~~

### 4. Get list of followers
~~~
endpoint - http://127.0.0.1:8000/follow 
Methods - GET

{
  "user_name": "test_user"
}
Sample responses -

200 - Ok.
Exceptions - User doesn't exist. Followers doesn't exist.
~~~


### 5. Create a tweet
~~~
endpoint - http://127.0.0.1:8000/tweet 
Method:- POST
{
  "user_name": "test_user",
	"tweet_text": "Some tweet body."
}
Sample responses -

201 - Tweet created successfully.
400 - Invalid request. (missing parameters or username)
~~~

### 6. Get all the tweets
~~~
endpoint - http://127.0.0.1:8000/tweet?user_name=test_user 
Method:- GET

Sample responses -

200 - List of tweets of given username.
400 - Invalid request. (missing parameters or username)
401 -
~~~


### 7. Delete a tweet using a tweet id
~~~
endpoint - http://127.0.0.1:8000/tweet?user_name=test_user 
Method:- DELETE

{
	"id":1
}
Sample responses -

200 - Tweet deleted successfully.
400 - Invalid request. (missing parameters or username)
404 - tweet with given id not found.
~~~
