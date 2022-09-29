<h1 align="center">
⚡Allops Platform⚡
</h1>

<p align="center">
<a href="https://allops.herokuapp.com/">Visit us👉🏻</a><br><br>
<strong>Allops is a dynamic website which helps proffessionals and students to stay informed about all the academic activities and opportunities available around the globe.</strong>
</p>

## Pages and Components:
* * *
<br>

* **Home/index** page to show our purpose, services and featured opportunities.
* **Signup, Signin** and **Signout**.
* **Compete, Events, Programs, Courses** to categorize opportunities and effective search.
* **Opportunity page** which contains all the details of a single opportunity like dates,official link, overview etc.
* **Saved** which allows user to save the opportunities to apply later
* **Mails** to allow users to subscribe/unsubscribe to our mail notifications.
* **Share** to allow user to share opportunities which are not listed and help community.
* **Profile page** for user options and opportunities shared by user.

<br>

## Installation
* * *
<br>

1. First we need to install the dependencies, install project dependencies by running:

```
pip install -r requirements.txt
```

*Dependencies include django-filters and django multiselectfield, responsible for filters, mails, share and Interest tags of opportunities.*

<br>

2. Make and apply migrations by running:

```
python manage.py makemigrations
```
*followed by:*

```
python manage.py migrate
```

<br>

3. Run your local server by running:

```
python manage.py runserver
```
*copy local host address and paste it in the browser's address bar.*

<br>

4. Signup on the website to access all features and services.
   
<br>

5. Create a super user by running:

```
python manage.py createsuperuser
```
*This step is important to add opportunities to featured list because I think only website's admin should be allowed to add opportunities to the featured list.*

<br>

## Files Information
* * *

<br>

### views.py
* * *

<br>

It contains most useful part of the backend code of the website. The functions of this files are as follows:

<br>

- **index**: for home page features like technology leaderboard and featured opportunities.
- **signup, signin** and **signout**: for createing accounts of users, login and logout.
- **get_opportunities**: which gets all the opportunities according to their type with filters, save and share buttons
- **activity**: It gets a particular opportunity by their id with all the information like title, dates, location, official link, overview, details, save button etc.
- **save_it**: It is used to add opportunities to saved list or remove them for a particular user. It works with Javascript to change the frontend of the website according to the backend operations.
- **saved**: It gets all the opportunities which are saved by user.
- **share**: It allows authenticated users to share opportunities with allops by filling the form. It is also responsible for sending mail notifications to users. As soon as the opportunity is added on the backend it also gets all the users whose any single interests matches with the new opportunity and add them to the recepients list then send all mails at once.
- **profile**: It gets all the opportunities shared by the user and present user with all the necessary options like configure mails, share opportunities, Signout.
- **activate_mails**: It is the form for users to subscribe, unsubscribe or update the mail notifications service by filling up the form. User can also generate multiple mails service with same user but different email id. It shows the unsubscribe options to users who have subscribed with some email id earlier.

<br>

### models.py
* * *

<br>

Contains all the necessary models and choices for Allops website.

<br>

- User model: for user related fields.
- opportunity model: for opportunity related fields like:
    - heading/title
    - description/overview
    - details
    - image
    - link
    - start date
    - end date
    - interest tags
    - location
    - user
    - time
    - type
    - featured
- save model: for allowing user to save opportunities. It's fields:
    - user
    - opportunity/actvity
- mails model: for providing mail services to user.
    - user
    - emai id/mail_id
    - interests/fields
* Choices: 
    - my_types
    - my_fields

<br>

### filters.py
* * *

<br>

Contains code for the interests filter and search by keyword filter.

<br>

- class opportunityFilter:
    - intersts: generate a multipe choice filter for interests tags of opportunities.
    - title: generate a char filter for the headings/title of opportunities.

<br>

### forms.py
* * *

<br>

Contains all the code for generating forms for the Allops. Forms are as follows:

<br>

- signup_form
- signin_form
- share_form
- mails_form

<br>

The form fields are similar to the models like User, opportunity and mails.

<br>

### urls.py
* * *

<br>

Contains code for defining URL paths according to the functions of views.py.

<br>

- signup
- signin
- signout
- Type/<str: type>
- opportunity/<int: item_id>
- save_id/<int: item_id>
- saved
- share
- profile
- mails

<br>

### admin.py
* * *

<br>

Contains models for registering them on the admin site of django. I've registered all the models of the website on django admin site.

<br>

### settings.py
* * *

<br>

The django settings for capstone projects.

<br>

- Added packages: 
    - Django-filters
    - multiselectfield
- Added static files url
- Added smtp configuration

<br>

### Allops.js
* * *

<br>

It contains javascript code used for following features:

<br>

- Select every save button on the page and change the css properties with bakcend operations.
- Select every share button on the page and copy the link of a particular opportunity on the user's clipboard and also add some inner html.
- Automatically submit interest filter form if changed.
- Adds placeholder to the search filter form input.
  
<br>

### styles.css
* * *

<br> 

This file contains CSS for the website with following styles:

- A custom font.
- Media queries to make website responsive.
- Navbar, body, buttons and links styles.
- Opportunity card styles for card front, back, background, preserve 3d, rotate, save, share etc.
- Opportunity page styles for save button, All info. of a opportunity.
- Filters styles for interest and search filter like blurred background div, hover etc.
- blur and visible div card for styling forms, technology leaderboard and filters.
- form field styles like width, height, border etc.
- A Horizontal rule class for div to make div look like faded hr.
- branding styles like font, font-size, images.
- Different opportunity banners styles like background, images, text align etc.
- pagination and profile page styles.
- index page tech leaderboard and services div styles.
- featured div styles.
- Index page footer styles like height, display, background, flex etc.
- Alerts styles for classes 'success' and 'error'.

<br>

### Templates
* * *

<br>

This folder contains all the html files used in the website.

<br>

- **index.html**: Contains html structure for home page of Allops.
    - Heading art/About 
    - services divs and technology leaderboard
    - featured div
    - footer

<br>

- **layout.html**: Contains top structure of the website which remains same for every other page except mail_template.
    - Navbar and dropdown
    - script files, stylesheets
    - Alerts

<br>

- **mail_template.html**: This is the mail template which is used to send users mails about the new opportunity added on the website.

<br>

- **mails.html**: This file contains structure of mails form page to allow user to subscribe, unsubscribe or update mails service.

<br>

- **opportunities.html**: Gets all the opportunity available on website according to their types.
    - page banner for different types.
    - filters panel for interest and search filter.
    - opportunity card divs with information, save, share buttons, links etc.
    - pagination if required.
  
<br>

- **opportunity.html**: The structure used for showing information and features of a single opportunity. Images, heading , dates, tags, location, saved or not etc.

<br>

- **profile.html**: The structure of profile page with user related options and list of all the opportunities shared by user with filters.

<br>

- **saved.html**: The structure of page which shows all the saved opportunities by users.

<br>

- **share.html**: The structure of form page which is used to share opportunities on Allops by users.

<br>

- **signin.html, signup.html**: For regitering an account and login on website. For signout there is a link in dropdown menu in the end.

<br>

### images
* * *

<br>

This folder have all the images used int Allops website like backgrounds, vecotrs etc.

<br>

## Tools and Languages
* * *

<br>

- Django(Python)
- Javascript:
    - React
- Bootstrap Studio
- Font Awesome
- Django-filter, multiselectfield
- HTML/CSS
