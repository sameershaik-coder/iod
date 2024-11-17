# [Django Datta Able PRO](https://appseed.us/product/datta-able-pro/django/)

Django starter styled with Datta Dashboard PRO, a premium Boostrap 5 design from CodedThemes The product is designed to deliver the best possible user experience with highly customizable feature-rich pages.

> **YOUR ACCESS TOKEN**: `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`

**IMPORTANT**: DON'T SHARE this TOKEN with anyone and don't save it on GitHUB or GitLab (becomes automatically invalidated).   

<br />

## Features: 

- ✅ `Up-to-date Dependencies`
- ✅ `Design`: [Django Theme Datta](https://github.com/app-generator/django-admin-datta-pro) - `PRO Version`
- ✅ `Sections` covered by the design:
  - ✅ **Admin section** (reserved for superusers)
  - ✅ **Authentication**: `Django.contrib.AUTH`, Registration
  - ✅ **All Pages** available in for ordinary users 
- ✅ `Docker`
- 🚀 `Deployment` 
  - `CI/CD` flow via `Render`

<br />

## How to use the product 

> 👉 Export `GITHUB_TOKEN` in the environment: 

```bash
$ export GITHUB_TOKEN='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'  # for Linux, Mac      !!! Don't share it or save it on GitHub !!!
$ set GITHUB_TOKEN='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'     # Windows CMD         !!! Don't share it or save it on GitHub !!!
$ $env:GITHUB_TOKEN = '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'  # Windows powerShell  !!! Don't share it or save it on GitHub !!!
```

This is required because the project has a private REPO dependency: `github.com/app-generator/priv-django-admin-datta-pro`

> 👉 Clone the sample project

```bash
$ git clone https://github.com/app-generator/django-datta-able-pro.git
$ cd django-datta-able-pro
```

> 👉 Follow the instructions provided by the [README](https://github.com/app-generator/django-datta-able-pro)

```bash
$ # Instal dependencies 
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ 
$ # Set Up Database
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create SuperUser
$ python manage.py createsuperuser
$
$ # Start Server
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

<br />

## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- home/
   |    |-- views.py                     # APP Views 
   |    |-- urls.py                      # APP Routing
   |    |-- models.py                    # APP Models 
   |    |-- tests.py                     # Tests  
   |    |-- templates/                   # Theme Customisation 
   |         |-- pages                   # 
   |              |-- custom-index.py    # Custom INDEX Page    
   |
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## How to Customize 

When a template file is loaded in the controller, `Django` scans all template directories starting from the ones defined by the user, and returns the first match or an error in case the template is not found. 
The  theme used to style this starter provides the following files: 

```bash
# This exists in ENV: LIB/admin_datta_pro
< UI_LIBRARY_ROOT >                      
   |
   |-- templates/                     # Root Templates Folder 
   |    |          
   |    |-- accounts/       
   |    |    |-- auth-signin.html     # Sign IN Page
   |    |    |-- auth-signup.html     # Sign UP Page
   |    |
   |    |-- includes/       
   |    |    |-- footer.html          # Footer component
   |    |    |-- sidebar.html         # Sidebar component
   |    |    |-- navigation.html      # Navigation Bar
   |    |    |-- scripts.html         # Scripts Component
   |    |
   |    |-- layouts/       
   |    |    |-- base.html            # Masterpage
   |    |    |-- base-auth.html       # Masterpage for Auth Pages
   |    |
   |    |-- pages/       
   |         |-- index.html           # INDEX page
   |         |-- landingpage.html     # Sample LP
   |         |-- *.html               # All other pages
   |    
   |-- ************************************************************************
```

When the project requires customization, we need to copy the original file that needs an update (from the virtual environment) and place it in the template folder using the same path. 

For instance, if we want to customize the `index.html` these are the steps:

- `Step 1`: create the `templates` DIRECTORY inside your app 
- `Step 2`: configure the project to use this new template directory
  - Edit `settings.py` TEMPLATES section 
- `Step 3`: copy the `index.html` from the original location (inside your ENV) and save it to the `YOUR_APP/templates` DIR
  - Source PATH: `<YOUR_ENV>/LIB/admin_datta_pro/templates/pages/index.html`
  - Destination PATH: `YOUR_APP/templates/pages/index.html`
- Edit the footer (Destination PATH)    

At this point, the default version of the `index.html` shipped in the library is ignored by Django.

In a similar way, all other files and components can be customized easily.

<br />

## Deploy on [Render](https://render.com/)

- Create a Blueprint instance
  - Go to https://dashboard.render.com/blueprints this link.
- Click `New Blueprint Instance` button.
- Connect your `repo` which you want to deploy.
- Fill the `Service Group Name` and click on `Update Existing Resources` button.
- After that your deployment will start automatically.

At this point, the product should be LIVE.


---
[Django Datta Able PRO](https://appseed.us/product/datta-able-pro/django/) - **Django** starter provided by **[AppSeed](https://appseed.us/)**
