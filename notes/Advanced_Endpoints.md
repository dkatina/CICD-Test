### Lesson Plan: Advanced SQLAlchemy Queries Utilizing Table Relationships

#### **Prerequisites**:

*   Basic knowledge of Flask and SQLAlchemy
    
*   Understanding of database models and relationships (one-to-many, many-to-many)
    

### **Learning Objectives**:

By the end of this lesson, students will:

1.  Understand how to utilize relationships between tables to write more complex SQLAlchemy queries.
    
2.  Be able to query related models using one-to-many and many-to-many relationships.
    
3.  Incorporate advanced schemas to capitalize on our relationship attributes
4. Learn how to use query parameters to pass information through the url
5. Understand the concept of pagination
    

**Recap of SQLAlchemy Relationships**
-------------------------------------

SQLAlchemy supports several types of relationships between tables:

*   **One-to-many**: One record in a table can relate to many records in another table (e.g., one customer can have many service tickets).
    
*   **Many-to-many**: Many records in one table relate to many records in another table (e.g., mechanics can work on multiple tickets, and tickets can have multiple mechanics)
    

In SQLAlchemy we can give our models relationship attributes that return a list of the objects they are related to.

**The Main Takeaway:**

The main takeaway is through these relationships, when we query an object, we get to access it's associated objects in the form of a python list. Lists are one of our most fundamental datatypes in python and because we get to treat these relationships as list, that opens them up to all of our built in list operations; .append(), .remove(), len(), .sort() etc. Using these operations we can create algorithms to edit our relationships, and give us insights into our data such as activity, popularity, demographics and so on.

**Creating Many-to-Many Relationships**
------------------------------------------



*   Modifying our Create Loan route, to add books to the loan when the loan is created
    
    *   Adding Books required .append()
        
---

**Creating Insightful endpoints Capitalizing on our Relationships**
-------------------------------------------------------------------

 Before we dive into creating these endpoints, one of the key concepts in being able to present insights, is to be able to organize your data. One of the easiest ways we know how to organize data in python is by sorting it with .sort(). Now .sort()'s base functionality is limited to sorting in ascending order (lowest-highest), however we can modify this by adding in sorting keys, which are functions we can create to specify how the data is sorted.

#### **Introduction to Lambda Functions**

**Definition:**

*   Lambda functions in Python are small functions defined with the lambda keyword. They are often used when a simple function is required for a short period and writing a full function with def would be overkill.
    

**Syntax:**

`   lambda parameters: expression   `

*   **Parameters:** Function variables
    
*   **Expression:** A single statement evaluated and returned by the lambda function.
    

**Example:**

```   
add = lambda x, y: x + y
print(add(3, 4))
# Output: 7 
```

*   x and y are our parameters
    
*   x + y is our expression who's value is returned
    

#### **Sorting with .sort() and Using Lambda Functions**

**Sorting in Python:**

*   The .sort() method is used to sort lists in place, and the sorted() function returns a new sorted list.
    

**Default sorting:** Without any additional arguments, .sort() will sort the list based on the default order (typically ascending order).

**Sorting Example:**

```   
numbers = [3, 1, 4, 2]
numbers.sort()  print(numbers)  
# Output: [1, 2, 3, 4]
```

**Custom Sorting with Keys:**

*   You can pass a key argument to .sort() or sorted() to customize the sorting behavior. The key argument expects a function that returns the value to be used for comparison.
    
*   **Lambda functions** are frequently used as key arguments due to their simplicity.
    

**Example: Sorting by length of strings:**

```   
words = ['apple', 'banana', 'pear', 'kiwi']
words.sort(key=lambda word: len(word))
print(words)  
# Output: ['pear', 'kiwi', 'apple', 'banana']
```

Here, the lambda function is used on each word in the list and returns the length of each string, so the list is sorted by the lengths of the words.

**Implementing Sorting Keys to make Insightful queries.**

Creating an endpoint to allow users to query the most popular books. Utilizing the book's relationship to loans we can sort the books list based on which books have been loaned out the most.

---

**Incorporating Query Parameters in our Endpoints**
---------------------------------------------------

**What are Query Parameters?**

*   Query parameters are key-value pairs appended to the end of a URL after the ? symbol. They provide additional information to the server and are often used to filter, sort, or limit the results in API requests.
    

**Structure:**
A URL with query parameters looks like this.

`https://example.com/items?item_name=phone`

*   The query parameter here is item\_name and the value we're assigning is phone. This could be used to search our database for items with "phone" in the name or description.
    

**Usage in APIs:**

*   Query parameters make it easier to customize responses from an API without changing the endpoint itself.
    
*   By adding query parameters we can send information to our server, like a search term, category filter, or sort command, without having to send a full JSON payload.
    

**Applying a query parameter to refine our searching**

Lets incorporate query parameters, to allow for a search term to pass through the URL. Then, utilize this search term to query the database for books that include the search term in the title.

---

**Efficient Data retrieval with Pagination**
--------------------------------------------

**What is Pagination?**

*   Pagination divides large sets of data into manageable chunks or pages. This is crucial in APIs to prevent overwhelming users with too much data at once.
    
**Page and Page Size:**

`https://api.example.com/products?page=2&page_size=10`

We can set up query parameters to take in attributes for Page# and How many items per Page, We can then use the attributes to divide up our data set and produce specified pages of data.
    

**Why Use Pagination?**

*   Pagination enhances performance and user experience by delivering results in smaller, more digestible portions, and reduces server load.
    

**Extending a Bulk Search endpoint to allow for pagination.**

SQLAlchemy has a built-in pagination query, that will keep track of the pages and which Items should be displayed on which page.