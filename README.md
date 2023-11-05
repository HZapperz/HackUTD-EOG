# HackUTD-EOG Application

Welcome to our HackUTD-EOG Challenge repository. This application is designed to process sensor data to detect methane leaks efficiently. It's built with Python and utilizes Streamlit for an interactive user interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following tools installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

To set up the application locally, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HZapperz/HackUTD-EOG.git
   cd HackUTD-EOG
   ```

2. **Set Up a Virtual Environment** (optional but recommended)

   - For Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   - For Unix or MacOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```
   ```terminal
   pip install pandas numpy streamlit
   ```
### Running the Application

1. **Start the Streamlit Server**

   ```bash
   streamlit run app.py
   ```

2. **Access the Application**

   Open your web browser and go to the link in your terminal to view the application.

## Usage

To use the application, follow these steps:

1. Upload a CSV file with the sensor data using the provided file uploader in the application.
2. The application will automatically process the data and display the leak detection results.
3. You can view and analyze the detected leaks within the app interface.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
