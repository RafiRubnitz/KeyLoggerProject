Endpoint              Methods  Rule                                   
--------------------  -------  ---------------------------------------
computers             GET      /computers
download_file         GET      /api/download/<folder>/<path:file_path>
get_computer_details  GET      /api/computers/<computer>
get_computers_list    GET      /api/get_computers_list
home                  GET      /
static                GET      /static/<path:filename>
stop                  GET      /computers/<computer_name>/stop
upload                POST     /api/upload
user_verification     POST     /user_verification



## Endpoint Descriptions

- **computers** – Returns the HTML page displaying the list of tracked computers.  
- **download_file** – API for downloading a JSON file from the server.  
- **get_computer_details** – Retrieves detailed information about a specific computer, including all associated files.  
- **get_computers_list** – Returns a list of all computers currently being tracked by the server.  
- **home** – The homepage of the application.  
- **static** – Serves static files such as CSS and JavaScript.  
- **stop** – Stops tracking a specific computer.  
- **upload** – API for uploading data to the server.  
- **user_verification** – API for verifying user credentials.  

---
 















