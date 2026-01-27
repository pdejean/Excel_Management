import pandas as pd
from pathlib import Path

DOSSIER = Path("excels")
SORTIE = "suivi_affaires.xlsx"

# adapte les noms si besoin (exactement comme dans Excel).0
COL_AFFAIRE = "Affaire"
COL_TOTAL = "Total"

all_rows = []

for f in DOSSIER.glob("*.xlsx"):
    employe = f.stem 

    df = pd.read_excel(f)

    df = df[[COL_AFFAIRE, COL_TOTAL]].copy()

    df[COL_AFFAIRE] = df[COL_AFFAIRE].astype(str).str.strip()
    df[COL_TOTAL] = pd.to_numeric(df[COL_TOTAL], errors="coerce").fillna(0)

    df["Employe"] = employe

    df = df[df[COL_AFFAIRE].str.len() > 0]

    all_rows.append(df)

df_detail = pd.concat(all_rows, ignore_index=True)

# Total réel par affaire (tous employés confondus)
df_total_affaire = (
    df_detail.groupby(COL_AFFAIRE, as_index=False)[COL_TOTAL]
    .sum()
    .rename(columns={COL_TOTAL: "Heures_Reelles"})
)

# Onglet "Affectations" : on liste qui travaille sur quoi (1 employé peut être sur plusieurs affaires)
df_affectations = (
    df_detail[df_detail["Total"] > 0]
    .groupby([COL_AFFAIRE, "Employe"], as_index=False)["Total"]
    .sum()
    .rename(columns={"Total": "Heures_Employe"})
)

# Onglet "Budget" (à compléter) : heures prévues / vendues / budgetées
df_budget = df_total_affaire[[COL_AFFAIRE]].copy()
df_budget["Heures_Budget"] = 0  # tu remplis ensuite à la main ou via un autre Excel

# Calcul du restant
df_suivi = df_total_affaire.merge(df_budget, on=COL_AFFAIRE, how="left")
df_suivi["Heures_Budget"] = pd.to_numeric(df_suivi["Heures_Budget"], errors="coerce").fillna(0)
df_suivi["Heures_Restantes"] = df_suivi["Heures_Budget"] - df_suivi["Heures_Reelles"]

with pd.ExcelWriter(SORTIE, engine="openpyxl") as writer:
    df_suivi.to_excel(writer, sheet_name="Suivi", index=False)
    df_affectations.to_excel(writer, sheet_name="Affectations", index=False)
    df_detail.to_excel(writer, sheet_name="Detail", index=False)
    df_budget.to_excel(writer, sheet_name="Budget_a_completer", index=False)

print(f"✅ Fichier créé : {SORTIE}")
