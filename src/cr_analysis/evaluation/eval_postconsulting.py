#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import re 

#===== CONFIGURATION ==============================#
survey_file = 'results-survey.csv'
survey_year = 2023
#===== INITIALISATION =============================#


#===== DEFINITIONS ================================#
#-- Definition of desired aspects
aspects = [
    'Please rate your experience of the following aspects of the consultation [Response time]',
    'Please rate your experience of the following aspects of the consultation [Methods of communication (i.e. emails, video calls, face-to-face meetings, etc.)]',
    'Please rate your experience of the following aspects of the consultation [Relevance of support given during the consultation]',
    'Please rate your experience of the following aspects of the consultation [Impact of the consultation on your project or work]'
]
recommendation_column = 'How likely are you to recommend using these consultation services to others?  []'

#===== FUNCTIONS ==================================#
#-- Function to convert string to numeric values
def convert_rating_to_numeric(rating_text):
    if rating_text == "10 (Extremely likely)":
        return 10
    elif rating_text == "0 (Not likely at all)":
        return 0
    else:
        return pd.to_numeric(rating_text, errors='coerce')

#-- Function to calculate percentage values
def calculate_aspect_percentages(df):
    percentages = {}
    for aspect in aspects:
        percentages[aspect] = df[aspect].value_counts(normalize=True) * 100
    return percentages

#-- Funktion zur Berechnung der durchschnittlichen Bewertung
def calculate_average_rating(df, aspect):
    ratings_mapping = {"Very poor": 1, "Below average": 2, "Average": 3, "Above average": 4, "Excellent": 5}
    df_mapped = df[aspect].map(ratings_mapping)
    return df_mapped.mean()

#-- Funktion zur Berechnung des NPS und Ausgabe der Zahlen für Promotoren und Detraktoren
def calculate_nps(dataframe):
    promoters = dataframe[dataframe[recommendation_column] >= 9]
    passives = dataframe[(dataframe[recommendation_column] == 7) | (dataframe[recommendation_column] == 8)]
    detractors = dataframe[dataframe[recommendation_column] <= 6]

    if len(dataframe) > 0:
        promoter_count = len(promoters)
        detractor_count = len(detractors)
        nps = (promoter_count - detractor_count) / len(dataframe) * 100
        return nps, promoter_count, len(passives), detractor_count
    else:
        return None, 0, 0, 0



#==================================================#
#===== PROGRAM ====================================#

#-- Reading csv data to a pandas dataframe
df = pd.read_csv(survey_file)

#-- Conversion and configurations of the data
df['Date started'] = pd.to_datetime(df['Date started'])
df['Date last action'] = pd.to_datetime(df['Date last action'])

#-- Apply function 'convert_rating_to_numeric to the designated column
df[recommendation_column] = df[recommendation_column].apply(convert_rating_to_numeric)

#-- Filtering of the datasets
df = df[df['Date last action'].dt.year == survey_year]

#-- Calculation of the overall ratings
percentages = calculate_aspect_percentages(df)

# Berechnen Sie die durchschnittlichen Bewertungen
average_ratings = {aspect: calculate_average_rating(df, aspect) for aspect in aspects}

# Berechnung des NPS
nps, promoters, passives, detractors = calculate_nps(df)

#===== END PROGRAM ================================#
#==================================================#


#===== OUTPUT =====================================#
#-- Output evaluation 
print("\n===============================")
print(f"Evaluation for {survey_year}:")
for aspect, percentages in percentages.items():
    print(f"{aspect}:")
    print(percentages)

print("\n-------------------------------")
# Ausgabe der durchschnittlichen Bewertungen
print(f"Average Rating for {survey_year}:")
print(average_ratings)

print("\n-------------------------------")
#-- Output of the NPS
print(f"Net Promoter Score (NPS) for {survey_year}: {nps:.1f}, Promotoren: {promoters}, Passives: {passives}, Detraktoren: {detractors}")


#===== PLOTS ======================================#

## Erstellen Sie Listen für die Plots und extrahieren Sie den Text innerhalb der eckigen Klammern
#aspects_list = [re.search(r'\[(.*?)\]', re.sub(r'\(.*?\)', '', aspect)).group(1) if re.search(r'\[(.*?)\]', re.sub(r'\(.*?\)', '', aspect)) else re.sub(r'\(.*?\)', '', aspect).strip() for aspect in aspects]
#ratings_2023 = [average_ratings_2023[aspect] for aspect in aspects]
#ratings_2022 = [average_ratings_2022[aspect] for aspect in aspects]
#
## Erstellen Sie ein Balkendiagramm
#x = list(range(len(aspects_list)))  # die Label-Positionen, konvertiert in eine Liste von int
#width = 0.35  # die Breite der Balken
#
#fig, ax = plt.subplots()
#rects1 = ax.bar([xi - width/2 for xi in x], ratings_2023, width, label='2023')
#rects2 = ax.bar([xi + width/2 for xi in x], ratings_2022, width, label='2022')
#
## Hinzufügen von Texten für Labels, Titel und benutzerdefinierte X-Achsen-Tick-Labels usw.
#ax.set_ylabel('Average ratings (0: Very poor - 5: Excellent)')
#ax.set_title('Average ratings according to aspects of consulting and year')
#ax.set_xticks(x)
#ax.set_xticklabels(aspects_list, rotation=45, ha="right")
#ax.legend()
#
## Zeigen Sie die Diagramme
#plt.show()


## ---------- ##
## -- TRAY -- ##
## ---------- ##
#df = df[(df['Date started'].dt.year == 2023) | (df['Date last action'].dt.year == 2023)]
#print(df.head())
