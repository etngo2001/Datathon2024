import csv
import pandas

def clean_data():
  data = pandas.read_csv('Datathon2024\Drug_overdose_death_rates__by_drug_type__sex__age__race__and_Hispanic_origin__United_States_20240518.csv')

  data = data[data["STUB_NAME"] != "Total"]

  data["SEX"] = None
  data["RACE"] = None
  data["HISPANIC ORIGIN"] = None
  data["DRUG"] = None

  for idx, row in data.iterrows():
    name = row["STUB_NAME"].upper().replace("(SINGLE RACE)", "").strip()
    label = row["STUB_LABEL"]
    drug = row["PANEL"]

    if row["STUB_NAME"] != "TOTAL":
      column_keys = name.split(" AND ")
      for keyword in ["AGE"]: # loop to remove any unnecessary keywords, in this case there is already an age column
        if keyword in column_keys:
          column_keys.remove(keyword)
      if "RACE" and "HISPANIC ORIGIN" in column_keys:
        column_keys.append(column_keys.pop(1))

      info = label.split(": ")

      for i in range(len(column_keys)):
        key = column_keys[i]
        data.at[idx, key] = info[i]

    data.at[idx, "DRUG"] = drug_classification(drug)

  data = data[["YEAR", "DRUG", "SEX", "AGE", "RACE", "HISPANIC ORIGIN", "ESTIMATE"]]

  data.to_csv("cleaned_demographic_data",index=False)

def clean_all_demographic_data():
  data = pandas.read_csv('Datathon2024\Drug_overdose_death_rates__by_drug_type__sex__age__race__and_Hispanic_origin__United_States_20240518.csv')

  data = data[data["STUB_NAME"] == "Total"]

  data["DRUG"] = None

  for idx, row in data.iterrows():
    drug = row["PANEL"]
    data.at[idx, "DRUG"] = drug_classification(drug)

  for key in ["SEX", "RACE", "HISPANIC ORIGIN"]:
    data[key] = None

  data = data[["YEAR", "DRUG", "SEX", "AGE", "RACE", "HISPANIC ORIGIN", "ESTIMATE"]]

  data.to_csv("cleaned_all_demographic_data.csv", index=False)

def drug_classification(str):
  mapping = {
        "All drug overdose deaths": "all",
        "Drug overdose deaths involving any opioid": "any opioid",
        "Drug overdose deaths involving heroin": "heroin",
        "Drug overdose deaths involving methadone": "methadone",
        "Drug overdose deaths involving natural and semisynthetic opioids": "natural and semisynthetic opioids",
        "Drug overdose deaths involving other synthetic opioids (other than methadone)": "other synthetic opioids (other than methadone)"
    }
  return mapping.get(str)

def tailor_data(file_path):
  data = pandas.read_csv(file_path)
  # Delete rows of data where the Estimate has no value
  data.dropna(subset="ESTIMATE", inplace=True)
  # Replace None values with "Not Specified"
  data.fillna(value="Not Specified", inplace=True)
  data.to_csv(file_path, index=False)

def combine_data(file_path1, file_path2):
  df1 = pandas.read_csv(file_path1)
  df2 = pandas.read_csv(file_path2)
  df = pandas.concat([df1, df2], ignore_index=True)
  df.to_csv("cleaned_drug_overdose_deathrate_data.csv", index=False)

# clean_all_demographic_data()
#tailor_data("cleaned_all_demographic_data.csv")
# clean_data()
# tailor_data("cleaned_demographic_data.csv")
# combine_data("cleaned_demographic_data.csv", "cleaned_all_demographic_data.csv")


