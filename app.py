from flask import Flask, request, jsonify
from tools import FactCheck, ProvideQuestionsForArticle, ProvideAnswerForArticle
import os
from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

CORS(app)  # Allow all origins

# Define a root endpoint that provides documentation
@app.route('/', methods=['GET'])
def documentation():
    doc = {
        "API Documentation": {
            "factcheck": {
                "description": "Perform fact-checking on a given query",
                "method": "GET",
                "endpoint": "/factcheck",
                "parameters": {
                    "query": "The query to be fact-checked"
                },
                "example": {
                    "url": "/factcheck?query=Is+the+earth+flat"
                },
                "response": {
                    "result": "The fact-checked result"
                }
            },
            "fetch_questions": {
                "description": "Fetch questions based on the provided article URL",
                "method": "GET",
                "endpoint": "/fetch_questions",
                "parameters": {
                    "url": "The URL of the article for which questions are to be fetched"
                },
                "example": {
                    "url": "/fetch_questions?url=https://example.com/article"
                },
                "response": {
                    "result": "List of questions generated for the article",
                    "document": "Serialized document content and metadata"
                }
            },
            "answer_questions": {
                "description": "Provide answers to questions based on a given article URL and input query",
                "method": "GET",
                "endpoint": "/answer_questions",
                "parameters": {
                    "url": "The URL of the article",
                    "query": "The specific question to be answered"
                },
                "example": {
                    "url": "/answer_questions?url=https://example.com/article&query=What+is+the+main+topic"
                },
                "response": {
                    "result": "Answer to the input question"
                }
            }
        }
    }
    return jsonify(doc)

# Define an endpoint to use the function
@app.route('/factcheck', methods=['GET'])
def factcheck():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    result = FactCheck(query)
    return jsonify({'result': result})

# Fetch questions
@app.route('/fetch_questions', methods=['GET'])
def fetch_questions():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result, document = ProvideQuestionsForArticle(url)
    if not result:
        return jsonify({'error': 'Failed to generate questions'}), 500

    # Serialize the Document object
    serialized_document = {
        "page_content": document.page_content,
        "metadata": document.metadata
    }

    return jsonify({'result': result, 'document': serialized_document})

# Answer questions
@app.route('/answer_questions', methods=['GET'])
def answer_questions():
    # Extract URL and input query from the request parameters
    url = request.args.get('url')
    input_query = request.args.get('query')

    if not url or not input_query:
        return jsonify({'error': 'Both URL and query parameters are required'}), 400

    # Call the function to generate answers
    result = ProvideAnswerForArticle(url, input_query)
    if not result:
        return jsonify({'error': 'Failed to generate an answer'}), 500

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)