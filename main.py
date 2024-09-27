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

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import objaverse.xl as oxl
# import pandas as pd

# app = Flask(__name__)
# CORS(app)  # Enable CORS to allow Next.js to access this API

# # Load annotations once during server startup and cache it
# annotations_cache = oxl.get_annotations(download_dir="~/.objaverse")

# @app.route('/get_annotations', methods=['GET'])
# def get_annotations():
#     # Pagination settings
#     page = int(request.args.get('page', 1))  # Default page is 1
#     page_size = int(request.args.get('pageSize', 10))  # Default 10 results per page
#     offset = (page - 1) * page_size

#     # Get search parameters
#     search_term = request.args.get('search', '')  # Example: search by a term (optional)
#     file_type = request.args.get('fileType', '')  # Example: 'stl', 'obj' (optional)
#     source = request.args.get('source', '')  # Example: 'thingiverse', 'sketchfab' (optional)

#     # Start with the cached annotations
#     filtered_annotations = annotations_cache

#     # Apply search filtering on specific columns (fileIdentifier, source)
#     if search_term:
#         filtered_annotations = filtered_annotations[
#             filtered_annotations['fileIdentifier'].str.contains(search_term, case=False, na=False) |
#             filtered_annotations['source'].str.contains(search_term, case=False, na=False)
#         ]

#     # Filter by file type (optional)
#     if file_type:
#         filtered_annotations = filtered_annotations[filtered_annotations['fileType'] == file_type]

#     # Filter by source (optional)
#     if source:
#         filtered_annotations = filtered_annotations[filtered_annotations['source'] == source]

#     # Paginate the results
#     paginated_annotations = filtered_annotations.iloc[offset:offset + page_size]

#     # Convert to a dictionary and return as JSON
#     return jsonify(paginated_annotations.to_dict(orient='records'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

##the latest working one
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
    
#     # Filter based on metadata filename inside the metadata column
#     if search_term:
#         annotations = annotations[annotations['metadata'].apply(
#             lambda meta: isinstance(meta, dict) and search_term.lower() in str(meta.get('fileName', '')).lower()
#         )]
    
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
import objaverse
import threading

app = Flask(__name__)

# Global variable to store cached annotations
cached_annotations = {}

def cache_all_annotations():
    """Load and cache all annotations when the app starts."""
    global cached_annotations
    uids = objaverse.load_uids()  # Load all UIDs
    cached_annotations = objaverse.load_annotations(uids=uids)  # Load all annotations
    print(f"Cached {len(cached_annotations)} annotations.")

# Start a thread to cache annotations when the app starts
threading.Thread(target=cache_all_annotations).start()

@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    search_term = request.args.get('search', '').lower()  # Get the search term
    limit = int(request.args.get('limit', 10))  # Default to 10 results if limit is not provided
    source_filter = 'sketchfab'  # Limit the source to Sketchfab

    # Filter the cached annotations based on search term and source
    filtered_annotations = {
        uid: annotation for uid, annotation in cached_annotations.items()
        if search_term in annotation.get('name', '').lower() and source_filter in annotation.get('source', '').lower()
    }

    # Limit the results
    limited_annotations = dict(list(filtered_annotations.items())[:limit])

    # Prepare the response with metadata and thumbnails
    response = []
    for uid, annotation in limited_annotations.items():
        thumbnails = annotation.get('thumbnails', {}).get('images', [])
        thumbnail_url = thumbnails[0]['url'] if thumbnails else None  # Get the first thumbnail if available

        response.append({
            'uid': uid,
            'name': annotation.get('name', 'Unnamed'),
            'thumbnail': thumbnail_url,
            'viewerUrl': annotation.get('viewerUrl'),
            'embedUrl': annotation.get('embedUrl'),
            'description': annotation.get('description', ''),
            'source': annotation.get('source')
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

