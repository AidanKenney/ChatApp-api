# :octocat: The Feed: An Online Forum :octocat:

The Feed is a message board application for users to create posts and respond to 
other users through comments in an open forum environment. I built this app as the V1 of
an ongoing social media project that will include chat messaging through Django 
Channels in future iterations. 

## Important Links

- [Deployed API](chatapp-api-django.herokuapp.com/)
- [Deployed Client](aidankenney.github.io/chatapp-client/)
- [Client Repository](https://github.com/AidanKenney/ChatApp-client)


## Planning Story

This project grew out of an interest in building a simple social application with
user-generated content -- akin to sites like Reddit, Craiglist, or early Facebook. My initial
impulse was to create a chat room, but within the time limits of this project, and being my
first experience with Django and second with React, I realized that a message board was a more 
realistic V1. I began by building the API with Django and Django-Rest-Framework, and was able
to build off of our lessons in Django to create Comments on Posts by using two foreign key fields
on the Comment Model. I also found it pleasantly simple using Python to sort my index responses
by the date posts were created. After this experience, I have gained a much better understanding of and 
appreciation for the modular framework of Django, and am excited to continue working with it. 

One issue I created for myself with Django was in updating my serializers so that more specific information could
be accessed on the front end -- usually the user's email for post and comment attribution. When
I began using serializers on the Post/Comment owner field, I did not realize that I had altered what the API was now expecting from the front end. 
I wanted to be able to create Comments with an owner simply indicated by an ID number, but also wanted to 
be able to read the email belonging to that owner on the front end. I found that I could use two different
serializers to meet these needs -- one for creating and updating, and one for reading. After I
had fixed this bug, it was smooth sailing with Django. 

***

### Unsolved Problems
I still need to find a way to make votes persist past page refreshes/site visits.
One option would be to create an unauthenticated patch route for votes made 
by users who don't own the post. Another option might be to create votes as its own entity like
a comment, then store these on a given post or comment. I would also need to store the voter's ID on the post
so that they cannot vote again and again. I was unable to dive into this in
the time remaining towards the end of the project, but I am excited to return to
this challenge after the course. 

As far as remaining reach goals, I still want to create a chat feature, order the feed
based on number of votes, and integrate a third-party-API to make an 'Article of the Day' feature, 
where everyday a new article would serve as a starting point for conversation. 

## Installation
1. Clone the repository: [Backend Github Repository](https://github.com/AidanKenney/ChatApp-api)
2. In the root directory of the backend project, type `pipenv shell` to start virtual environment, then `pipenv install` to install dependencies. 
3. Create a psql database for the project. Type 'psql' to get into interactive shell. Run 'CREATE DATABASE "your-DB-name";'
3. Type the following in the same root directory to start the server (take note of your python version before running command): `python3 manage.py runserver`
4. Clone the repository: [Front Github Repository](https://github.com/AidanKenney/ChatApp-client)
5. In the root directory of the front end project, type `npm i`.
6. Type the following in the same root directory: `npm start` to start the server.

***

### User Stories
    1.  As a signed in user, I would like to make a message board post.
    2.  As a signed in user, I would like to see all posts.
    3.  As a signed in user I would like to comment on a post. 
    4.  As a signed in user, I would like to update my own comments.
    5.  As a signed in user, I would like to delete my own comments and posts.

### Technologies Used
- Python
- Django / Django-Rest-Framework
- SQL/PostgresQL
- JavaScript
- React / React-DOM-Router / React-Bootstrap
- axios
- Passport JS
- Bcrypt
- CSS/Sass
- Styled-Components
- MomentJS

## Routes and Paths
| Verb   | URI Pattern            | Controller#Action |
|--------|------------------------|-------------------|
| POST   | `/sign-up/`             | `users#signup`    |
| POST   | `/sign-in/`             | `users#signin`    |
| PATCH  | `/change-pw/`           | `users#changepw`  |
| DELETE | `/sign-out/`           | `users#signout`   |
| GET    | `/posts/`               | `posts#index`       |
| GET    | `/posts/:id/`          |`posts#show`         |
| PATCH  | `/posts/:id/`           | `posts#update`    |
| POST  | `/posts/`               | `posts#create`    |
| DELETE | `/posts/:id`           | `posts#delete`    
| GET    | `/comments/`            | `posts#index`        |
| GET    | `/comments/:id/`        |`comments#show`       |
| PATCH  | `/comments/:id/`        | `comments#update`    |
| POST  | `/comments/`             | `comments#create`    |
| DELETE | `/comments/:id`          | `comments#delete`   |


## Images

#### ERD:
![Imgur](https://i.imgur.com/oDVZE2u.png)
