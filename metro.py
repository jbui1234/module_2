import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

country_city_df = pd.read_csv('country_city.csv')

# Drop rows with missing City or Country
country_city_df = country_city_df.dropna(subset=['City', 'Country'])

# Clean string fields
country_city_df['City'] = country_city_df['City'].astype(str).str.strip()
country_city_df['Country'] = country_city_df['Country'].astype(str).str.strip()

# Clean and convert ridership to numeric
country_city_df['Annual ridership (millions)'] = pd.to_numeric(
    country_city_df['Annual ridership (millions)'], errors='coerce'
).fillna(0.0)

G = nx.Graph()
for _, row in country_city_df.iterrows():
    city = row['City']
    G.add_node(city, 
               country=row['Country'], 
               ridership=row['Annual ridership (millions)'], 
               system=row['Name'])

# Add edges between cities in the same country
for _, row in country_city_df.iterrows():
    for _, other_row in country_city_df.iterrows():
        if row['Country'] == other_row['Country'] and row['City'] != other_row['City']:
            G.add_edge(row['City'], other_row['City'])

# Centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Weighted centrality based on ridership
weighted_centrality = {
    node: G.nodes[node].get('ridership', 0.0)
    for node in G.nodes
}

# Get top 10 by each centrality
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
top_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
top_weighted = sorted(weighted_centrality.items(), key=lambda x: x[1], reverse=True)[:10]


print("\nTop 10 by Degree Centrality:")
for city, val in top_degree:
    print(f"{city}: {val:.4f}")

print("\nTop 10 by Betweenness Centrality:")
for city, val in top_betweenness:
    print(f"{city}: {val:.4f}")

print("\nTop 10 by Eigenvector Centrality:")
for city, val in top_eigenvector:
    print(f"{city}: {val:.4f}")

print("\nTop 10 by Weighted Centrality (Ridership):")
for city, val in top_weighted:
    print(f"{city}: {val:.2f} million riders")

plt.figure(figsize=(12, 12))
node_size = [v * 2000 for v in degree_centrality.values()]
nx.draw(G, with_labels=True, node_size=node_size, font_size=8, node_color='skyblue', font_weight='bold')
plt.title("Metro System Cities Network (Degree Centrality)")
plt.show()
