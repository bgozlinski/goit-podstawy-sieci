# Python Web and UDP Server Application

This application demonstrates a simple web server that handles both HTTP and UDP requests, with the latter saving incoming messages to a JSON file.

## Features

- HTTP server on port 3000 serving HTML pages and static content.
- UDP server on port 5000 receiving and saving messages to a JSON file.
- Docker containerization with volume mapping for persistent data storage.

## Requirements

- Python 3.8+
- Docker (for containerization)

## Project Structure

```
project/
│
├── front-init/
│   ├── index.html
│   ├── message.html
│   ├── error.html
│
├── static/
│   ├── style.css
│   └── logo.png
│
├── storage/
│   └── data.json
│
└── main.py
```

## Local Setup

1. Clone the repository and navigate to the project directory.
2. Install Python 3.8 or higher if not already installed.
3. (Optional) Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Run the server script:
   ```bash
   python main.py
   ```

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t my-python-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 3000:3000 -p 5000:5000 -v "$(pwd)/storage":/usr/src/app/storage my-python-app
   ```

This will start the web server accessible at `http://localhost:3000` and the UDP server on port 5000.

## Usage

- Navigate to `http://localhost:3000` to view the index page.
- Go to `http://localhost:3000/message` to send a message via the web form.
- Messages sent from the form are saved to `storage/data.json` through the UDP server.

## Development

- HTML files can be modified directly. Static files like CSS or images should be placed in the `static` directory.
- To update Python logic, modify `main.py` and restart the server.

## License

[Insert your choice of license here]

## Contributors

- [Your Name]

