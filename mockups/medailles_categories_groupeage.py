import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

data = pd.read_csv("medallists.csv")

birth_dates = data["birth_date"].to_list()
medal_dates = data["medal_date"].to_list()
medal_types = data["medal_type"].to_list()
disciplines = data["discipline"].to_list()

ages = []
sport = []
for i in range(len(birth_dates)):
    birth_date = birth_dates[i]
    medal_date = medal_dates[i]
    medal_type = medal_types[i]

    if (medal_type == "Bronze Medal"):
        birth = birth_date.split('-')
        medal = medal_date.split('-')
        start = datetime(int(birth[0]), int(birth[1]), int(birth[2]))
        end = datetime(int(medal[0]), int(medal[1]), int(medal[2]))

        difference = end - start
        ages.append(int((difference.days + difference.seconds/86400)/365.2425))
        sport.append(disciplines[i])

age_groups = ["10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"]
nbr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sport_category = [0] * len(ages)
athlete_age_groups = [0] * len(ages)

for i in range(len(ages)):
    index = int(ages[i] / 5) - 2
    athlete_age_groups[i] = age_groups[index]
    # nbr[index] = nbr[index] + 1

    if (sport[i] == 'Table Tennis' or sport[i] == 'Badminton' or sport[i] == 'Tennis') :
        sport_category[i] = "Sports de raquette"
    elif (sport[i] == 'Triathlon' or sport[i] == 'Modern Pentathlon') :
        sport_category[i] = "-athlon"
    elif (sport[i] == 'Athletics') :
        sport_category[i] = "Athlétisme"
    elif (sport[i] == 'Canoe Sprint' or sport[i] == 'Rowing' or sport[i] == 'Surfing' or sport[i] == 'Sailing' or sport[i] =='Canoe Slalom') :
        sport_category[i] = "Sport sur bateaux"
    elif (sport[i] == 'Swimming' or sport[i] == 'Diving' or sport[i] == 'Marathon Swimming' or sport[i] == 'Artistic Swimming') :
        sport_category[i] = "Piscine"
    elif (sport[i] == 'Golf' or sport[i] == 'Shooting' or sport[i] == 'Archery') :
        sport_category[i] = "Sports de précision"
    elif (sport[i] == 'Water Polo' or sport[i] == 'Hockey' or sport[i] == 'Football' or sport[i] == 'Handball' or sport[i] == 'Basketball' or sport[i] == 'Rugby Sevens' or sport[i] == 'Beach Volleyball' or sport[i] == '3x3 Basketball' or sport[i] == 'Volleyball') :
        sport_category[i] = "Sports d'équipe"
    elif (sport[i] == 'Artistic Gymnastics' or sport[i] == 'Rhythmic Gymnastics' or sport[i] == 'Trampoline Gymnastics') :
        sport_category[i] = "Gymnastique"
    elif (sport[i] == 'Cycling BMX Freestyle' or sport[i] == 'Cycling BMX Racing' or sport[i] == 'Cycling Track' or sport[i] == 'Cycling Mountain Bike' or sport[i] == 'Cycling Road') :
        sport_category[i] = "Cyclisme"
    elif (sport[i] == 'Wrestling' or sport[i] == 'Taekwondo' or sport[i] == 'Boxing' or sport[i] == 'Judo' or sport[i] == 'Fencing') :
        sport_category[i] = "Sports de combat"
    elif (sport[i] == 'Sport Climbing' or sport[i] == 'Weightlifting' or sport[i] == 'Breaking' or sport[i] == 'Skateboarding' or sport[i] == 'Equestrian') :
        sport_category[i] = "Autres sports"

d1 = []
d2 = []
d3 = []
categories = ["Sports de raquette", "-athlon", "Athlétisme", "Sport sur bateaux", "Piscine", "Sports de précision", "Sports d'équipe", "Gymnastique", "Cyclisme", "Sports de combat", "Autres sports"]

for group in age_groups:
    for category in categories:
        number = 0
        available_number = 0
        for i in range(len(athlete_age_groups)):
            if (sport_category[i] == category):
                available_number += 1
                if (athlete_age_groups[i] == group):
                    number += 1

        if (number > 0):
            d1.append(group)
            d2.append(category)
            d3.append(number / available_number)

d = {"Groupes d'âges": d1, "Catégorie de sport": d2, "Ratio de médailles": d3}
df = pd.DataFrame(data = d)
fig = px.bar(df, x = "Groupes d'âges", y = "Ratio de médailles", color = "Catégorie de sport", title = "Ratio de médailles de bronze gagnées par rapport au groupe d'âge et à la catégorie de sport")
fig.show()