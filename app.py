from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download
import os, logging

logging.basicConfig(level=logging.INFO)

class EmbeddingModel:
    def __init__(self, repo_id, options):
        self.repo_id = repo_id
        snapshot_download(repo_id=repo_id)
        self.model = SentenceTransformer(repo_id)
        self.batch_size = options.get('batch_size', 32)
        self.normalize_embeddings = options.get('normalize_embeddings', False)
        self.device = options.get('device', 'cpu')

    def _generate_embeddings(self, sentences, override_options):
        embeddings = self.model.encode(
            sentences,
            batch_size=override_options.get('batch_size', self.batch_size),
            normalize_embeddings=override_options.get('normalize_embeddings', self.normalize_embeddings),
            device=override_options.get('device', self.device),
            show_progress_bar=False
        )
        return embeddings

    def _create_output(self, sentences, embeddings, override_options):
        out = []
        for sentence, embedding in zip(sentences, embeddings):
            s = {
                "sentence": sentence,
                "embedding": list(embedding),
                "repo": self.repo_id,
                "parameters": {
                    "batch_size": override_options.get('batch_size', self.batch_size),
                    "normalize_embeddings": override_options.get('normalize_embeddings', self.normalize_embeddings),
                    "device": override_options.get('device', self.device),
                }
            }
            out.append(s)
        return out

    def handle_sentences(self, sentences: object, override_options: object = None) -> object:
        if override_options is None:
            override_options = {}
        logging.info(f"Override options: {override_options}")
        embeddings = self._generate_embeddings(sentences, override_options).astype('float64')
        return self._create_output(sentences, embeddings, override_options)


options = {
    'convert_to_numpy': bool(os.getenv('CONVERT_TO_NUMPY', 'True') == 'True'),
    'convert_tensor': bool(os.getenv('CONVERT_TENSOR', 'False') == 'True'),
    'batch_size': int(os.getenv('BATCH_SIZE', 32)),
    'normalize_embeddings': bool(os.getenv('NORMALIZE_EMBEDDINGS', 'False') == 'True'),
    'device': os.getenv('DEVICE', 'cpu')
}
app = Flask(__name__)
embedding_model = EmbeddingModel(os.getenv('REPO_ID', 'sentence-transformers/all-mpnet-base-v2'), options)


@app.route("/embed_demo", methods=['GET'])
def embed_demo():
    sentences = [
        "This framework generates embeddings for each input sentence",
        "Sentences are passed as a list of string.",
        "The quick brown fox jumps over the lazy dog.",
    ]
    result = embedding_model.handle_sentences(sentences)
    return jsonify(result), 201


@app.route("/embed_sentences", methods=["POST"])
def embed_sentences():
    if request.is_json:
        sentences = request.get_json()
        if isinstance(sentences, list) and all(isinstance(sentence, str) for sentence in sentences):
            result = embedding_model.handle_sentences(sentences)
            return jsonify(result), 201
        else:
            return {"error": "Invalid input. Expected a list of strings."}, 400
    return {"error": "Request must be JSON"}, 415

@app.route("/embed_sentences/normalize", methods=["POST"])
def embed_sentences_normalize():
    if request.is_json:
        sentences = request.get_json()
        if isinstance(sentences, list) and all(isinstance(sentence, str) for sentence in sentences):
            normalize_options = {"normalize_embeddings": True}
            result = embedding_model.handle_sentences(sentences, normalize_options)
            return jsonify(result), 201
        else:
            return {"error": "Invalid input. Expected a list of strings."}, 400
    return {"error": "Request must be JSON"}, 415