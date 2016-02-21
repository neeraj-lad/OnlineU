<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <!-- Navbar -->
        {% block content %}
        {% include "navbar.html" %}

        <!-- About -->
        <h1>Educational Site</h1>
        <p>Site tagline</p>

        {% if "username" in login_session %}
        <!-- Majors -->
        <h2>{{login_session["username"].split(" ")[0]}}'s Majors</h2>
        {% for major in enrolled_majors %}
            <div class="majorBlock">
            <h2>{{major.name}}</h2>
            <p>{{major.description}}</p>
            <p>Progress:</p>
            </div>
        {% endfor %}
        
        <!-- Courses -->
        <h2>{{login_session["username"].split(" ")[0]}}'s Courses</h2>
        {% for course in enrolled_courses %}
            <div class="majorBlock">
            <h2>{{course.name}}</h2>
            <p>{{course.description}}</p>
            <p>Grade:</p>
            </div>
        {% endfor %}

        {% else %}
            <p>Sign in to view your curriculum.</p>
        {% endif %}
        {% endblock %}
    </body>
</html>
