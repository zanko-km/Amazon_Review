# Amazon_Review
To run the code, first install the required libraries using the following command.
```bash
pip install -r requirements.txt
```
Then, by running the pipeline, you can access the cleaned and engineered data in the database.
```bash
python pipeline.py
```
if you using `python3`:
```
python3 pipeline.py
```
If you want to run with Docker file run this commands in command prompt
```bash
docker build -t pipeline .
docker run --rm pipeline
```
