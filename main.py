# from flask import Flask, jsonify, request
# import objaverse.xl as oxl

# app = Flask(__name__)

# @app.route('/get_annotations', methods=['GET'])
# def get_annotations():
#     download_dir = request.args.get('download_dir', "~/.objaverse")
#     limit = int(request.args.get('limit', 10))  # Default to 10 annotations if limit is not provided
#     annotations = oxl.get_annotations(download_dir=download_dir)
#     limited_annotations = annotations.head(limit)  # Limit the number of annotations
#     return jsonify(limited_annotations.to_dict())

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)


# from flask import Flask, jsonify, request
# import objaverse.xl as oxl
# import pandas as pd

# app = Flask(__name__)

# @app.route('/get_annotations', methods=['GET'])
# def get_annotations():
#     download_dir = request.args.get('download_dir', "~/.objaverse")
#     limit = int(request.args.get('limit', 10))  # Default to 10 annotations if limit is not provided
    
#     # Get search parameters
#     search_term = request.args.get('search', '')  # Example search term
#     file_type = request.args.get('fileType', '')  # Filter by fileType (e.g., 'stl', 'obj')
#     source = request.args.get('source', '')  # Filter by source (e.g., 'thingiverse', 'sketchfab')

#     # Load annotations
#     annotations = oxl.get_annotations(download_dir=download_dir)
    
#     # Convert annotations DataFrame to string and apply a filter on the search term
#     if search_term:
#         annotations = annotations[annotations.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    
#     # Filter by file type and source if provided
#     if file_type:
#         annotations = annotations[annotations['fileType'] == file_type]
#     if source:
#         annotations = annotations[annotations['source'] == source]

#     # Limit the number of results
#     limited_annotations = annotations.head(limit)

#     return jsonify(limited_annotations.to_dict(orient='records'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

from flask import Flask, jsonify, request
from flask_cors import CORS
import objaverse.xl as oxl
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS to allow Next.js to access this API

# Load annotations once during server startup and cache it
annotations_cache = oxl.get_annotations(download_dir="~/.objaverse")

@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    # Pagination settings
    page = int(request.args.get('page', 1))  # Default page is 1
    page_size = int(request.args.get('pageSize', 10))  # Default 10 results per page
    offset = (page - 1) * page_size

    # Get search parameters
    search_term = request.args.get('search', '')  # Example: search by a term (optional)
    file_type = request.args.get('fileType', '')  # Example: 'stl', 'obj' (optional)
    source = request.args.get('source', '')  # Example: 'thingiverse', 'sketchfab' (optional)

    # Start with the cached annotations
    filtered_annotations = annotations_cache

    # Apply search filtering on specific columns (fileIdentifier, source)
    if search_term:
        filtered_annotations = filtered_annotations[
            filtered_annotations['fileIdentifier'].str.contains(search_term, case=False, na=False) |
            filtered_annotations['source'].str.contains(search_term, case=False, na=False)
        ]

    # Filter by file type (optional)
    if file_type:
        filtered_annotations = filtered_annotations[filtered_annotations['fileType'] == file_type]

    # Filter by source (optional)
    if source:
        filtered_annotations = filtered_annotations[filtered_annotations['source'] == source]

    # Paginate the results
    paginated_annotations = filtered_annotations.iloc[offset:offset + page_size]

    # Convert to a dictionary and return as JSON
    return jsonify(paginated_annotations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
