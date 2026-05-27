import pandas as pd
import random

categories = {
    "Cloud/Software": [
        "AWS {service} monthly hosting bill",
        "Azure {tier} subscription fee",
        "Google Cloud Platform {usage} charges",
        "Zoom {plan} license renewal",
        "Salesforce CRM {edition}",
        "GitHub team plan for {seats} users",
        "Dropbox business storage {tb} TB",
        "Microsoft 365 {license} annual fee",
        "Adobe Creative Cloud {product} license",
        "Slack {tier} grid",
    ],
    "Logistics": [
        "DHL {type} courier charges",
        "FedEx {service} shipping fee",
        "Blue Dart express parcel",
        "UPS ground freight {weight}kg",
        "Maersk container transport",
        "TNT freight invoice",
        "USPS priority mail {tracking}",
        "Canada Post {method} delivery",
        "Royal Mail international shipping",
        "DPD pick‑and‑deliver service",
    ],
    "Office Supplies": [
        "Staples printer paper {reams} reams",
        "HP ink cartridges {color}",
        "Desk chair ergonomic model",
        "Notebooks and pens bulk order",
        "Whiteboard markers set of {count}",
        "Avery label stickers {size}",
        "Bic ballpoint pens box of 50",
        "Post‑it notes pack {count}",
        "Brother toner cartridge {model}",
        "Scotch tape dispenser",
    ],
    "Utilities": [
        "Electricity bill for {month}",
        "Water supply charges",
        "Gas heating invoice",
        "Internet broadband monthly",
        "Waste collection fee",
        "Sewer service charge",
        "Street lighting tax",
        "Recycling program fee",
        "Electricity demand charge",
        "Water treatment cost",
    ],
    "Travel": [
        "Uber ride to {airport} airport",
        "Delta flight {number}",
        "Marriott hotel {nights} nights",
        "Train ticket to {destination}",
        "Car rental for {days} days",
        "Lyft business trip receipt",
        "American Airlines domestic flight",
        "Hilton conference rate",
        "Enterprise rental SUV",
        "Amtrak Acela ticket",
    ],
    "Inventory": [
        "Steel beams {tons} tons",
        "Warehouse pallets order",
        "Packaging supplies {units} units",
        "Electronics components bulk",
        "Furniture restock",
        "Plastic containers {liters} L",
        "Safety gloves dozen pack",
        "Cleaning supplies inventory",
        "Labels and barcodes rolls",
        "Shipping boxes 200ct",
    ],
}

# Placeholder values
services = ["EC2", "S3", "RDS", "Lambda"]
tiers = ["Basic", "Standard", "Premium"]
usages = ["compute", "storage", "network"]
plans = ["Pro", "Business", "Enterprise"]
editions = ["Professional", "Enterprise"]
licenses = ["E3", "E5", "Business Premium"]
products = ["Creative Cloud", "Photoshop", "Premiere Pro"]
types = ["Express", "Ground", "Overnight"]
services_other = ["Ground", "Freight", "Next Day"]
weights = [1, 5, 10, 20]
trackings = [123456, 789012, 345678]
methods = ["Expedited", "Priority", "Regular"]
reams = [1, 2, 5, 10]
colors = ["black", "color", "cyan", "magenta"]
counts = [50, 100, 200, 500]
sizes = ["small", "medium", "large"]
models = ["HL‑L2350DW", "DCP‑L2550DW"]
months = ["January", "February", "March", "April", "May", "June"]
airports = ["JFK", "ORD", "LAX", "ATL", "DEN"]
numbers = [100, 200, 300, 400]
nights = [1, 2, 3, 5]
destinations = ["Boston", "Chicago", "San Francisco"]
days = [1, 2, 3, 7]
tons = [1, 5, 10, 20]
units = [100, 500, 1000]
liters = [5, 10, 20]

rows = []
for cat, templates in categories.items():
    for _ in range(350):  # 350 per category → 2100 total
        template = random.choice(templates)
        text = template.format(
            service=random.choice(services),
            tier=random.choice(tiers),
            usage=random.choice(usages),
            plan=random.choice(plans),
            edition=random.choice(editions),
            seats=random.randint(5, 50),
            tb=random.choice([1, 2, 5]),
            license=random.choice(licenses),
            product=random.choice(products),
            type=random.choice(types),
            service_other=random.choice(services_other),
            weight=random.choice(weights),
            tracking=random.choice(trackings),
            method=random.choice(methods),
            reams=random.choice(reams),
            color=random.choice(colors),
            count=random.choice(counts),
            size=random.choice(sizes),
            model=random.choice(models),
            month=random.choice(months),
            airport=random.choice(airports),
            number=random.choice(numbers),
            nights=random.choice(nights),
            destination=random.choice(destinations),
            days=random.choice(days),
            tons=random.choice(tons),
            units=random.choice(units),
            liters=random.choice(liters),
        )
        rows.append({"text": text, "category": cat})

df = pd.DataFrame(rows).drop_duplicates()
df.to_csv("data/sample_data_big.csv", index=False)
print(f"Generated {len(df)} rows → saved to data/sample_data_big.csv")