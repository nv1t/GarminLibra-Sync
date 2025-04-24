# Weight Data Synchronization Script

This project provides a Python script to synchronize weight data from Garmin Connect to the Libra app API. It fetches the latest weight data from Garmin Connect and uploads it to the Libra app.

## Features

- Fetches body composition data (weight, body fat, muscle mass) from Garmin Connect.
- Uploads the data to the Libra app API.
- Automatically handles authentication and token storage.
- Logs detailed information for debugging and monitoring.

## Prerequisites

- Python 3.6 or higher
- A Garmin Connect account
- Libra app API access (https://libra-app.eu/api/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nv1t/GarminLibra-Sync
   cd GarminLibra-Sync
   ```

2. Set up a `pyenv` virtual environment:
   ```bash
   pyenv install 3.x.x  # Replace with the required Python version
   pyenv virtualenv 3.x.x weight-env  # Replace with the required Python version
   pyenv activate weight-env
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your Garmin and Libra API credentials:
   ```env
   EMAIL=your_email@example.com
   PASSWORD=your_password
   TOKENSTORE=path_to_tokenstore
   AUTH_TOKEN=your_libra_api_token
   ```

## Usage

1. Run the script:
   ```bash
   python sync.py
   ```

2. The script will:
   - Fetch the latest weight data from Garmin Connect.
   - Upload the data to the Libra app API.

## Logging

The script logs information to the console. You can adjust the logging level in the script by modifying the `logging.basicConfig(level=logging.INFO)` line.

## Troubleshooting

- Ensure your `.env` file is correctly configured.
- Check the logs for error messages.
- Verify your Garmin Connect and Libra app credentials.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.