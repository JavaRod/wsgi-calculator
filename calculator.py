"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback


def rtfm(*args):
    content = """
<h1>Welcome to the Calculator</h1>
<p>Many numbers enter, only one number returns</p>
<p>To use this calculator, enter this URL into the browser</p>
<p>http://127.0.0.1/FUNCTION/VALUE/VALUE/...</p>
<p>FUNCTION can be <ul><li>add</li><li>subtract</li><li>multiply</li><li>divide</li></ul></p>
<p>You can have 1 or more integers for VALUE</p>
<p>Entering only 1 value will simply return that value</p>
<p>Note: You will receive a message if you attempt to divide by 0</p>
<h2>Examples</h2>
<p>Addition: http://127.0.0.1:8080/add/23/42</p>
<p>Subtraction: http://127.0.0.1:8080/subtract/23/42</p>
<p>Multiplication: http://127.0.0.1:8080/multiply/3/5</p>
<p>Division: http://127.0.01:8080/divide/22/11</p>
"""

    return content


def add(*args):
    total = sum(map(int, args))
    return str(total)


def subtract(*args):
    result = int(args[0])
    for value in args[1:]:
        result = result - int(value)
    return str(result)


def multiply(*args):
    result = int(args[0])
    for value in args[1:]:
        result = result * int(value)
    return str(result)


def divide(*args):
    try:
        result = int(args[0])
        for value in args[1:]:
            result = result / int(value)
        return str(result)
    except ZeroDivisionError:
        return "Cannot divide by 0"


def resolve_path(path):
    funcs = {
        '': rtfm,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
