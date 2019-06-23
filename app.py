from flask import Flask, request, make_response, jsonify
from reviews import get_lending_tree_reviews

app = Flask(__name__)


@app.route('/')
def root():
    return jsonify({
        'routes': {
            'path': '/lender',
            'methods': ['GET'],
            'required_query_parameters': 'url'
        }
    })


@app.route('/lender')
def lender_reviews():
    url = request.args.get('url')
    if url is None:
        return make_response(jsonify({'error': 'url query parameter not provided'}), 400)

    reviews = get_lending_tree_reviews(url)
    if reviews is None:
        return make_response(jsonify({'error': f'unable to get reviews for {url}'}), 404)
    return jsonify(get_lending_tree_reviews(url))


if __name__ == '__main__':
    app.run(debug=True)
