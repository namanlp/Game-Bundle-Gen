import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder


# Import the Data
data = pd.read_excel('./Games_Purchase_Data.xlsx')

# Convert the data in the form of array of arrays
transactions = []
for index, row in data.iterrows():
    a = []
    for i in row:
        if type(i) == str:
            a.append(str(i))
    transactions.append(a)

# Test Print the data
# print(transactions[0:5])

# Encode the transactions for FP Growth Function
te = TransactionEncoder()
te.fit(transactions)
encoded_transactions = te.transform(transactions)
encoded_transactions_df = pd.DataFrame(encoded_transactions)

# Use FP Growth and find trends
frequent_item_set = fpgrowth(encoded_transactions_df, min_support=0.20)

# Sorting thee result
frequent_item_set = frequent_item_set.sort_values(by="support", ascending=False)
print("\nTop 10 Trending Game Bundles are :\n")
# print(frequent_item_set)

index = 1

for item_set in frequent_item_set.itemsets:
    if index > 10:
        break
    if len(item_set) >= 2:
        print(str(index) + ".", end=' ')
        index += 1

        # Frozen set to List
        item_set = list(item_set)

        # Retrieve actual games from encoder
        games = list(map(lambda x: te.columns_[x], item_set))

        # Print Games
        print(*games, sep=', ')
