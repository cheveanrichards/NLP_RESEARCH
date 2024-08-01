import fitz  # PyMuPDF
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


class KnowledgeGraph:
    def __init__(self):
        self.results = {}
        pass
    
    #1 marker/numerical extractor functions_____________________________________________________________________________
    def extract_text_after_phrases(self,pdf_path, phrases):
        """
        Extract text lines below each phrase in a multi-page PDF until the stopping phrase is encountered or the specified number of lines are extracted.

        Args:
        - pdf_path (str): Path to the PDF document.
        - phrases (dict): Dictionary with phrases as keys and lists as values, where each list contains
                        the number of lines to extract and a stopping phrase.

        Returns:
        - dict: Dictionary with phrases as keys and extracted lines as values.
        """
        # Open the PDF document
        document = fitz.open(pdf_path)

        # Initialize a dictionary to store results
        results = {phrase: [] for phrase in phrases}

        # Iterate through each page in the document
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text("text")
            lines = text.split('\n')

            for i, line in enumerate(lines):
                for phrase, (num_lines, stop_phrase) in phrases.items():
                    if phrase in line and not results[phrase]:
                        # Collect lines after the phrase until the stop phrase is encountered or the number of lines is reached
                        count = 0
                        for subsequent_line in lines[i+1:]:
                            if subsequent_line.strip():  # Exclude empty/whitespace-only lines
                                if stop_phrase and stop_phrase in subsequent_line:
                                    break
                                tokens = word_tokenize(subsequent_line)

                                # Convert to lowercase and remove punctuation
                                cleaned_tokens = [token.lower() for token in tokens if token.isalnum()]

                                # Join tokens back into a single string
                                cleaned_line =  ' '.join(cleaned_tokens)
                                results[phrase].append(cleaned_line)
                                count += 1
                                if count == num_lines:
                                    break

        # Return the dictionary with extracted lines
        return results


    #2 process pdf in path______________________________________________
    def process_pdfs_in_directory(self,directory_path, phrases):
        """
        Process all PDF files in the specified directory, extracting text according to the phrases.

        Args:
        - directory_path (str): Path to the directory containing PDF files.
        - phrases (dict): Dictionary with phrases as keys and lists as values, where each list contains
                        the number of lines to extract and a stopping phrase.

        Returns:
        - dict: Dictionary with filenames as keys and dictionaries of extracted lines as values.
        """
        aggregated_results = {}

        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                print(f"Processing {pdf_path}")
                results = self.extract_text_after_phrases(pdf_path, phrases)
                aggregated_results[filename] = results

        self.results = aggregated_results
        return aggregated_results
    
    # ____________________________________________________________________________________
    
    #3 Utility removal functions_____________________________________________
    def remove_words_from_line(self, line, words_to_remove):
        # Create a regex pattern for the words to remove
        pattern = r'\b(?:' + '|'.join(re.escape(word) for word in words_to_remove) + r')\b'
        # Substitute the words with an empty string
        cleaned_line = re.sub(pattern, '', line)
        # Remove extra spaces left from the removal
        cleaned_line = re.sub(' +', ' ', cleaned_line).strip()
        return cleaned_line
    
    #4 Utility function__________________________________________________
    def word_removal(self, removal_dict):
        updated_aggregated_extracted_lines = {}

        for filename, extracted_lines in self.results.items():
            updated_extracted_lines = {}
            print(f"File: {filename}")

            for phrase, lines in extracted_lines.items():
                words_to_remove = removal_dict.get(phrase, [])
                updated_lines = []
                print(f"  Phrase: {phrase}, Words to remove: {words_to_remove}")

                for line in lines:
                    print(f"    Original line: {line}, Length: {len(line)}")
                    cleaned_line = self.remove_words_from_line(line, words_to_remove)
                    print(f"    Cleaned line: {cleaned_line}, Length: {len(cleaned_line)}")
                    if cleaned_line != '':
                        updated_lines.append(cleaned_line)

                updated_extracted_lines[phrase] = updated_lines

            updated_aggregated_extracted_lines[filename] = updated_extracted_lines

        return updated_aggregated_extracted_lines
    # ____________________________________________________________________________________

  #5 Method to convert to JSON__________________________________________________
    def to_json(self, data, file_path):
        """
        Convert the provided data to a JSON file.

        Args:
        - data (dict): Dictionary to convert to JSON.
        - file_path (str): Path to the JSON file where the results will be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    #6 Method to convert from JSON to dict
    def to_dict(self, file_path):
        # Example JSON file
        with open(file_path) as json_file:
            dict_data = json.load(json_file)
        return dict_data
    