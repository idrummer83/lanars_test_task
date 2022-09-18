# lanars_test_task
Develop a REST API for a portfolio publication site.


Where:

  All users are able to:
  
    ● signup
    ● see image feed (image, image description, portfolio name that
    contains this image) ordered by creation time
    ● search image by name/description/portfolio name that contains
    this image
    ● leave the comments for the picture
    
  Registered user should be able to:
  
    ● login, logout
    ● create portfolios
    ● have several portfolios
    ● upload image in his portfolios
    ● edit, delete own profile
    ● edit, delete own portfolios
    ● edit, delete own images
    
  Portfolio:
  
    ● Should contain name, description, images
    Image:
    ● Should contain name, description, comments
    Key requirements:
    ● Should be implemented Error Handler with next statuses 400,
    401, 403 and 404
    ● Should be implemented request validation
    ● Project should contains db migration files
    
  Use the following technologies:
  
    ● PostgreSQL
    ● Python as a server technology (Django and Django REST framework)
