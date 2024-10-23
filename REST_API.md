### Building a RESTful API

#### 1\. **Define Resources**

Identify the core entities in your application, such as users, products, or orders.

#### 2\. **Structure URIs**

Use nouns in URIs (e.g., https://api.example.com/products). Avoid actions in URIs.

#### 3\. **Use Proper HTTP Methods**

#### When creating routes we can reuse the same endpoint (ex. /users), and create divergence using different Methods

*   **GET /users**: Retrieve all products.
    
*   **POST /users**: Create a new product.
    
*   **PUT /users/1**: Update a product with ID 1.
    
*   **DELETE /users/1**: Delete a product with ID 1.
    

#### 4\. **Status Codes**

*   **200 OK**: Success.
    
*   **201 Created**: Resource created.
    
*   **400 Bad Request**: Client error.
    
*   **404 Not Found**: Resource not found.
    
*   **500 Internal Server Error**: Server error.
    

### **Introduction to Marshmallow**

Marshmallow is a popular library used in Flask applications to serialize and deserialize data, as well as for input data validation. It works well with ORMs like SQLAlchemy but is not limited to them.

*   **Serialization**: Converts complex objects (like SQLAlchemy model objects) into simpler data types (like JSON) to send over the network.
    
*   **Deserialization**: Converts raw input data into application-specific data structures, such as populating a SQLAlchemy model.
    
*   **Validation**: Ensures that input data conforms to expected types and formats before processing.
    

#### **Installation:**

`   pip install flask-marshmallow, marshmallow-sqlalchemy   `




### **Marshmallow Schemas**

Are utilizing the marshmallow-sqlalchemy package we can actually generate Schemas using our models to create an auto schema

#### **User Schema Example:**

```python
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
```

**Explanation:**

*    Utilizing our Member model we are able to create an auto schema which can be used Serialize and Deserialize Member objects, aswell as validate that incoming data has all the information required
    

### **Flask API with CRUD Endpoints**

We will now implement the CRUD (Create, Read, Update, Delete) operations for the Member model. We'll use our current Flask app for the API and Marshmallow for serialization, deserialization, and validation.

**Endpoints**
- Create a member
- Read a single member
- Read all members
- Update a member
- Delete a Member