import pandas as pd

from mlxtend.preprocessing import TransactionEncoder

from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)


def run_apriori(transaction_file):

    df = pd.read_csv(transaction_file)

    #Which items occured in same transcation
    transactions = (
        df.groupby("Transaction_ID")["Food_Item"]
        .apply(list)
        .tolist()
    )

    encoder = TransactionEncoder()

    #1- item exists in transcation
    encoded = encoder.fit(
        transactions
    ).transform(transactions)

    #result in pandas df
    basket = pd.DataFrame(
        encoded,
        columns=encoder.columns_
    )

    frequent_items = apriori(
        basket,
        min_support=0.05,
        use_colnames=True
    )

    rules = association_rules(
        frequent_items,
        metric="confidence",
        min_threshold=0.30
    )

    return frequent_items, rules


if __name__ == "__main__":

    from pathlib import Path

    backend_folder = Path(__file__).resolve().parent.parent

    transaction_file = (
        backend_folder /
        "data" /
        "canteen_transactions.csv"
    )

    frequent_items, rules = run_apriori(
        transaction_file
    )

    print("\nFrequent Itemsets")

    print(
        frequent_items.head(10)
    )

    print("\nAssociation Rules")

    if len(rules) > 0:

        result = rules[
            [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
        ]

        print(result.head(10))

    else:

        print("No association rules found.")