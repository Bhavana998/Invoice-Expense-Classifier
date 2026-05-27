import pandas as pd
import random
import re

df = pd.read_csv("data/sample_data.csv")
original_count = len(df)

# Rich synonym dictionary
synonyms = {
    "courier": ["delivery", "shipping", "transport", "dispatch", "freight", "carrier"],
    "charges": ["fee", "cost", "expense", "bill", "payment", "invoice"],
    "office": ["workplace", "desk", "cubicle", "admin", "corporate"],
    "supplies": ["materials", "equipment", "stationery", "consumables", "items"],
    "cloud": ["hosting", "saas", "online service", "virtual", "web"],
    "software": ["application", "tool", "platform", "system", "program"],
    "utility": ["service", "supply", "provision", "resource"],
    "travel": ["trip", "journey", "commute", "business trip", "transportation"],
    "inventory": ["stock", "warehouse goods", "supply stock", "merchandise", "store"],
    "monthly": ["monthly recurring", "monthly fee", "per month", "each month"],
    "bill": ["invoice", "statement", "charge", "payment due"],
    "hosting": ["web hosting", "server hosting", "cloud server", "vm hosting"],
}

def augment_text(text, num_variants=8):
    variants = []
    for _ in range(num_variants):
        words = text.split()
        new_words = []
        for w in words:
            if w.lower() in synonyms and random.random() < 0.4:
                new_words.append(random.choice(synonyms[w.lower()]))
            else:
                new_words.append(w)
        # Randomly swap two words (5% chance)
        if random.random() < 0.05 and len(new_words) > 1:
            i, j = random.sample(range(len(new_words)), 2)
            new_words[i], new_words[j] = new_words[j], new_words[i]
        variants.append(" ".join(new_words))
    return variants

new_rows = []
for _, row in df.iterrows():
    # Keep original
    new_rows.append({"text": row["text"], "category": row["category"]})
    # Add augmented variants
    for aug_text in augment_text(row["text"]):
        new_rows.append({"text": aug_text, "category": row["category"]})

new_df = pd.DataFrame(new_rows).drop_duplicates(subset=["text"])
print(f"Original: {original_count} → New: {len(new_df)} rows")
new_df.to_csv("data/sample_data_augmented.csv", index=False)
print("Saved to data/sample_data_augmented.csv")