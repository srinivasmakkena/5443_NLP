# Webscraping using pyppeteer and BeautifulSoup an retriving dynamic data
## Srinivas Makkena

### Description:

This program allows you to retrieve airport weather data by scraping the website "https://www.wunderground.com/history". It provides a user interface where you can select a filter (currently only "daily" is available), an airport code, and a specific date. The program then fetches the weather data for the selected parameters and displays it in a table format.

The following files and folders are included:

| File/Folder | Description |
|----------|----------|
| [Resources](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/tree/main/Assignments/A07/Resources) | Contains resources such as the airport-codes.json file, which stores information about airport codes and names. |
| [get_content.py](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/blob/main/Assignments/A07/get_content.py) | This file contains the function `get_dynamic_content()` which is responsible for scraping the weather data from the website. |
| [airport-codes.json](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/blob/main/Assignments/A07/Resources/airport-codes.json) | A JSON file that contains a list of airport codes and their corresponding names. This data is used to populate the airport code dropdown in the user interface. |
| [scrape.py](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/blob/main/Assignments/A07/scrape.py) | The main Python script that runs the program. It creates a graphical user interface using the PySimpleGUI library and handles user interactions. |

## Instructions:

1. Install the required libraries by running `pip install -r requirements.txt` in your command line or terminal.
2. Run the `main.py` script to start the program.
3. In the program's user interface, select the filter (currently only "daily" is available), an airport code, and a specific date.
4. Click the "Submit" button to retrieve the airport weather data for the selected parameters.
5. The program will display the weather data in a table format.
6. Close the program by clicking the "Close" button.

With this program, you can easily retrieve and view airport weather data for different dates and airports.
## Screesnshots
![image](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/assets/32659482/ae1ef56d-7508-4e32-8ea2-0a0d8e1cd16d)

![image](https://github.com/srinivasmakkena/4883-SoftwareTools-Makkena/assets/32659482/4b76af1b-4b85-46ba-82ac-b4fb6ffb2563)

