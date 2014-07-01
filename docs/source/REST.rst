REST (Representational state transfer)
======================================

For some good primers on REST, have a look at the following links.

* Roy Felding in Chapter 5 of his dissertation on network based software architectures_
* REST_
* `Best Practices for Designing a Pragmatic RESTful API`_
* `HTTP status codes and reason phrase`_

The Basics
----------

The key principles of REST involve separating your API into logical resources. These resources are manipulated using HTTP requests where the method (GET, POST, PUT, PATCH, DELETE) has specific meaning.


+---------+------------+--------------------------------------------------------------+------+------------+
| Method  | Scope      | Description                                                  | Safe | Idempotent |
+---------+------------+--------------------------------------------------------------+------+------------+
| GET     | collection | Retrieve all resources in a collection                       | Yes  | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| GET     | resource   | Requests a specific representation of a resource             | No   | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| PUT     | resource   | Create or update a resource with the supplied representation | No   | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| DELETE  | resource   | Deletes the specified resource                               | No   | No         |
+---------+------------+--------------------------------------------------------------+------+------------+
| POST    | collection | Submits data to be processed by the identified resource      | Yes  | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| HEAD    | collection | Retrieve all resources in a collection (header only)         | Yes  | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| HEAD    | resource   | Similar to GET but only retrieves headers and not the body   | Yes  | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+
| OPTIONS | any        | Returns the methods supported by the identified resource     | Yes  | Yes        |
+---------+------------+--------------------------------------------------------------+------+------------+

Principles
----------

* A RESTful API should be stateless.
* Caching: E-tag or LastModified

Resources
---------

Resources should be nouns (not verbs!) that make sense from the perspective of the API consumer.  For example, some of our nouns, would be Track, Station, Artist, Album, Ringtone, etc.

Once you have your resources defined, you need to identify what actions apply to them and how those would map to your API. RESTful principles provide strategies to handle CRUD actions using HTTP methods mapped as follows:

* GET /ringtones/recommended - Retrieves a list of ringtones
* GET /ringtones/310068 - Retrieves a specific ringtone
* POST /thumbs - Creates a new ticket
* PUT /thumbs/3150504 - Updates thumbs for stations or tracks
* PATCH /thumbs/3150504 - Partially updates stations or tracks
* DELETE /thumbs/3150504 - Deletes taste for station or track

Relations
_________

* GET /artists/1233302/stations - Retrieves list of stations the artist is in
* GET /artists/1233302/stations/5 - Retrieves the 5th station that the artist is in
* POST /artists/1233302/stations - Creates a new station featuring that artist
* PUT /artists/1233302/stations/5 - Updates the 5th station that the artist is in
* PATCH /artists/1233302/stations/5 - Partially updates the 5th station that the artist is in
* DELETE /artists/1233302/stations/5 - Deletes the 5th station that the artist is in

Other that don't fit in the CRUD model
______________________________________

* GET /search/artists - Search for a particular artist
* GET /search/tracks - Search for a particular track
* GET /search/stations - Search for stations
* GET /search/ringtones - Search for ringtones

The Rules
_________

* Always use SSL. No exceptions.
* An API is only as good as its documentation.
* Always version your API.
  + URL versioning for major releases (i.e. http://example.com/api/v1/)
  + http custom header for date based sub-versions

* Pretty print by default & ensure gzip is supported
* snake_case api end points
* JSON only responses or throw a 415 Unsupported Media Type HTTP status code
* PUT, POST or PATCH must always return status code 201 and update the Location header
* RFC 6585 introduced a HTTP status code 429 Too Many Requests to accommodate rate limiting.
  + X-Rate-Limit-Limit - The number of allowed requests in the current period
  + X-Rate-Limit-Remaining - The number of remaining requests in the current period
  + X-Rate-Limit-Reset - The number of seconds left in the current period

Loading related resources
_________________________

* You can specify loading a related resource by adding a parameter.  For example:
  + GET /ringtones/310068?include=artists

Filtering, Sorting and Searching
________________________________

* Filtering
  + Use a unique query parameter for each field that implements filtering (i.e. /stations?tag=rock)
* Sorting
  + Similar to filtering, a generic parameter sort can be used to describe sorting rules (i.e. /ringtones?sort=popularity)
* Searching
  + A special parameter can be used to search within a resource.  For example, we could use 'q' for query:  /ringtones?q=drake
* Limiting
  + You can also limit your requests (GET /ringtones?fields=id&q=drake - for just the ringtone ids)

These can also be combined:  /ringtones?q=drake&tag=hiphop&sort=-popularity

Errors
------

Just like an HTML error page shows a useful error message to a visitor, an API should provide a useful error message in a known consumable format.

* The API should always return sensible HTTP status codes
* A JSON error body should provide a few things for the developer - a useful error message, a unique error code (that can be looked up for more details in the docs) and a detailed description.  For example:

.. code:: python

    {
      "code" : 1234,
      "message" : "Something bad happened :(",
      "description" : "More details about the error here"
    }

Validation errors for PUT, PATCH and POST requests will need a field breakdown.  For example:

.. code:: python

    {
      "code" : 1024,
      "message" : "Validation Failed",
      "errors" : [
        {
          "code" : 5432,
          "field" : "first_name",
          "message" : "First name cannot have fancy characters"
        },
        {
           "code" : 5622,
           "field" : "password",
           "message" : "Password cannot be blank"
        }
      ]
    }

HTTP Status Codes
-----------------

200 OK
    Response to a successful GET, PUT, PATCH or DELETE. Can also be used for a POST that doesn't result in a creation.
201 Created
    Response to a POST that results in a creation. Should be combined with a Location header pointing to the location of the new resource
204 No Content
    Response to a successful request that won't be returning a body (like a DELETE request)
304 Not Modified
    Used when HTTP caching headers are in play
400 Bad Request
    The request is malformed, such as if the body does not parse
401 Unauthorized
    When no or invalid authentication details are provided. Also useful to trigger an auth popup if the API is used from a browser
403 Forbidden
    When authentication succeeded but authenticated user doesn't have access to the resource
404 Not Found
    When a non-existent resource is requested
405 Method Not Allowed
    When an HTTP method is being requested that isn't allowed for the authenticated user
410 Gone
    Indicates that the resource at this end point is no longer available. Useful as a blanket response for old API versions
415 Unsupported Media Type
    If incorrect content type was provided as part of the request
422 Unprocessable Entity
    Used for validation errors
429 Too Many Requests
    When a request is rejected due to rate limiting


.. _architectures: http://www.ics.uci.edu/%7Efielding/pubs/dissertation/top.htm 
.. _REST: https://en.wikipedia.org/wiki/Representational_state_transfer
.. _best_practices: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
.. _`Best Practices for Designing a Pragmatic RESTful API`: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
.. _`HTTP status codes and reason phrase`: http://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6.1.1

