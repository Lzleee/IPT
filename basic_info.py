import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns



with open("Grocery_and_Gourmet_Food.jsonl", "r") as file:
    df = pd.read_json(file, lines=True)
    print(df.info(show_counts=True))
    print(df.describe())
    data = {
        'rating': [0,4,5,5,5],
        'helpful_vote': [-1,0,0,1,27883]
    }
    summary_df = pd.DataFrame(data, index=['min', '25%', '50%', '75%', 'max'])

    # Plotting the box plot
    sns.set(style="whitegrid")  # Setting the seaborn style
    plt.figure(figsize=(12, 6))  # Set the figure size

    # Creating box plots
    sns.boxplot(data=summary_df, orient='v', palette="vlag")
    plt.title('Summary of rating and helpful_vote')
    plt.ylabel('Values')
    plt.tight_layout()
    plt.grid(True)
    plt.savefig('review_overview.png', dpi=200)
    print(df.columns)


with open("meta_Grocery_and_Gourmet_Food.jsonl", "r") as file:
    df_meta = pd.read_json(file, lines=True)
    print(df_meta.info(show_counts=True))
    print(df_meta.describe())
    data = {
        'average_rating': [1, 3.9, 4.3, 4.7, 5],
        'rating_number': [1, 5, 17, 74, 202066]
    }
    summary_df = pd.DataFrame(data, index=['min', '25%', '50%', '75%', 'max'])

    # Plotting the box plot
    sns.set(style="whitegrid")  # Setting the seaborn style
    plt.figure(figsize=(12, 6))  # Set the figure size

    # Creating box plots
    sns.boxplot(data=summary_df, orient='v', palette="vlag")
    plt.title('Summary of average_rating and rating_number')
    plt.ylabel('Values')
    plt.tight_layout()
    plt.grid(True)
    plt.savefig('review_overview.png', dpi=200)
    print(df.columns)