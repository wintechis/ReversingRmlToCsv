# ReversingRmlToCsv

![Static Badge](https://img.shields.io/badge/RML2CSV-purple) ![Static Badge](https://img.shields.io/badge/python-3.8-yellow?logo=python&logoColor=white&labelColor=blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)


### RDF to CSV Converter 

A GUI application for converting RDF and RML files into CSV format.

---

## Table Of Contents

- [Description](#Description)

- [Features](#Features)

- [Prerequisites](#Prerequisites)

- [Installation](#Installation)

- [Usage](#Usage)

- [License](#License)



### I. Description

> This project provides a graphical user interface (GUI) tool for converting RDF (Resource Description Framework) and RML (RDF Mapping Language) files into CSV  format. The application simplifies the process of transforming complex semantic data into a more accessible and widely-used format for data analysis.

>The tool is built using PyQt5 for the GUI and leverages the rdflib library for handling RDF data and pandas for CSV operations. It supports file browsing, conversion status display, and error handling to ensure a smooth user experience.

### II. Features

  File Browsing: Easily select RDF (.nq) and RML (.ttl) files through a file dialog.

  Conversion Process: Converts selected RDF and RML files into a CSV file.

  Status Display: Shows the status of the conversion process, including success messages and error notifications.

  Error Handling: Provides informative error messages for invalid file formats, missing files, and conversion issues.

  GUI Interface: User-friendly interface designed for simplicity and ease of use.


### III. Prerequisites

Before using the RDF to CSV Converter, ensure you have the following installed:

- Python 3.8 or higher
- PyQt5 for the GUI framework
- rdflib for RDF data processing
- pandas for CSV operations

### IV Installation

Install the dependencies if you haven't already:
```bash
pip install -r requirements.txt
```
### V. Usage

1. *[Launch the Application](#Launch_the_Application)*: Run the main application script:
    ```bash
    python main_app.py
    ```
2. *[Select Files](#Select_Files)*:
Click on the Browse buttons to select your RDF (.nq) and RML (.ttl) files.
You can also manually enter the file paths in the input fields.

3. *[Convert to CSV](#Convert_to_CSV)*:
Click the Convert to CSV button to start the conversion process.
The application will display a status message indicating the success or failure of the conversion.

4. *[View Output](#View_Output)*:
Upon successful conversion, a hyperlink to the generated output.csv file will be displayed. Click on the link to open the file.






### VI. License

This project is licensed under the MIT License. Please have a look at the LICENSE file for more details.






