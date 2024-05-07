# RAG_SQL
Example of RAG with where LLM is used to generate SQL select statements to select relevant documents instead of using vector DB and embeddings.

Uses SQLite to store documents. Documents are loaded from a local `documents` folder. Only works with `.txt` files right now.

To download an example dataset of BBC news articles run `download_example_docs.sh`

Uses the OpenAI API, so needs the OpenAI API key environment variable to be set.

## Example
```bash
python rag_sql.py -q "What events did Sarah Claxton compete in?"
```
Response:
```text
Sarah Claxton, a British hurdler, competed in the 100m hurdles and 400m hurdles events during her athletic career. She represented Great Britain in various international competitions, including the Olympics and World Championships. Claxton was known for her speed, agility, and technique in navigating the hurdles on the track.
```
