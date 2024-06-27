import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open ("Retail_Transactions_Dataset.csv","r") as file:
    df = pd.read_csv(file)
    print(df.info(show_counts=True))
    print(df.describe())
    

    
    sns.set(style="whitegrid")

    total_items = df['Total_Items']

    
    plt.figure(figsize=(10, 6))  
    plt.hist(total_items, bins=10, color='skyblue', edgecolor='black')  
    plt.xlabel('Total Items')
    plt.ylabel('Frequency')
    plt.title('Distribution of Total Items')
    plt.xticks(rotation=45)  
    plt.tight_layout()  
    plt.savefig('Total_Items.png', dpi=200)  

    sns.set(style="whitegrid")

    total_cost = df['Total_Cost']

    
    plt.figure(figsize=(10, 6))  
    plt.hist(total_cost, bins=20, color='lightgreen', edgecolor='black')  
    plt.xlabel('Total Cost')
    plt.ylabel('Frequency')
    plt.title('Distribution of Total Cost')
    plt.xticks(rotation=45)  
    plt.tight_layout()  
    plt.savefig('Total_Cost.png', dpi=200)  
        