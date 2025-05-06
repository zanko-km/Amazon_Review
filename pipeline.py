import subprocess
subprocess.run(["python", "Scripts/db.py"])
subprocess.run(["python", "Scripts/data_preprocessing.py"])
subprocess.run(["python", "Scripts/import_to_db.py"])
subprocess.run(["python", "Scripts/feature_engineering.py"])
