### **Learning Objectives**:

By the end of this lesson, students will:

1.  Understand the purpose of Flask-Limiter for rate limiting in APIs.
    
2.  Understand the purpose of Flask-Caching for caching in APIs.
    
3.  Learn how to implement Flask-Limiter and Flask-Caching in a Flask API following the Application Factory Pattern.
    
4.  Be able to use Flask-Limiter and Flask-Caching on a specific blueprint (e.g., a user blueprint).
    

### **Section 1: Introduction to Flask-Limiter**

#### **What is Flask-Limiter?**

*   Flask-Limiter is an extension that provides rate limiting to Flask applications, which is essential for preventing abuse by limiting the number of requests a client can make to the API. This allows us to protects our API from malicious attacks like DDOS attacks, which are repetitive requests (100's even 1000's per second) used to overwhelm your server.
    

**Use Cases**:

*   Protecting routes from excessive traffic
    
*   Throttling requests to sensitive endpoints (login, registration, etc.)
    

#### **Installing Flask-Limiter**

`   pip install Flask-Limiter   `

#### **How Flask-Limiter Works**

*   Flask-Limiter allows you to set limits per route or globally. The rate limit syntax follows a simple format like 5 per minute or 100 per hour.
    

### **Implementing Flask-Limiter in a Flask API**

#### **Project Structure**

```
/project
├── /application
│   ├── __init__.py 
│   ├── extensions.py <--- Where we will initialize 3rd party API's
│   ├── /blueprints
│   │   ├──/user
│   │      ├──__init__.py  
│   │	   ├── routes.py  
│   │	   └── userSchemas.py
│   └── models.py
├── app.py
└── config.py

```

#### **Navigate to extensions.py**

*   Reminder, this file will hold all third-party extension instances.
    
```
# application/extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address) #creating and instance of Limiter
```

#### **Initialize Flask-Limiter in the Application Factory**

*   Modify the \_\_init\_\_.py file to include Flask-Limiter initialization.
    

```
# application/__init__.py
from flask import Flask
from app.models import db
from .blueprints.user import user_bp
from .extensions import ma, limiter

def create_app(config_name):
    app = Flask(__name__)
    
    # Load app configuration
    app.config.from_object(f'config.{config_name}')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    
    return app
```

#### **Apply Flask-Limiter to a Route**

*   In the member blueprint, apply rate limiting to specific routes.
    
```python
# app/blueprints/user/routes
from flask import jsonify
from app.blueprints.member import member_bp
from app.models import member
from app.extensions import limiter
from .schemas import member_schema, members_schema

@member_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")  #A client can only attempt to make 3 members per hour
def create_member():
    try: 
				# Deserialize and validate input data
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	#use data to create an instance of member
    new_member = member(name=member_data['name'], email=member_data['email'], password=member_data['password'])
    
	#save new_member to the database
    db.session.add(new_member)
    db.session.commit()

	# Use schema to return the serialized data of the created member
    return member_schema.jsonify(new_member), 201
```


#### **Testing Flask-Limiter**

*   Using Postman we could test /users POST endpoint multiple times in rapid succession and observe after POSTing 3 times we would meet our limit.
    

### **Introduction to Flask-Caching**

#### **What is Flask-Caching?**

*   Flask-Caching is an extension to cache data and improve performance in Flask applications by storing the results of expensive or frequently accessed API calls. By storing frequently accessed data to a cache, when that data is requested you can simply reach into the cache for the information, instead of performing a full database query. This increases the speed at which the data is returned and also prevents repetitive calls to the db.
    

**Use Cases**:

*   Caching API responses to reduce database queries
    
*   Improving response times for high-traffic endpoints
    

#### **3.2 Installing Flask-Caching**

`   pip install Flask-Caching   `

#### **3.3 How Flask-Caching Works**

*   Flask-Caching supports various caching backends, such as in-memory, Redis, or file-based caches.
    

### **Section 4: Implementing Flask-Caching in a Flask API**

#### **4.1 Create and Configure extensions.py**

*   Add the Flask-Caching instance to the extensions.py file.
    
```python
# app/extensions.py
from flask_caching import Cache

# Add to existing extensions
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
```

#### **4.2 Initialize Flask-Caching in the Application Factory**

*   Modify the \_\_init\_\_.py file to include Flask-Caching initialization.
    

```python
# app/__init__.py
from flask import Flask
from app.models import db
from .blueprints.user import user_bp
from .extensions import ma, limiter, cache

def create_app(config_name):
    app = Flask(__name__)
    
    # Load app configuration
    app.config.from_object(f'config.{config_name}')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    
    return app
```

#### **4.3 Apply Flask-Caching to Routes**

*   In the member blueprint, cache specific routes.
    
```python
# app/blueprints/user/routes
from flask import jsonify
from app.blueprints.user import user_bp
from app.models import User
from app.extensions import cache
from .schemas import user_schema, users_schema


@user.route('/users', methods=['GET'])
@cache.cached(timeout=60)
def get_users():
    query = select(User)
    result = db.session.execute(query).scalars().all()
    return users_schema.jsonify(result), 200 #use users_schema to serialize many users
```


#### **Testing Flask-Caching**

*   Now this will be slightly harder to notice, but in postman when you make the first request, that request will go all the way into the database to grab the data. It will then store that data to a cache so when you make any subsequent calls within 60 seconds it will reach into the cache instead. So if you were to test these calls, the first one would be slower than the ones following.