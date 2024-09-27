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

from flask import Flask, jsonify, request, send_file
import objaverse  # Import objaverse for Objaverse 1 API
import threading
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG for more detailed output

app = Flask(__name__)

# Global variable to store cached annotations
cached_annotations = {}

def cache_all_annotations():
    global cached_annotations
    try:
        uids = objaverse.load_uids()  # Load all UIDs
        cached_annotations = objaverse.load_annotations(uids=uids)  # Load all annotations
        logging.info(f"Successfully cached {len(cached_annotations)} annotations.")
    except Exception as e:
        logging.error(f"Error while caching annotations: {str(e)}")

# Start a thread to cache annotations when the app starts
threading.Thread(target=cache_all_annotations).start()

@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    try:
        search_term = request.args.get('search', '').lower()
        limit = int(request.args.get('limit', 10))
        source_filter = 'sketchfab'

        # Log the search parameters
        logging.debug(f"Received search term: {search_term}, limit: {limit}")

        filtered_annotations = {
            uid: annotation for uid, annotation in cached_annotations.items()
            if search_term in annotation.get('name', '').lower() and source_filter in annotation.get('source', '').lower()
        }

        limited_annotations = dict(list(filtered_annotations.items())[:limit])

        # Log the number of filtered results
        logging.debug(f"Filtered annotations count: {len(limited_annotations)}")

        response = []
        for uid, annotation in limited_annotations.items():
            thumbnails = annotation.get('thumbnails', {}).get('images', [])
            thumbnail_url = thumbnails[0]['url'] if thumbnails else None

            response.append({
                'uid': uid,
                'name': annotation.get('name', 'Unnamed'),
                'thumbnail': thumbnail_url,
                'viewerUrl': annotation.get('viewerUrl'),
                'embedUrl': annotation.get('embedUrl'),
                'description': annotation.get('description', ''),
                'source': annotation.get('source'),
                'fileIdentifier': annotation.get('fileIdentifier'),  # Add fileIdentifier for download
            })

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error in get_annotations: {str(e)}")
        return jsonify({'error': 'Error processing request'}), 500

@app.route('/download_model/<uid>', methods=['GET'])
def download_model(uid):
    try:
        logging.debug(f"Received request to download model with UID: {uid}")

        # Load objects based on UID and download them
        download_dir = '/tmp/objaverse_models'  # Directory for downloaded models
        os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

        # Download the object using Objaverse 1's load_objects function
        objects = objaverse.load_objects(uids=[uid], download_processes=1)

        # Log the objects dict returned by Objaverse
        logging.debug(f"Loaded objects: {objects}")

        # Get the local file path of the downloaded model
        file_path = objects.get(uid)

        if file_path and os.path.exists(file_path):
            logging.info(f"Successfully found model at {file_path}, preparing to send.")
            return send_file(file_path, as_attachment=True)
        else:
            logging.error(f"Model not found for UID: {uid}")
            return jsonify({'error': 'Model not found'}), 404

    except Exception as e:
        logging.error(f"Error in download_model: {str(e)}")
        return jsonify({'error': 'Error downloading model'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
