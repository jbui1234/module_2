import pandas as pd
import networkx as nx
from prettytable import PrettyTable


df = pd.read_csv('country_city.csv')
df = df.dropna(subset=['City', 'Country'])
df['City'] = df['City'].astype(str).str.strip()
df['Country'] = df['Country'].astype(str).str.strip()
df['Annual ridership (millions)'] = pd.to_numeric(df['Annual ridership (millions)'], errors='coerce').fillna(0.0)

# Build graph
G = nx.Graph()
for _, row in df.iterrows():
    city = row['City']
    G.add_node(city, 
               country=row['Country'], 
               ridership=row['Annual ridership (millions)'], 
               system=row['Name'])

for _, row1 in df.iterrows():
    for _, row2 in df.iterrows():
        if row1['Country'] == row2['Country'] and row1['City'] != row2['City']:
            G.add_edge(row1['City'], row2['City'])

# Centralities
degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
weighted = {node: G.nodes[node].get('ridership', 0.0) for node in G.nodes}

# Function to print top/bottom N
def print_table(title, data, metric_index, reverse=True, N=20):
    sorted_data = sorted(data, key=lambda x: x[metric_index], reverse=reverse)[:N]
    table = PrettyTable()
    table.field_names = ["City", "Degree", "Betweenness", "Eigenvector", "Ridership (M)"]
    for row in sorted_data:
        table.add_row(row)
    print(f"\n{title}")
    print(table)

# Combine all into list of tuples
combined = []
for city in G.nodes:
    combined.append((
        city,
        round(degree.get(city, 0), 4),
        round(betweenness.get(city, 0), 4),
        round(eigenvector.get(city, 0), 4),
        round(weighted.get(city, 0), 2)
    ))

# Top 20 Tables
print_table("Top 20 by Degree Centrality", combined, 1, reverse=True)
print_table("Top 20 by Betweenness Centrality", combined, 2, reverse=True)
print_table("Top 20 by Eigenvector Centrality", combined, 3, reverse=True)
print_table("Top 20 by Weighted Centrality (Ridership)", combined, 4, reverse=True)

# Bottom 20 Tables
print_table("Bottom 20 by Degree Centrality", combined, 1, reverse=False)
print_table("Bottom 20 by Betweenness Centrality", combined, 2, reverse=False)
print_table("Bottom 20 by Eigenvector Centrality", combined, 3, reverse=False)
print_table("Bottom 20 by Weighted Centrality (Ridership)", combined, 4, reverse=False)
