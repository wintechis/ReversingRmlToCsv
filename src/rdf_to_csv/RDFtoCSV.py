

import pandas as pd
import os
import re

from rdflib.namespace import RDF
from rdflib.term import BNode, URIRef, Literal
from rdflib import Graph, Dataset
from urllib.parse import unquote, urlparse 


class RDFtoCSVConverter:
    """
    A converter class that transforms RDF data into CSV format.

    The class processes RDF graphs (N-Quads) and a mapping file (RML)to structure the data appropriately
    for CSV conversion. It handles references, literals, and provides methods to save the
    final CSV output.
    """
    
    def __init__(self, rdf_file, mapping_file, output_csv):
        """
        Initializes the RDF to CSV converter with the specified files.

        Args:
            rdf_file (str): Path to the RDF file(.nq) to convert.
            mapping_file (str): Path to the mapping file (.ttl) that defines the conversion structure.
            output_csv (str): Path where the output CSV file will be saved.

        Attributes:
            graph (Dataset): Parses the RDF file in N-Quads format using rdflib.Dataset().
            mapping_graph (Graph): Parses the RML mapping file in Turtle format using rdflib.Graph().
            columns (list): List of column names for the CSV output.
            data (list): List of rows containing the CSV data.
            subject_template (str): Template for subject URIs.
            ref_object_maps (dict): Dictionary storing reference object maps for joins.
            language_columns (dict): Dictionary for handling language-specific columns.
        """
        self.rdf_file = rdf_file
        self.mapping_file = mapping_file
        self.output_csv = output_csv
        self.graph = Dataset()
        self.mapping_graph = Graph()
        self.columns = []
        self.data = []
        self.subject_template = None
        self.ref_object_maps = {}  # Store RefObjectMaps for joins
        self.language_columns = {}

    
    def check_files_exist(self):
        """Checks if the RDF and mapping files exist. Raises FileNotFoundError if either file is missing."""
        if not os.path.exists(self.rdf_file):
            raise FileNotFoundError(f"Error: RDF file '{self.rdf_file}' is missing.")
        if not os.path.exists(self.mapping_file):
            raise FileNotFoundError(f"Error: Mapping file '{self.mapping_file}' is missing.")

    
    def load_rdf_file(self):
        """
        Loads and parses the RDF and mapping files. 
        
        Raises ValueError if parsing fails.
        
        """
        try:
            self.graph.parse(self.rdf_file, format="nquads")
        except Exception as e:
            raise ValueError(f"Error parsing RDF file '{self.rdf_file}': {e}")

        try:
            self.mapping_graph.parse(self.mapping_file, format="turtle")
        except Exception as e:
            raise ValueError(f"Error parsing mapping file '{self.mapping_file}': {e}")

    

    def extract_subject_template(self):
        """
        Extracts the subject template and term type from the RML mapping.

        This method executes a SPARQL query to retrieve the subject template and its associated term type.
        It ensures that only one subject map is present and handles different term types appropriately.

        Raises:
            ValueError: If no subject template is found.
            ValueError: If the term type is 'Literal', as literals are not allowed as subjects.
        """

        query = """
        PREFIX rml: <http://w3id.org/rml/>
        SELECT DISTINCT ?template ?termType WHERE {
            ?triplesMap rml:subjectMap ?subjectMap . 
            ?subjectMap rml:template ?template .
            OPTIONAL { ?subjectMap rml:termType ?termType }
            OPTIONAL { ?subjectMap rml:graphMap ?graphMap . ?graphMap rml:termType ?termType }
        }
        """
        results = list(self.mapping_graph.query(query))

        
        # Check if results are empty
        if not results:
            raise ValueError("Error: No subject template found in the RML mapping.")
            
        self.subject_template = str(results[0][0])

        # If termType is missing, assign a default or handle accordingly
        self.subject_term_type = str(results[0][1]) if results[0][1] else "DefaultTermType"

        if not self.subject_template.strip():
            raise ValueError("Error: No subject template found in the RML mapping.")

        # Handle if termType is Blank Node
        if "BlankNode" in self.subject_term_type:
            print("Blank Node detected. Extracting ID...")
            

        print(f"Term Type: {self.subject_term_type}")
        if "Literal" in self.subject_term_type:
            raise ValueError("LiteralSubjectError: The subject term type is Literal, which is not allowed.")
        
        # If the term type is IRI, extract all IRIs and store them in a class attribute
        if "IRI" in self.subject_term_type:
            print("Term Type is IRI. Extracting IRIs...")
            try:
                # SPARQL query to retrieve IRIs
                iri_query = """
                PREFIX rml: <http://w3id.org/rml/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT ?s
                WHERE {
                    ?s rdf:type foaf:Person .
                }
                """
                iri_results = list(self.graph.query(iri_query))
                self.iris = [str(result[0]) for result in iri_results]  # Store IRIs in a class attribute
                print(f"Extracted IRIs: {self.iris}")
            
            except Exception as e:
                raise ValueError(f"Error extracting IRIs: {str(e)}")

        print(f"Extracted Template: {self.subject_template}")
        self.extract_columns_from_template(self.subject_template)

    
    
    def extract_columns_from_template(self, template):
        """
        Extracts and normalizes column names from a given template.

        This method identifies patterns within curly braces in the template,
        normalizes the column names by replacing spaces with underscores, and
        ensures each column name is unique before adding it to the list of columns.

        Args:
            template (str): The template string containing column patterns.
        """
        columns_in_template = re.findall(r'\{(.*?)\}', template, re.DOTALL)
        print(f"Columns Found in Template: {columns_in_template}")

        for column in columns_in_template:
            # Normalize column names to avoid duplicates
            normalized_column = column.replace(' ', '_')  # Normalize to lowercase and replace spaces
            if normalized_column not in [col.lower() for col in self.columns]:
                self.columns.append(normalized_column)
        
        print(f"Final Columns: {self.columns}")
        

    


    

    


    def extract_data(self):
        """
        Extracts data from the RDF graph based on the mapping and prepares it for CSV conversion.

        This method processes each quad (subject, predicate, object, context) in the RDF graph,
        extracts relevant data, and structures it into records. It handles different object types
        (blank nodes, URIs, literals), manages datatype mappings, and processes templates to
        split values into multiple columns. Finally, it ensures all records have consistent columns
        and performs any necessary joins before storing the data for CSV output.
        
        """
        records = {}
        
        datatype_map = {}
        
        query = """
        PREFIX rml: <http://w3id.org/rml/>
        PREFIX ex: <http://example.com/>
        SELECT ?objectMap ?predicate ?datatypeTemplate
        WHERE {
            ?triplesMap rml:predicateObjectMap ?pom .
            ?pom rml:predicate ?predicate;
                rml:objectMap ?objectMap .
            OPTIONAL {
                ?objectMap rml:datatypeMap ?dm .
                ?dm rml:template ?datatypeTemplate .
            }
        }
        """
        
        results = list(self.mapping_graph.query(query))
        print(results)

        # Print the datatype templates
        if results:
            for row in results:
                object_map = str(row[0])
                predicate = str(row[1])
                datatype_template = str(row[2])
                if datatype_template != 'None':
                # Extract datatype name from the URI
                    if '#' in datatype_template:
                        datatype_name = datatype_template.split('#')[-1]
                    else:
                        datatype_name = datatype_template

                
                    # Map predicate to datatype
                    predicate_short = predicate.split("#")[-1] if "#" in predicate else predicate.split("/")[-1]
                    datatype_map[predicate_short] = datatype_name

                print("Datatype Map:", datatype_map)

        
    
        for s, p, o, _ in self.graph.quads():
            
            subject_id = str(s)
            # Check if it's a blank node
            if isinstance(s, BNode):
                subject_id = f"_:blank_{s}"
                
            predicate = str(p)
            # Extract the short form of the predicate
            if "#" in predicate:
                predicate_short = predicate.split("#")[-1]
            else:
                predicate_short = predicate.split("/")[-1]
            
            
            # Process object values
            if isinstance(o, BNode):
                object_value = self.resolve_blank_node(o)
                print(f"Blank node detected: {o}, processed as: {object_value} | Subject: {s}, Predicate: {p}")
            
            elif isinstance(o, URIRef):
                parsed = urlparse(str(o))
                object_value = unquote(parsed.path.split("/")[-1] if parsed.path else str(o))
            elif isinstance(o, Literal):
                object_value = str(o)
                # Check if this is from rml:objectMap with rml:datatype
                datatype = str(o.datatype) if o.datatype else "string"
                # Extract datatype name from URI
                if '#' in datatype:
                    datatype_name = datatype.split('#')[-1]
                
                else:
                    datatype_name = datatype
                    

            else:
                object_value = str(o)
                
            

            # Initialize the record if not present
            if subject_id not in records:
                records[subject_id] = {col: "" for col in self.columns}

            if datatype_map and predicate_short in datatype_map:
            # Add datatype column if missing
                datatype_column = f"{predicate_short}_datatype"
                if datatype_column not in self.columns:
                    self.columns.append(datatype_column)
                records[subject_id][datatype_column] = datatype_name if 'datatype_name' in locals() else datatype_map[predicate_short]

            # Handle language-specific columns
            if hasattr(o, 'language') and o.language:
                lang = o.language
                column_name = self.language_columns.get(predicate_short, f"{predicate_short}_{lang}")
                if column_name not in self.columns:
                    self.columns.append(column_name)
                records[subject_id][column_name] = object_value
                
            else:
                # Add predicate column if missing
                if predicate_short.lower() not in [col.lower() for col in self.columns]:
                    self.columns.append(predicate_short)
                
                records[subject_id][predicate_short] = object_value
        

            records[subject_id] = self.populate_template_fields(subject_id, records[subject_id])
                
            # Check if predicate has a template and split values accordingly
            object_template_query = """
            PREFIX rml: <http://w3id.org/rml/>
            SELECT DISTINCT ?template WHERE {
                ?triplesMap rml:predicateObjectMap [ rml:predicate <%s>; rml:objectMap [ rml:template ?template ] ].
            }
            """ % predicate

            object_template_results = list(self.mapping_graph.query(object_template_query))

            if object_template_results:
                template_str = str(object_template_results[0][0])
                placeholders = re.findall(r'\{(.*?)\}', template_str)

                # Split the object_value based on spaces (assuming space-separated values)
                split_values = object_value.split(' ')

                # Add placeholders to columns if they aren't already present
                for placeholder in placeholders:
                    if placeholder not in self.columns:
                        self.columns.append(placeholder)

                # Assign split values to placeholders
                for i, placeholder in enumerate(placeholders):
                    if i < len(split_values):
                        records[subject_id][placeholder] = split_values[i]
            else:
                # If no template matches, store as usual
                records[subject_id][predicate_short] = object_value

        for record in records.values():
            for col in self.columns:
                if col not in record:
                    record[col] = ""
        
        self.data = records

    
    
    
    def populate_template_fields(self, subject_id, record):
        """
        Populate the template fields like {ID}, {fname}, {lname} from the subject URI or blank node.

        This method extracts values from the subject URI or blank node based on the defined subject template.
        It supports both blank nodes and URIs, extracting values and mapping them to the corresponding
        placeholders in the template.

        Args:
            subject_id (str): The identifier of the subject, which can be a URI or a blank node.
            record (dict): The dictionary containing the data record to be populated.

        Returns:
            dict: The updated record with template fields populated.
        """
        if not self.subject_template:
            return record

        # Extract placeholders from the subject template
        placeholders = re.findall(r'\{(.*?)\}', self.subject_template)
        if not placeholders:
            return record

        # Handle blank nodes by querying their associated literals
        if isinstance(subject_id, str) and subject_id.startswith("_:blank_"):
            blank_node_id = BNode(subject_id.replace("_:blank_", ""))
            
            # Query the graph for the blank node's properties
            for _, p, o, _ in self.graph.quads((blank_node_id, None, None, None)):
                predicate_short = str(p).split("/")[-1]
                for placeholder in placeholders:
                    # Check if predicate matches the placeholder name
                    if placeholder.lower() == predicate_short.lower():
                        record[placeholder] = str(o)
                        print(f"Extracted from blank node: {placeholder} -> {o}")
            return record

        # Handle URIs with placeholders in the subject template
        regex_pattern = self.subject_template
        for placeholder in placeholders:
            regex_pattern = regex_pattern.replace(f'{{{placeholder}}}', r'([^/;]+)')

        # Escape everything except capture groups
        regex_pattern = re.escape(regex_pattern).replace(r'\(\[\^/;\]\+\)', r'([^/;]+)')

        # Attempt to match the subject string against the template pattern
        match = re.match(regex_pattern, subject_id)
        if match:
            extracted_values = match.groups()
            for placeholder, value in zip(placeholders, extracted_values):
                normalized_placeholder = placeholder.replace(' ', '_')
                decoded_value = unquote(value)
                record[normalized_placeholder] = decoded_value
                print(f"Extracted from URI: {normalized_placeholder} -> {decoded_value}")

        return record






    def resolve_blank_node(self, node):
        """
        Converts a blank node into a string identifier to ensure uniqueness and consistency.

        This method is crucial for maintaining uniform identifiers for blank nodes, preventing duplicates and ensuring data integrity.

        Args:
            node: The blank node to be converted into a string identifier.

        Returns:
            str: A unique string identifier for the blank node, formatted as "blank_node_{node}".
        """
        return f"blank_node_{str(node)}"

    
    
    def write_to_csv(self):
        """
        Writes the processed data to a CSV file.

        This method handles the conversion of the internal data structure into a pandas DataFrame.
        
        The following steps are performed:
        - Check if there is data to write. If not, create an empty DataFrame with the expected columns.
        - Ensure all columns are included in the DataFrame.
        - Reorder the columns to match the specified order.
        - Write the DataFrame to a CSV file.

        .. note::
            If there is no data to write, an empty DataFrame with the expected columns will be created.
        """
        
        if not self.data:
            df = pd.DataFrame(columns=self.columns)
        else:
            # Convert the data dictionary into a DataFrame
            df = pd.DataFrame.from_dict(self.data, orient="index")
        
            # Ensure all extracted columns are included in the DataFrame
            for column in self.columns:
                if column not in df.columns:
                    df[column] = ""
        print (df)
            
        df = df[self.columns]
        df.to_csv(self.output_csv, index=False)
        print(f"CSV file '{self.output_csv}' has been successfully created.")

    
    
    def run(self):
        """
        Executes the entire data conversion process from start to finish.

        This method orchestrates the sequence of operations required to convert RDF data to CSV, 
        including file checks, data loading, mapping extractions, data processing, and final CSV output.
        """
        
        self.check_files_exist()
        self.load_rdf_file()

        self.extract_subject_template()
        self.extract_data()

        self.write_to_csv()
    
        
           