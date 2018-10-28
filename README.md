# Finally Understand User Authentication in Django REST Framework

_Talk given at [DjangoConUS 2018](https://2018.djangocon.us/talk/finally-understand-authentication-in/)_

[Slides available here](https://tinyurl.com/djangocon2018-rest-auth).

Traditional Django handles user authentication for us. REST Framework? Not so much. The abundance of choice is overwhelming and typically THE biggest obstacle for newcomers.

This talk is a deep dive on authentication in Django REST Framework. We’ll start with an overview of HTTP and REST APIs before demonstrating how to implement the 4 built-in auth modes and their respective pros/cons. Special attention will be paid to common gotchas such as, Why do I need “both” TokenAuth and SessionAuth? What are JWTs?

Next we’ll implement a real-world REST auth setup that includes user registration, password reset/confirm, social auth, and endpoints for sign up, log in, and log out. The third-party packages django-rest-auth and django-allauth will be used .

By the end of the talk attendees will understand the basics of REST authentication, the tradeoffs involved, and walk away with a working implementation to jumpstart their future projects.
