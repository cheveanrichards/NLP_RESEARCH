import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np
import os

class ReportProcessor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_json()

    def load_json(self):
        with open(self.json_file_path, 'r') as file:
            return json.load(file)
    
    def get_embedding(self, text_list):
        return self.model.encode(text_list)
    
    def get_section_embedding(self, report_key, section_key):
        if report_key in self.data and section_key in self.data[report_key]:
            section_text = self.data[report_key][section_key]
            return self.get_embedding(section_text)
        else:
            raise KeyError(f"Section '{section_key}' not found in report '{report_key}'.")

    def get_combined_embeddings(self, report_key, section_keys):
        combined_embeddings = []
        for section_key in section_keys:
            if section_key in self.data[report_key]:
                section_text = self.data[report_key][section_key]
                embeddings = self.get_embedding(section_text)
                combined_embeddings.append(embeddings.mean(axis=0))
            else:
                raise KeyError(f"Section '{section_key}' not found in report '{report_key}'.")
        return np.concatenate(combined_embeddings)

    def get_all_combined_embeddings(self, section_keys):
        all_embeddings = {}
        for report_key in self.data:
            try:
                combined_embedding = self.get_combined_embeddings(report_key, section_keys)
                all_embeddings[report_key] = combined_embedding
            except KeyError as e:
                print(e)
        return all_embeddings
    
    def find_optimal_clusters(self, embeddings, max_k=10):
        silhouette_scores = []
        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=0)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            silhouette_scores.append((k, score))
        optimal_k = max(silhouette_scores, key=lambda x: x[1])[0]
        return optimal_k

    def cluster_reports(self, section_keys, num_clusters=None, method='kmeans', metric='euclidean'):
        all_embeddings = self.get_all_combined_embeddings(section_keys)
        
        if not all_embeddings:
            raise ValueError(f"No embeddings found for sections '{section_keys}' across all reports.")
        
        # Combine all embeddings into a single array for clustering
        combined_embeddings = np.array(list(all_embeddings.values()))
        
        # Choose clustering method
        if method == 'kmeans':
            if num_clusters is None:
                num_clusters = self.find_optimal_clusters(combined_embeddings)
            model = KMeans(n_clusters=num_clusters, random_state=0)
        elif method == 'hierarchical':
            if num_clusters is None:
                num_clusters = self.find_optimal_clusters(combined_embeddings)
            model = AgglomerativeClustering(n_clusters=num_clusters, affinity=metric, linkage='ward')
        elif method == 'dbscan':
            model = DBSCAN(metric=metric)
        else:
            raise ValueError("Unsupported clustering method")

        # Fit the model and predict clusters
        clusters = model.fit_predict(combined_embeddings)

        # Create a dictionary to store cluster assignments
        clustered_reports = {}
        for report_key, cluster_id in zip(all_embeddings.keys(), clusters):
            if cluster_id not in clustered_reports:
                clustered_reports[cluster_id] = []
            clustered_reports[cluster_id].append(report_key)
        
        return clustered_reports
    
