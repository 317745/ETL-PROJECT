import requests
from tqdm import tqdm

# ------------------------------
# 1. Funciones auxiliares
# ------------------------------

def check_not_empty(name, data):
    if not data:
        print(f"❌ ERROR: {name} está vacío")
    else:
        print(f"✔️ OK: {name} contiene {len(data)} registros")


def check_required_keys(name, data, required_keys):
    missing = []
    for item in data:
        for key in required_keys:
            if key not in item:
                missing.append(key)
    if missing:
        print(f"❌ ERROR en {name}: faltan llaves -> {set(missing)}")
    else:
        print(f"✔️ OK: Todas las llaves requeridas están presentes en {name}")


def check_unique_ids(name, data, id_key="id"):
    ids = [item[id_key] for item in data if id_key in item]
    if len(ids) != len(set(ids)):
        print(f"❌ ERROR: IDs duplicados en {name}")
    else:
        print(f"✔️ OK: No hay IDs duplicados en {name}")


# ------------------------------
# 2. Llamados a la API
# ------------------------------

print("\n📌 Descargando regiones…")
reqRegiones = requests.get("https://api-colombia.com/api/v1/Region").json()

print("📌 Descargando departamentos por región…")
reqDepartaments = [
    requests.get(f"https://api-colombia.com/api/v1/Region/{region}/departments").json()
    for region in tqdm(range(1, 7))
]


# ------------------------------
# 3. Validaciones
# ------------------------------

print("\n==============================")
print("VALIDACIÓN DE REGIONES")
print("==============================")

check_not_empty("Regiones", reqRegiones)
check_required_keys("Regiones", reqRegiones, ["id", "name"])
check_unique_ids("Regiones", reqRegiones)


print("\n==============================")
print("VALIDACIÓN DE DEPARTAMENTOS")
print("==============================")

# aplanar lista de listas
flat_departments = [d for region_list in reqDepartaments for d in region_list]

check_not_empty("Departamentos", flat_departments)
check_required_keys("Departamentos", flat_departments, ["id", "name", "regionId"])
check_unique_ids("Departamentos", flat_departments)

print("\n✨ Validación completa.\n")
