import os
from pprint import pprint
import re
import shutil

class IncidentCategorizer:
    def __init__(self, pattern_dict):
        self.pattern_dict = pattern_dict

    def categorize_incident(self, text):
        text = text.lower()
        category_counts = {category: 0 for category in self.pattern_dict}

        for category, patterns in self.pattern_dict.items():
            category_counts[category] = sum(len(re.findall(pattern, text)) for pattern in patterns)

        max_count = max(category_counts.values())
        if max_count == 0:
            return "Uncategorized"
        
        max_categories = [cat for cat, count in category_counts.items() if count == max_count]
        return max_categories[0] if len(max_categories) == 1 else "Uncategorized"

    def calculate_probabilities(self, aggregated_extracted_lines, keys):
        probabilities = {}

        for filename, extracted_lines in aggregated_extracted_lines.items():
            file_probabilities = {category: 0 for category in self.pattern_dict}

            for key in keys:
                if key in extracted_lines:
                    lines = extracted_lines[key]
                    category_counts = {category: 0 for category in self.pattern_dict}

                    for line in lines:
                        category = self.categorize_incident(line)
                        if category in category_counts:
                            category_counts[category] += 1

                    total = sum(category_counts.values())
                    if total > 0:
                        for category in self.pattern_dict:
                            file_probabilities[category] += category_counts[category] / total

            # Calculate average probabilities across all specified keys
            total_keys = len(keys)
            if total_keys > 0:
                for category in self.pattern_dict:
                    file_probabilities[category] /= total_keys

            probabilities[filename] = file_probabilities

        return probabilities
    
    def filter_and_print_incidents(self, categorized_data, thresholds):
        """
        Filter and print incidents based on user-defined probability thresholds.

        Args:
        - categorized_data (dict): Dictionary with filenames as keys and dictionaries of probabilities as values.
        - thresholds (dict): Dictionary with category names as keys and tuples of (min_threshold, max_threshold) as values.
                             Use None for no threshold.

        Example:
        thresholds = {
            'Pilot Error': (0.33, None),  # At least 0.33
            'Weather Condition': (None, 0.33),  # Less than 0.33
            'Engine Failure': (0.33, None)  # At least 0.33
        }
        """
        for key, val in categorized_data.items():
            meets_criteria = True
            for category, (min_threshold, max_threshold) in thresholds.items():
                if category not in val:
                    meets_criteria = False
                    break
                if min_threshold is not None and val[category] < min_threshold:
                    meets_criteria = False
                    break
                if max_threshold is not None and val[category] >= max_threshold:
                    meets_criteria = False
                    break
            
            if meets_criteria:
                pprint(key)























#     def filter_and_copy_incidents(self, categorized_data, thresholds, source_path, dest_path, f=None):
#             """
#             Filter incidents based on user-defined probability thresholds and copy matching files to a destination folder.
#             If the destination folder exists, it will be removed and recreated.

#             Args:
#             - categorized_data (dict): Dictionary with filenames as keys and dictionaries of probabilities as values.
#             - thresholds (dict): Dictionary with category names as keys and tuples of (min_threshold, max_threshold) as values.
#                                 Use None for no threshold.
#             - source_path (str): Path to the source directory containing the original files.
#             - dest_path (str): Path to the destination directory where matching files will be copied.
#             - f (object): Optional file system operations object. If None, built-in operations will be used.

#             Returns:
#             - list: List of filenames that were successfully copied.
#             """
#             if f is None:
#                 f = FileSystemOps()

#             copied_files = []

#             # Remove destination directory if it exists
#             if f.exists(dest_path):
#                 f.rmtree(dest_path)

#             # Create destination directory
#             f.makedirs(dest_path)

#             for key, val in categorized_data.items():
#                 meets_criteria = True
#                 for category, (min_threshold, max_threshold) in thresholds.items():
#                     if category not in val:
#                         meets_criteria = False
#                         break
#                     if min_threshold is not None and val[category] < min_threshold:
#                         meets_criteria = False
#                         break
#                     if max_threshold is not None and val[category] >= max_threshold:
#                         meets_criteria = False
#                         break
                
#                 if meets_criteria:
#                     source_file = f.path_join(source_path, key)
#                     dest_file = f.path_join(dest_path, key)
#                     if f.exists(source_file):
#                         f.copy(source_file, dest_file)
#                         copied_files.append(key)
#                         print(f"Copied: {key}")
#                     else:
#                         print(f"File not found: {key}")

#             return copied_files
            

# class FileSystemOps:
#     """Default file system operations class."""
#     def makedirs(self, path, exist_ok=False):
#         os.makedirs(path, exist_ok=exist_ok)

#     def path_join(self, *paths):
#         return os.path.join(*paths)

#     def exists(self, path):
#         return os.path.exists(path)

#     def copy(self, src, dst):
#         shutil.copy2(src, dst)

#     def rmtree(self, path):
#         shutil.rmtree(path)