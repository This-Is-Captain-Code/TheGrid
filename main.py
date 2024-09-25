from flask import Flask, jsonify, request
import objaverse.xl as oxl

app = Flask(__name__)

@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    download_dir = request.args.get('download_dir', "~/.objaverse")
    limit = int(request.args.get('limit', 10))  # Default to 10 annotations if limit is not provided
    annotations = oxl.get_annotations(download_dir=download_dir)
    limited_annotations = annotations.head(limit)  # Limit the number of annotations
    return jsonify(limited_annotations.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
