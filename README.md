
<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="images/logo2.png" alt="Logo" height="100" width="150">
</div>

# Curry & Crumbs 

A full stack Django application that serves as a food blog.
Built with content recommendation, user engagement tracking, and a simple API layer for extensibility.

## Built With

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563d7c?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Features

- ### User Registration & Authentication
    -  Uses Django's builtin `UserCreationForm` for registration
    -  Implements Django's `AuthenticationForm` for secure credential handling.
    -  Certain pages that require authentication are protected using the `@login_required` decorator.

- ### User Engagement Tracking using views and likes
    - Likes are a `ManyToManyField` on the `Post` model linked to `User`. Appears as a toggle on each post.
    - Views are recorded as instances of a `PostView` model.

- ### Search/Filter based on categories and tags
    - Implemented on post titles, tags and categories using Django `Q` objects for multi-field filtering.
  
- ### Content Recommendation based on User Activity
    - Recommends posts using a weight-based scoring algorithm:
        - User actions are assigned scores, with some having higher weight than others. (eg. +3 for a like, +1 for a view)
        - Also incorporates collaborative signals: if another user has similar activity, it gets a higher weight.
        - Top 4 posts with the highest cumulative scores are displayed as recommended.
    - **Requires prior user interaction for meaningful results.**
  
- ### RESTful API built using Django REST Framework, with the following endpoints:

    - `/api/posts/` – List all blog posts

    - `/api/posts/<id>/` – Retrieve a single post

    - `/api/<id>/comments/` – Submit and retrieve comments

    - `/api/categories/` – Get all categories


## Roadmap

- [ ]  User Profile showing likes, comments and saved posts 
- [ ]  Save Posts feature
- [ ]  Include comments as a factor in recommender system
- [ ]  Light/dark mode toggle
- [ ]  UI Improvements

## Known Issues
 - Trying to like a post without being logged in results in an unhandled error.

 - Opening the "Recommended" page without having viewed or liked any posts results in empty recommendations (no fallback/default content).

## References

- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- Youtube:
     - [Django Tutorial](https://www.youtube.com/playlist?list=PL0Zuz27SZ-6NamGNr7dEqzNFEcZ_FAUVX) by Dave Gray
     - [DRF Tutorial](https://www.youtube.com/playlist?list=PL-2EBeDYMIbSXhV8FMC1hVD32Fi6e4l2u) by BugBytes
 - [Django Blog Tutorial](https://realpython.com/build-a-blog-from-scratch-django/)
