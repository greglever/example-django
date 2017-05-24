# example-django

A simple [django](https://www.djangoproject.com/) application exposing a 
[REST API](https://stackoverflow.com/questions/671118/what-exactly-is-restful-programming) with automatic 
generation of [Swagger](http://swagger.io/) documentation.

```
git clone https://github.com/greglever/example-django.git
cd example-django
chmod 754 ./run_application.sh
./run_application.sh
```
if everything has built correctly then you should see the following:
```
example_app_1  | Django version 1.11.1, using settings 'ExampleProject.settings'
example_app_1  | Starting development server at http://0.0.0.0:8000/
example_app_1  | Quit the server with CONTROL-C.
```
and if you navigate to [http://0.0.0.0:8000/api/docs](http://0.0.0.0:8000/api/docs) then you should see a page that looks
like the following:

![Example Swagger Page](/example_swagger_page.png?raw=true)
