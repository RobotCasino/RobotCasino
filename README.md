# Python Docker Project

A Python application with browser automation using Playwright, configured to run in a Docker container.

## Project Structure

```
.
├── .github/
│   └── copilot-instructions.md
├── main.py                   # Main application entry point
├── youtube_automation.py     # YouTube browser automation script
├── requirements.txt          # Python dependencies (includes Playwright)
├── Dockerfile               # Docker configuration with Playwright support
├── .dockerignore            # Files to exclude from Docker build
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- Docker daemon running

## How to Execute the Project

### Running the YouTube Automation

1. **Build the Docker image:**
   ```bash
   docker build -t python-docker-app .
   ```

2. **Run the YouTube automation:**
   ```bash
   docker run --rm python-docker-app python youtube_automation.py
   ```

   This will:
   - Launch a headless Chromium browser
   - Navigate to YouTube
   - Capture page title and URL
   - Take a screenshot (saved as `youtube_screenshot.png`)
   - Close the browser

### Running the Default Application

Run the basic hello world app:
```bash
docker run --rm python-docker-app
```

### Option 2: Build and Run in One Command

```bash
docker build -t python-docker-app . && docker run --rm python-docker-app python youtube_automation.py
```
## Development

### Running Locally Without Docker

1. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

4. **Run the YouTube automation:**
   
   **For WSL with Windows X server (xLaunch/VcXsrv):**
   ```bash
   ./run_with_display.sh
   ```
   
   **Or set DISPLAY manually:**
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
   python youtube_automation.py
   ```
   
   **For native Linux:**
   ```bash
   python youtube_automation.py
   ```

   Or run the default application:
   ```bash
   python main.py
   ```

## Running with Docker and X11 Display

### Prerequisites for WSL + Windows X Server:

1. **Install an X Server on Windows:**
   - Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or xLaunch
   
2. **Launch the X Server:**
   - Run XLaunch with these settings:
     - Display number: `0`
     - Start no client
     - **Important:** Check "Disable access control"
   
3. **Allow WSL access (Windows Firewall):**
   ```powershell
   # Run in PowerShell as Administrator
   New-NetFirewallRule -DisplayName "WSL X Server" -Direction Inbound -LocalPort 6000 -Protocol TCP -Action Allow
   ```

### Running with Docker Compose:

```bash
# Make sure xLaunch is running on Windows first!
docker-compose up --build
```

### Running with Docker directly:

```bash
# Get Windows host IP
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# Build the image
docker build -t python-docker-app .

# Run with X11 forwarding
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  python-docker-app python youtube_automation.py
```

### Customizing the YouTube Automation

Edit `youtube_automation.py` to:
- Change from headless to visible browser: Set `headless=False` in the launch command
- Perform searches: Uncomment the search code section
- Navigate to different websites: Change the URL in `page.goto()`
- Add interactions: Use Playwright selectors to click, type, etc.

### Adding Dependencies

Add new dependencies to `requirements.txt`, then rebuild the Docker image.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Adding Dependencies

Add new dependencies to `requirements.txt`, then rebuild the Docker image.

## Customization

- Modify `main.py` to add your application logic
- Edit `youtube_automation.py` to customize browser automation:
  - Change target URLs
  - Add search functionality
  - Interact with page elements
  - Extract data from websites
- Update `requirements.txt` to include additional Python packages
- Adjust the `Dockerfile` if you need different Python version or additional system dependencies
- Change the exposed port in `Dockerfile` if your application uses a different port

## Playwright Features

The YouTube automation script demonstrates:
- Browser launching (headless mode)
- Page navigation
- Waiting for page load
- Getting page information (title, URL)
- Taking screenshots
- Async/await patterns

For more Playwright features, see the [Playwright Python documentation](https://playwright.dev/python/).

## Troubleshooting

### Browser Issues in Docker
If you encounter browser-related errors, ensure the Dockerfile includes all necessary system dependencies for Playwright.

### Screenshot Access
Screenshots are saved inside the container. To access them, you can:
- Mount a volume: `docker run -v $(pwd):/app/output --rm python-docker-app python youtube_automation.py`
- Copy files from container: `docker cp <container-id>:/app/youtube_screenshot.png .`

- **List all containers (including stopped):**
  ```bash
  docker ps -a
  ```

- **Stop a running container:**
  ```bash
  docker stop <container-id>
  ```

- **Remove a container:**
  ```bash
  docker rm <container-id>
  ```

- **Remove the image:**
  ```bash
  docker rmi python-docker-app
  ```

- **View container logs:**
  ```bash
  docker logs <container-id>
  ```

## Customization

- Modify `main.py` to add your application logic
- Update `requirements.txt` to include additional Python packages
- Adjust the `Dockerfile` if you need different Python version or additional system dependencies
- Change the exposed port in `Dockerfile` if your application uses a different port

## License

This project is open source and available under the MIT License.
# RobotCasino-Robots
