# vbn_api Documentation

## Overview

`vbn_api` is a Python-based API interaction tool designed to fetch and display departure information from the Verkehrsverbund Bremen/Niedersachsen (VBN).

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

- Core script to interact with the VBN API.
- Retrieves and processes departure data from specified stations. Needs start and destination station
- needs a key you can request from https://www.vbn.de/service/entwicklerinfos/opendata-und-openservice

### vbn_stat.py

- Assists in managing station-specific data.
- Includes utilities for handling station lists and displaying it using tkinter.

### README.md

- This document

### .gitignore

- Defines files/directories Git should ignore, such as Python bytecode and temporary files.

### requirements.txt

- Lists Python dependencies required for the project.
- Content:

```txt
pycurl>=7.45.2
```

> **Note for Linux users:** You may need to install additional system packages:
> ```bash
> sudo apt update
> sudo apt install libcurl4-openssl-dev libssl-dev python3-tk
> ```

## Usage

### Requirements

- Python 3.x
- Required Python libraries (listed in `requirements.txt`):
  - pycurl
- GUI requires `tkinter`, which is bundled with Python on Windows/macOS but might need to be installed on Linux.

### Example: Retrieving Station Information

Before fetching departure times, you may want to determine the IDs of nearby stations. The VBN API provides a planning endpoint that accepts coordinates and returns matching transit locations.

Here is a sample `curl` command that uses the VBN API to get routing and station data:

```bash
curl -X GET \
  'http://gtfsr.vbn.de/api/routers/connect/plan?arriveBy=false&date=02-14-2025&fromPlace=53.059429,8.899465&toPlace=53.051735,8.819698&time=13:00:00&mode=WALK,TRANSIT&maxWalkDistance=300' \
  -H 'Authorization: YOUR_API_KEY_HERE' \
  -H 'Host: gtfsr.vbn.de'
```

- Replace `YOUR_API_KEY_HERE` with your personal API key obtained from [VBN Open Data](https://www.vbn.de/service/entwicklerinfos/opendata-und-openservice).
- Replace the coordinates with your desired start (`fromPlace`) and destination (`toPlace`) locations.

#### Interpreting the Output

In the returned JSON, look under the `plan → from` or `to` fields, or inside each item in the `legs` array. You’ll typically find fields like:

```json
"stopId": "000123456",
"name": "Bremen Hauptbahnhof",
"lat": 53.083,
"lon": 8.813
```

You can then use the extracted `stopId` in your own requests via the `vbn_api.py` script.

### Installation

```bash
git clone https://github.com/b0hne/vbn_api.git
cd vbn_api
pip install -r requirements.txt
```

### Running the Application

```bash
python vbn_api.py
```

Adjust parameters within `vbn_api.py` or through command-line arguments if implemented, to specify the station data.

## Contribution

Contributions are welcome! Please open an issue or submit a pull request.

## License

See repository for licensing details or contact the maintainer directly.

---

For more details, visit the GitHub repository at [https://github.com/b0hne/vbn_api](https://github.com/b0hne/vbn_api).

