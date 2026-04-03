import pandas as pd
from difflib import get_close_matches

# =========================
# 📂 LOAD DATA
# =========================
df = pd.read_csv("datset/dataset.csv")
desc_df = pd.read_csv("datset/symptom_Description.csv")
prec_df = pd.read_csv("datset/symptom_precaution.csv")

# =========================
# 🧹 CLEAN FUNCTION
# =========================
def clean_text(text):
    return str(text).strip().lower().replace(" ", "_")

# =========================
# 🧠 FIND DISEASE
# =========================
def find_disease(user_symptoms):
    user_symptoms = [clean_text(s) for s in user_symptoms]

    best_match = None
    best_score = 0

    for _, row in df.iterrows():
        symptoms = row[1:].dropna().values
        symptoms = [clean_text(s) for s in symptoms]

        match_count = 0

        for user_sym in user_symptoms:
            for sym in symptoms:
                if user_sym == sym or user_sym in sym or sym in user_sym:
                    match_count += 1
                    break

        score = match_count / len(user_symptoms)

        if score > best_score:
            best_score = score
            best_match = row["Disease"]

    if best_score >= 0.6:
        return best_match
    else:
        return None

# =========================
# 📖 GET DESCRIPTION
# =========================
def get_description(disease_name):
    if not disease_name:
        return "No description available"

    disease_name = disease_name.strip().lower()
    disease_list = desc_df["Disease"].str.lower().tolist()

    match = get_close_matches(disease_name, disease_list, n=1, cutoff=0.6)

    if match:
        row = desc_df[desc_df["Disease"].str.lower() == match[0]]
        return row.iloc[0]["Description"]

    return "Description not found"

# =========================
# 💊 GET PRECAUTION
# =========================
def get_precaution(disease_name):
    if not disease_name:
        return ["No precaution available"]

    disease_name = disease_name.strip().lower()
    disease_list = prec_df["Disease"].str.lower().tolist()

    match = get_close_matches(disease_name, disease_list, n=1, cutoff=0.6)

    if match:
        row = prec_df[prec_df["Disease"].str.lower() == match[0]]

        precautions = []
        for col in row.columns[1:]:
            value = row.iloc[0][col]
            if pd.notna(value):
                precautions.append(str(value).strip())

        return precautions

    return ["No specific precautions found"]

# =========================
# 🚀 MAIN PROGRAM
# =========================
user_input = input("Enter symptoms (comma separated): ")
user_symptoms = user_input.split(",")

disease = find_disease(user_symptoms)

if disease:
    print("\n" + "="*40)
    print("🩺 Predicted Disease:", disease)

    description = get_description(disease)
    print("\n📖 Description:")
    print(description)

    precautions = get_precaution(disease)
    print("\n💊 Precautions:")
    for i, p in enumerate(precautions, 1):
        print(f"  ✔ {p}")

    print("="*40)

else:
    print("\n❌ Not enough matching symptoms. Try adding more symptoms.")