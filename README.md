# vbn_api (Desktopless Branch) Documentation

## Overview

`vbn_api` is a Python-based tool designed to fetch and display departure information from the Verkehrsverbund Bremen/Niedersachsen (VBN). The `desktopless` branch is tailored for environments without a graphical user interface (GUI), enabling command-line interaction for retrieving and processing departure data.

## Repository Structure

```
vbn_api/
├── vbn_api.py
├── vbn_stat.py
├── README.md
├── .gitignore
└── requirements.txt
```

## Files Description

### vbn_api.py

- **Purpose:** Interacts with the VBN API to retrieve departure data.
- **Functionality:** Fetches and processes departure information based on specified stations. Displays them using a png send to attached display.
- **Note:** Requires an API key obtainable from [VBN Open Data](https://www.vbn.de/service/entwicklerinfos/opendata-und-openservice).

### vbn_stat.py

- **Purpose:** Manages station-specific data.
- **Functionality:** Handles station lists and related operations without relying on a GUI.

### README.md

- **Purpose:** Provides documentation and instructions for the project.

### .gitignore

- **Purpose:** Specifies files and directories for Git to ignore, such as Python bytecode and temporary files.

### requirements.txt

- **Purpose:** Lists the Python dependencies required for the project.
- **Content:**
  ```txt
  pycurl>=7.45.2
  ```
- **Note for Linux Users:** Additional system packages may be required:
  ```bash
  sudo apt update
  sudo apt install libcurl4-openssl-dev libssl-dev
  ```

## Usage

### Requirements

- **Python Version:** Python 3.x
- **Python Libraries:** Listed in `requirements.txt` (e.g., `pycurl`).

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/b0hne/vbn_api.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd vbn_api
   ```
3. **Checkout the Desktopless Branch:**
   ```bash
   git checkout desktopless
   ```
4. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Execute the following command in the terminal:

```bash
python vbn_stat.py
```

Configure parameters within `vbn_stat.py` to specify station data and other preferences.

### Example: Retrieving Station Information

To determine the IDs of nearby stations, use the VBN API's planning endpoint with specific coordinates:

```bash
curl -X GET \
  'http://gtfsr.vbn.de/api/routers/connect/plan?arriveBy=false&date=MM-DD-YYYY&fromPlace=LAT1,LON1&toPlace=LAT2,LON2&time=HH:MM:SS&mode=WALK,TRANSIT&maxWalkDistance=300' \
  -H 'Authorization: YOUR_API_KEY_HERE' \
  -H 'Host: gtfsr.vbn.de'
```

- **Replace:**
  - `YOUR_API_KEY_HERE` with your API key from [VBN Open Data](https://www.vbn.de/service/entwicklerinfos/opendata-und-openservice).
  - `MM-DD-YYYY`, `LAT1,LON1`, `LAT2,LON2`, and `HH:MM:SS` with your specific date, coordinates, and time.

**Interpreting the Output:**

The JSON response will contain fields like:

```json
"stopId": "000123456",
"name": "Bremen Hauptbahnhof",
"lat": 53.083,
"lon": 8.813
```

Use the extracted `stopId` in your requests via the `vbn_api.py` script.

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for enhancements or bug fixes.

## License

For licensing details, refer to the repository or contact the maintainer.

---

For more information, visit the GitHub repository at [https://github.com/b0hne/vbn_api/tree/desktopless](https://github.com/b0hne/vbn_api/tree/desktopless). 
