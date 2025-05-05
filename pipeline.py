import subprocess
subprocess.run(["python", "scripts/db.py"])
subprocess.run(["python", "scripts/data_preprocessing.py"])
subprocess.run(["python", "scripts/import_to_db.py"])
subprocess.run(["python", "scripts/feature_engineering.py"])