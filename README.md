# A simple server, based on FastAPI.
You can use it to upload, download and delete files.

Writes a file to disk and uses it's hash like file name.

Endpoints:

/upload/ (via POST method) - using form-data's field 'file' with file-like object.
Returns the hash of file.

/download/?file_hash=<file's hash> (via GET method) - gives the file or an error message.

/delete/?file_hash=<file's hash> (via DELETE method) - returns status '200' (and info message)
if file successfully deleted. If not, returns error message.

# Running
In the main directory, execute 'python run.py [--debug=True]' command in the shell's window

# Technologies used
- FastAPI\Starlette
- uvicorn

# Requirements
- Python 3.5.2+
- Linux OS (was tested on Ubuntu 16.04)
- See 'requirements.txt' for more details

# To contribute
There are no something special to join the project.

# Contacts
To contact with me: @MaikSturm932 (using Telegram app)
or email: maik.sturm932@gmail.com

