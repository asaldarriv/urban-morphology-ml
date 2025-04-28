import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Leer el archivo Excel
file_path = "../boeing_results_harvard/world-stats.xlsx"
data = pd.read_excel(file_path)

# Inspeccionar los datos
print("Primeras filas del dataset:")
print(data.head())

# Verificar valores faltantes
print("\nValores faltantes por columna:")
print(data.isnull().sum())

# Eliminar filas con valores faltantes
data = data.dropna()

# Seleccionar columnas específicas para el análisis
columns_to_analyze = [
    'orientation_entropy',
    'prop_4way', 'prop_3way',
    'bc_max', 'elev_mean', 'area_km2'
]
data_selected = data[columns_to_analyze]

# # Estadísticas descriptivas
# print("\nEstadísticas descriptivas de las columnas seleccionadas:")
# print(data_selected.describe())

# # --------------------------------------
# # 1. Análisis de Correlación
# # --------------------------------------
# plt.figure(figsize=(12, 10))
# correlation_matrix = data_selected.corr()
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title("Matriz de Correlación")
# plt.tight_layout()
# plt.savefig("correlation_heatmap.png")
# plt.show()

# # Identificar variables altamente correlacionadas (> 0.85)
# corr_matrix_abs = correlation_matrix.abs()
# upper = corr_matrix_abs.where(np.triu(np.ones(corr_matrix_abs.shape), k=1).astype(bool))
# high_corr = [column for column in upper.columns if any(upper[column] > 0.85)]
# print("\nVariables altamente correlacionadas (correlación > 0.85):")
# print(high_corr)

# # --------------------------------------
# # 2. Análisis de Varianza
# # --------------------------------------
# variance = data_selected.var()
# print("\nVarianza de cada variable:")
# print(variance.sort_values())

# # Identificar variables con varianza baja (umbral arbitrario, ajustable)
# low_variance_threshold = 0.01
# low_variance_cols = variance[variance < low_variance_threshold].index.tolist()
# print(f"\nVariables con varianza < {low_variance_threshold}:")
# print(low_variance_cols)

# # --------------------------------------
# # 3. Análisis de Escalas
# # --------------------------------------
# print("\nDescripción general de escalas (para decidir normalización):")
# print(data_selected.describe())

# Normalizar datos
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_selected)

# Convertir de nuevo a DataFrame para análisis más cómodo
data_scaled_df = pd.DataFrame(data_scaled, columns=columns_to_analyze)

# # --------------------------------------
# # 4. Análisis de Importancia con PCA
# # --------------------------------------
# pca = PCA()
# pca.fit(data_scaled)

# explained_variance = pca.explained_variance_ratio_
# print("\nProporción de varianza explicada por cada componente principal (PCA):")
# print(explained_variance)

# # Gráfica de varianza explicada (codo)
# plt.figure(figsize=(8, 5))
# plt.plot(np.cumsum(explained_variance), marker='o')
# plt.title('Varianza acumulada explicada por componentes principales (PCA)')
# plt.xlabel('Número de componentes')
# plt.ylabel('Varianza acumulada')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("pca_explained_variance.png")
# plt.show()

# # (Opcional) Ver cómo las variables contribuyen a los primeros componentes
# pca_components = pd.DataFrame(pca.components_, columns=columns_to_analyze)
# print("\nComponentes principales (PCA) - Peso de cada variable en cada componente:")
# print(pca_components)

# # --------------------------------------
# # 5. Pairplot actualizado usando datos escalados
# # (ya no es obligatorio, pero puede ser útil visualizar con escalado)
# # --------------------------------------
# pairplot_scaled = sns.pairplot(data_scaled_df, diag_kind='kde', corner=True)
# pairplot_scaled.figure.suptitle("Pairplot de las columnas seleccionadas (escaladas)", y=1.02)
# pairplot_scaled.figure.tight_layout()
# pairplot_scaled.savefig("pairplot_scaled.png")
# plt.show()

# # --- 2. Método del codo (Elbow Method) para elegir k ---
# inertia = []
# k_range = range(1, 11)  # Probar de 1 a 10 clusters

# for k in k_range:
#     kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#     kmeans.fit(data_scaled)
#     inertia.append(kmeans.inertia_)

# # Graficar el resultado
# plt.figure(figsize=(8, 5))
# plt.plot(k_range, inertia, marker='o')
# plt.title('Método del Codo para determinar el número óptimo de clusters')
# plt.xlabel('Número de Clusters (k)')
# plt.ylabel('Inercia')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("elbow_method.png")
# plt.show()



# --- 3. Elegir k y aplicar KMeans ---
optimal_k = 7  # <-- AQUÍ defines el k que elijas basándote en el gráfico del codo
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(data_scaled)

# Añadir los clusters al dataframe original
data_selected_with_clusters = data_selected.copy()
data_selected_with_clusters['Cluster'] = clusters

# --- 4. Analizar resultados ---
print("\nNúmero de elementos en cada cluster:")
print(data_selected_with_clusters['Cluster'].value_counts())

# (Opcional) Visualizar usando solo las 2 primeras variables principales (PCA)
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(data_pca[:, 0], data_pca[:, 1], c=clusters, cmap='viridis', s=50)
plt.title('Visualización de Clusters con PCA')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.grid(True)
plt.tight_layout()
plt.savefig("kmeans_pca_clusters.png")
plt.show()