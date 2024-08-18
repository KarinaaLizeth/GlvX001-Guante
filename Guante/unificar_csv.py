import pandas as pd

def load_and_label_csv(filename, label):
    data = pd.read_csv(filename)
    data['label'] = label
    return data

# Cargar y etiquetar los datos
te_amo_data = load_and_label_csv('datos_te amo.csv', 'te amo')
escuela_data = load_and_label_csv('datos_escuela.csv', 'escuela')
comer_data = load_and_label_csv('datos_comer.csv', 'comer')
hola_data = load_and_label_csv('datos_hola.csv', 'hola')
mal_data = load_and_label_csv('datos_bien.csv', 'bien')
bien_data = load_and_label_csv('datos_mal.csv', 'mal')

# Unir todos los datasets
all_data = pd.concat([te_amo_data, comer_data, escuela_data,hola_data,mal_data,bien_data], ignore_index=True)

# Guardar el dataset unificado
all_data.to_csv('senias.csv', index=False)
