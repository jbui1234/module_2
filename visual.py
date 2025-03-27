import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random

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

# Centrality
degree = nx.degree_centrality(G)
node_sizes = [3000 * degree[node] for node in G.nodes]

# Build country clusters
countries = df['Country'].unique()
country_positions = {}
angle = 0
radius = 10

# Position each country in a circular layout (spread apart)
for i, country in enumerate(countries):
    theta = 2 * np.pi * i / len(countries)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    country_positions[country] = (x, y)

pos = {}
random.seed(42)
for node in G.nodes:
    base_x, base_y = country_positions[G.nodes[node]['country']]
    jitter_x = random.uniform(-1.5, 1.5)
    jitter_y = random.uniform(-1.5, 1.5)
    pos[node] = (base_x + jitter_x, base_y + jitter_y)

# Colors
unique_countries = list(df['Country'].unique())
color_map = {country: i for i, country in enumerate(unique_countries)}
node_colors = [color_map[G.nodes[node]['country']] for node in G.nodes]
cmap = cm.get_cmap('tab20', len(unique_countries))

# Plot
plt.figure(figsize=(28, 26))
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=cmap, alpha=0.9)
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.25)
nx.draw_networkx_labels(G, pos, font_size=6, font_color='black')

plt.title("Metro Network Grouped by Country Clusters\n(Logical Spatial Separation)", fontsize=20)
plt.axis('off')
plt.tight_layout()
plt.show()
