###
Quickstart: install packages from requirements.txt and run flask app.

The application will download the default model ('sentence-transformers/all-mpnet-base-v2') from hugging face and expose a simple api to embed sentences.

The app has been written by someone new to pyton and wanting to play around with sbert. Blame chatgpt, it wrote like half of this.  
This is not production ready, though I will be turning it into a public docker container.   

### API
- Flask web application: The rest of the code sets up a web application using Flask. This application has three endpoints:

    1. `/embed_demo`: a GET endpoint that embeds hardcoded sentences.
    2. `/embed_sentences`: a POST endpoint that takes a list of sentences as a JSON payload and returns their embeddings.
    3. `/embed_sentences/normalize`: a POST endpoint similar to `/embed_sentences` but it normalizes the embeddings.


These endpoints will accept post requests containing json arrays of sentences, which will encoded and returned as json.

```http
POST localhost:5000/embed_sentences
Content-Type: application/json

[
  "Test number one.",
  "Test 2."
]
```

The output will be in the below format (number of vectors has been truncated):

```json
[
  {
    "embedding": [
      -0.005890531465411186,
      0.024965772405266762,
      -0.0500827319920063,
      -0.018901731818914413
    ],
    "parameters": {
      "batch_size": 32,
      "device": "cpu",
      "normalize_embeddings": false
    },
    "repo": "sentence-transformers/all-mpnet-base-v2",
    "sentence": "Test number one."
  },
  {
    "embedding": [
      0.008925802074372768,
      -0.0020000915974378586,
      -0.06097005680203438,
      -0.03114527463912964,
      0.009883358143270016,
      0.03417069837450981,
      -0.019230583682656288,
      -0.06188041716814041,
      -0.019297847524285316
    ],
    "parameters": {
      "batch_size": 32,
      "device": "cpu",
      "normalize_embeddings": false
    },
    "repo": "sentence-transformers/all-mpnet-base-v2",
    "sentence": "Test 2."
  }
]

```


Note: The environment variables are used to set the options for the embedding model:

```python
options = {
    'convert_to_numpy': bool(os.getenv('CONVERT_TO_NUMPY', 'True') == 'True'),
    'convert_tensor': bool(os.getenv('CONVERT_TENSOR', 'False') == 'True'),
    'batch_size': int(os.getenv('BATCH_SIZE', 32)),
    'normalize_embeddings': bool(os.getenv('NORMALIZE_EMBEDDINGS', 'False') == 'True'),
    'device': os.getenv('DEVICE', 'cpu')
}
embedding_model = EmbeddingModel(os.getenv('REPO_ID', 'sentence-transformers/all-mpnet-base-v2'), options)

```

This serves as a practical way to modify behavior of the application without changing the source code, which might be beneficial in different environments (e.g. development, testing, production).
