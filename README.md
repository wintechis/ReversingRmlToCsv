# ReversingRmlToCsv

![Static Badge](https://img.shields.io/badge/RML2CSV-purple) ![Static Badge](https://img.shields.io/badge/python-3.8-yellow?logo=python&logoColor=white&labelColor=blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)


### RDF to CSV Converter 

An application is designed to process and transform RDF (Resource Description Framework) and RML (RDF Mapping Language) files into CSV format.


---

## Table Of Contents

- [Description](#Description)

- [Features](#Features)

- [Prerequisites](#Prerequisites)

- [Installation](#Installation)

- [Usage](#Usage)



- [License](#License)



### I. Description


This project provides a tool to convert RDF and RML files into CSV format, simplifying the process of transforming semantic data into a widely-used format for data analysis and visualization.

>Semantic data, such as RDF and RML, contains meaningful information and relationships but is not organized in a tabular format. This makes it challenging to use with tools like spreadsheets or data analysis software. This tool overcomes these challenges by converting semantic data into a CSV format, enabling easier access and seamless integration with data analysis tools.



*Important Requirements*

- RDF files must be in .nq format.
- RML files must be in .ttl format.

The tool is built using PyQt5 for the GUI and leverages the rdflib library for handling RDF data and pandas for CSV operations. It supports file browsing, conversion status display, and error handling to ensure a smooth user experience.

### II. Features

  *File Browsing:* Easily select RDF (.nq) and RML (.ttl) files through a file dialog.

  *Conversion Process:* Converts selected RDF and RML files into a CSV file.

  *Status Display:* Shows the status of the conversion process, including success messages and error notifications.

  *Error Handling:* Provides informative error messages for invalid file formats, missing files, and conversion issues.

  *GUI Interface:* User-friendly interface designed for simplicity and ease of use.


### III. Prerequisites

Before using the RDF to CSV Converter, ensure you have the following installed:

- Python 3.8 or higher
- PyQt5 for the GUI framework
- rdflib for RDF data processing
- pandas for CSV operations

### IV. Installation

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
<img width="617" alt="1  select files" src="https://github.com/user-attachments/assets/4432ebe9-f6f1-4409-b5bb-86aed9192727" />


3. *[Convert to CSV](#Convert_to_CSV)*:
Click the Convert to CSV button to start the conversion process.
The application will display a status message indicating the success or failure of the conversion.

<img width="614" alt="2b  Status display- error" src="https://github.com/user-attachments/assets/64d5bd13-8e65-4cec-849d-84c18c54a753" />

<img width="622" alt="2 Status display-Sucess" src="https://github.com/user-attachments/assets/4dfef0bc-efd6-45e4-acf0-435a03fbd094" />

<img width="622" alt="2a  Status Display-error" src="https://github.com/user-attachments/assets/35b79a2d-38fc-4f39-a1a1-48894ae0db81" />


4. *[View Output](#View_Output)*:
Upon successful conversion, a hyperlink to the generated output.csv file will be displayed. Click on the link to open the file.

<img width="385" alt="CSV file" src="https://github.com/user-attachments/assets/042f3484-d2b8-4154-9ee0-9788df9d0258" />

           

### VI. License

This project is licensed under the MIT License. Please have a look at the LICENSE file for more details.






