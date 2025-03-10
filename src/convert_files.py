from rdf_to_csv.RDFtoCSV import RDFtoCSVConverter

def convert_files_to_csv(rdf_file, mapping_file):
    """
    Converts RDF and mapping files into a CSV file.

    This function initializes the RDFtoCSVConverter with the provided RDF and mapping files,
    runs the conversion process, and handles any exceptions that may occur during the process.

    Args:
        rdf_file (str): Path to the RDF file to be converted.
        mapping_file (str): Path to the mapping file that defines the conversion rules.

    Returns:
        str: A message indicating the successful creation of the output CSV file.

    Raises:
        ValueError: If an error occurs during the conversion process.
    """
    output_csv = "output.csv"
    try:
        # Initialize the converter with the input files and output file name
        converter = RDFtoCSVConverter(rdf_file, mapping_file, output_csv)
        converter.run()
         
        return f'CSV file output.csv has been successfully created.'
    
    except Exception as e:
        # Catch any exceptions that occur during the conversion process
        
        raise ValueError(f'Error during conversion: {str(e)}') # Raise a ValueError with a descriptive error message