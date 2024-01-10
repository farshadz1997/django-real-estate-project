# Real Estate Webstie

**Home Property** is a real estate website for listing properties to sell or rent. 

## Installation
<details>
<summary>Run with Docker</summary>
 
* First create <code>.env</code> file and set these parameters inside it:
    
```txt
DEBUG=1
EMAIL_HOST=<Your_host>
EMAIL_PORT=<PORT>
DEFAULT_FROM_EMAIL=<SENDER_NAME>
EMAIL_HOST_USER=<YOUR_EMAI>
EMAIL_HOST_PASSWORD=<EMAIL_PASSWORD_OR_APP_PASSWORD>
```
* Build image from <code>Dockerfile</code> with this command:
```bash
docker build .
```
* In the repository's directory open the terminal and run:
```bash
docker-compose up
```
</details>
<details>
<summary>Run manually on Windows</summary>
 
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```bash
pip install -r requirements.txt
```
- Have the RabbitMQ server installed and started on your Windows
- Replace this snippet in <code>home_property_project/setting.py</code> for your database:
```python
DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.sqlite3",
       "NAME": BASE_DIR / "db.sqlite3",
   }
}
```
- Comment out CELERY_BROKER_URL and CELERY_RESULT_BACKEND in settings file.
- To run Celery on Windows run this command in another Terminal in the repository directory:
```bash
celery -A home_property_project worker -l info --pool=solo
```
- This project uses Gmail SMTP service to request a forgotten password and you need to change it in [settings](https://github.com/farshadz1997/real-estate-project/blob/d572149d11695d3bb7904ff4f04b2397288b2853/home_property_project/settings.py#L161) of project to use it.
create a new superuser or use just mine with the following information:  
* Username: admin  
* Password: HomeProperty1234
- Start the server with this command:
```bash
python manage.py runserver
```
</details>

## Features
* Properties
  * Up to 6 photos per property.
  * Users can add, edit, and delete owned properties.
  * Categorised properties.
  * Search properties by name, type, and category.
* Send emails through Celery.
* Contact section.  
* User dashboard.
  * Change password, email, and profile picture.
* Blogs which controlled by admins.
  * Comments in blogs.
  * Search in blogs.

## Photos
### Home page
![Home page](https://user-images.githubusercontent.com/60227955/144056636-122642da-8417-499f-8826-45937a34bd0e.png)
### Properties 
![Properties page](https://user-images.githubusercontent.com/60227955/144057042-d3621f8e-28f8-4a16-855b-510e75e3c51c.png)
### Blogs page
![Blogs page](https://user-images.githubusercontent.com/60227955/144057397-48cae7ed-6f86-474d-8412-706c89bb22b2.png)
### User dashboard
![image](https://user-images.githubusercontent.com/60227955/144057555-501c4369-fae8-42f1-9504-2d00b768f8f3.png)
