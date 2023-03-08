## ozymandias 

Advanced Python and Django backend for a manufacturing process management dashboard

---

## Goals 

  - implement user authorization / authentication using OAuth2 and OpenID
  - runs on Docker container and started with single command `docker-compose up`
  - running application to be reached in the browser at [docker host]:8080 
  - provide a RESTful API to CRUD relevant objects 
  - admin available at [docker host]:8080/admin
  - unit tested with minimum 75% code coverage
  - provide Swagger API documentation
  - PostgreSQL database backend
---

## Instructions 

**Unit Tests**
1.  `$ cd ozymandias/project`
2.  `$ ./manage.py test`

**Unit Tests (with coverage.py)**
1.  `$ cd ozymandias/project`
2.  `$ coverage run manage.py test`
3.  `$ coverage report`

---

Written by Antonio Redekop