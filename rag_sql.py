import os
from glob import glob
from tqdm import tqdm
import argparse

from openai import OpenAI

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from sqlalchemy.ext.declarative import declarative_base

SQLBase = declarative_base()

class Document(SQLBase):
    __tablename__ = "Document"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

#Input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-q', type=str, help="Question to answer")
args = parser.parse_args()

#create db
DB_URI = 'sqlite:///DOCS.db'

db_engine = create_engine(DB_URI, echo=True)

SQLBase.metadata.drop_all(db_engine)
SQLBase.metadata.create_all(db_engine)

Session = sessionmaker(bind=db_engine)
session = Session()

#Get files
DOCS_DIR= "./documents"
filenames = glob(f"{DOCS_DIR}/**", recursive=True)

documents = []
for f in tqdm(filenames):
    try:
        content = open(f,'r').read()
        doc = Document(content=content)
        session.add(doc)
    except:
        print(f"Could not read {f}")

session.commit()

#User query
question = args.q

#RAG SQL
client = OpenAI()

llm_prompt = f"""You have access to a SQL table of documents named Document.
The schema of Document is
id: integer
content: text

A user wants to answer the following question:
{question}

Write a SQL statement to retrieve documents that contain relevant information
to answer the user question. Make the statement specific, but not overly restrictive.
Your answer should contain only the SQL statement and no
other text.
"""

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": llm_prompt},
  ]
)
print(response.choices[0])
answer = response.choices[0].message.content

query = text(answer)

q = select(Document).from_statement(query)
cursor = session.execute(q)
docs = []
for result in cursor.scalars():
    docs.append(result.content)

context = " ".join(docs)
print(context)

#final question answer
llm_prompt = f"""Please answer the following user question:
{question}

In your answer you can use the following information as context:
{context}
"""

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": llm_prompt},
  ]
)
print(response.choices[0])
