from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the pre-trained model (update the path as needed)
model = load_model('disease_prediction_tf_model.h5')

# Disease-Symptoms Mapping
disease_symptoms = {
    "Fungal infection": ["Itching", "Skin rash", "Redness", "Cracked skin", "Blisters"],
    "Allergy": ["Sneezing", "Runny nose", "Watery eyes", "Itchy skin", "Rashes"],
    "GERD": ["Heartburn", "Chest pain", "Sour taste in mouth", "Regurgitation", "Difficulty swallowing"],
    "Chronic cholestasis": ["Jaundice", "Itching", "Fatigue", "Dark urine", "Pale stools"],
    "Drug Reaction": ["Skin rash", "Fever", "Itching", "Swelling", "Difficulty breathing"],
    "Peptic ulcer disease": ["Abdominal pain", "Bloating", "Heartburn", "Nausea", "Vomiting"],
    "AIDS": ["Weight loss", "Chronic diarrhea", "Fever", "Fatigue", "Night sweats"],
    "Diabetes": ["Increased thirst", "Frequent urination", "Blurred vision", "Fatigue", "Weight loss"],
    "Gastroenteritis": ["Diarrhea", "Vomiting", "Abdominal cramps", "Fever", "Nausea"],
    "Bronchial Asthma": ["Wheezing", "Shortness of breath", "Coughing", "Chest tightness", "Fatigue"],
    "Hypertension": ["Headache", "Dizziness", "Blurred vision", "Chest pain", "Nosebleeds"],
    "Migraine": ["Severe headache", "Nausea", "Sensitivity to light/sound", "Visual disturbances", "Vomiting"],
    "Cervical spondylosis": ["Neck pain", "Stiffness", "Numbness in arms", "Headache", "Muscle weakness"],
    "Paralysis (brain hemorrhage)": ["Loss of muscle control", "Slurred speech", "Confusion", "Sudden headache", "Numbness"],
    "Jaundice": ["Yellowing of skin/eyes", "Fatigue", "Dark urine", "Itchy skin", "Pale stool"],
    "Malaria": ["High fever", "Chills", "Sweating", "Headache", "Muscle pain"],
    "Chickenpox": ["Itchy rash", "Fever", "Fatigue", "Loss of appetite", "Red spots/blisters"],
    "Dengue": ["High fever", "Headache", "Muscle pain", "Rash", "Joint pain"],
    "Typhoid": ["High fever", "Weakness", "Abdominal pain", "Constipation or diarrhea", "Loss of appetite"],
    "Hepatitis A": ["Fatigue", "Loss of appetite", "Jaundice", "Nausea", "Abdominal pain"],
    "Hepatitis B": ["Joint pain", "Fatigue", "Jaundice", "Abdominal discomfort", "Dark urine"],
    "Hepatitis C": ["Fatigue", "Joint pain", "Jaundice", "Loss of appetite", "Nausea"],
    "Hepatitis D": ["Jaundice", "Fatigue", "Abdominal pain", "Vomiting", "Dark urine"],
    "Hepatitis E": ["Nausea", "Jaundice", "Fever", "Abdominal pain", "Dark urine"],
    "Alcoholic hepatitis": ["Jaundice", "Loss of appetite", "Fever", "Nausea", "Abdominal pain"],
    "Tuberculosis": ["Cough with blood", "Weight loss", "Night sweats", "Fever", "Chest pain"],
    "Common Cold": ["Sneezing", "Runny nose", "Sore throat", "Cough", "Mild fever"],
    "Pneumonia": ["Cough with phlegm", "Chest pain", "Fever", "Fatigue", "Shortness of breath"],
    "Hemorrhoids (piles)": ["Rectal bleeding", "Pain while sitting", "Itching", "Swelling around anus", "Lump near anus"],
    "Heart attack": ["Chest pain", "Shortness of breath", "Nausea", "Sweating", "Arm pain"],
    "Varicose veins": ["Swollen veins", "Pain after standing", "Skin discoloration", "Itching", "Cramps"],
    "Hypothyroidism": ["Fatigue", "Weight gain", "Cold intolerance", "Constipation", "Dry skin"],
    "Hyperthyroidism": ["Weight loss", "Heat intolerance", "Rapid heartbeat", "Nervousness", "Sweating"],
    "Hypoglycemia": ["Sweating", "Shakiness", "Confusion", "Hunger", "Blurred vision"],
    "Osteoarthritis": ["Joint pain", "Stiffness", "Swelling", "Limited motion", "Bone spurs"],
    "Arthritis": ["Joint pain", "Swelling", "Redness", "Stiffness", "Fatigue"],
    "Vertigo": ["Dizziness", "Loss of balance", "Nausea", "Vomiting", "Headache"],
    "Epilepsy": ["Seizures", "Loss of consciousness", "Confusion", "Stiffness", "Twitching of muscles"]
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms = data.get('symptoms', [])

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    # Identify matching diseases based on selected symptoms
    possible_diseases = []
    for disease, disease_symptom_list in disease_symptoms.items():
        if all(symptom in disease_symptom_list for symptom in symptoms):
            possible_diseases.append(disease)

    if not possible_diseases:
        return jsonify({"predictedDisease": "No matching disease found"}), 200

    # Assuming you want to use a trained model for final prediction (optional)
    # You can modify this part if needed to predict based on model or data analysis
    predicted_disease = possible_diseases[0]  # If you want to return the first matching disease

    return jsonify({"predictedDisease": predicted_disease}), 200

if __name__ == '__main__':
    app.run(debug=True)
