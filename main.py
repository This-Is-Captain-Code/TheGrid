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

##### the latest working one

# from flask import Flask, jsonify, request, send_file
# import objaverse  # Import objaverse for Objaverse API
# import threading
# import os
# import logging
# from flask_cors import CORS  # Import CORS

# # Configure logging
# logging.basicConfig(level=logging.INFO)  # Set log level to INFO for more concise output

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Global variable to store cached annotations and index
# cached_annotations = {}
# name_index = {}

# def cache_all_annotations():
#     """Load and cache all annotations when the app starts."""
#     global cached_annotations, name_index
#     try:
#         uids = objaverse.load_uids()  # Load all UIDs
#         cached_annotations = objaverse.load_annotations(uids=uids)  # Load all annotations
#         # Build an index for names to make search faster
#         for uid, annotation in cached_annotations.items():
#             name = annotation.get('name', '').lower()
#             if name:
#                 if name in name_index:
#                     name_index[name].append(uid)
#                 else:
#                     name_index[name] = [uid]
#         logging.info(f"Cached {len(cached_annotations)} annotations.")
#     except Exception as e:
#         logging.error(f"Error while caching annotations: {str(e)}")

# # Start a thread to cache annotations when the app starts
# threading.Thread(target=cache_all_annotations).start()

# @app.route('/get_annotations', methods=['GET'])
# def get_annotations():
#     search_term = request.args.get('search', '').lower()  # Get the search term
#     limit = int(request.args.get('limit', 10))  # Default to 10 results if limit is not provided

#     # Direct lookup in the name index
#     matched_uids = []
#     for name, uids in name_index.items():
#         if search_term in name:
#             matched_uids.extend(uids)
#         if len(matched_uids) >= limit:
#             break

#     # Prepare the response with metadata and thumbnails
#     response = []
#     for uid in matched_uids[:limit]:
#         annotation = cached_annotations[uid]
#         thumbnails = annotation.get('thumbnails', {}).get('images', [])
#         thumbnail_url = thumbnails[0]['url'] if thumbnails else None  # Get the first thumbnail if available

#         response.append({
#             'uid': uid,
#             'name': annotation.get('name', 'Unnamed'),
#             'thumbnail': thumbnail_url,
#             'viewerUrl': annotation.get('viewerUrl'),
#             'embedUrl': annotation.get('embedUrl'),
#             'description': annotation.get('description', ''),
#             'source': annotation.get('source')
#         })

#     return jsonify(response)

# @app.route('/download_model/<uid>', methods=['GET'])
# def download_model(uid):
#     """Download the 3D model based on its UID."""
#     try:
#         logging.debug(f"Received request to download model with UID: {uid}")

#         # Load objects based on UID and download them
#         download_dir = '/tmp/objaverse_models'  # Directory for downloaded models
#         os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

#         # Download the object using Objaverse's load_objects function
#         objects = objaverse.load_objects(uids=[uid], download_processes=1)

#         # Log the objects dict returned by Objaverse
#         logging.debug(f"Loaded objects: {objects}")

#         # Get the local file path of the downloaded model
#         file_path = objects.get(uid)

#         if file_path and os.path.exists(file_path):
#             logging.info(f"Successfully found model at {file_path}, preparing to send.")
#             return send_file(file_path, as_attachment=True)
#         else:
#             logging.error(f"Model not found for UID: {uid}")
#             return jsonify({'error': 'Model not found'}), 404

#     except Exception as e:
#         logging.error(f"Error in download_model: {str(e)}")
#         return jsonify({'error': 'Error downloading model'}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

from flask import Flask, jsonify, request, send_file
import objaverse.xl as oxl  # Using Objaverse-XL for annotations from multiple sources
import threading
import os
import logging
from flask_cors import CORS  # Import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set log level to INFO for more concise output

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store cached annotations and index
cached_annotations = {}
name_index = {}

def cache_all_annotations():
    """Load and cache all annotations when the app starts."""
    global cached_annotations, name_index
    try:
        # Load annotations from all sources (Objaverse-XL)
        cached_annotations = oxl.get_annotations().to_dict(orient='index')
        
        # Build an index for names to make search faster
        for uid, annotation in cached_annotations.items():
            name = annotation.get('name', '').lower()
            if name:
                if name in name_index:
                    name_index[name].append(uid)
                else:
                    name_index[name] = [uid]
        logging.info(f"Cached {len(cached_annotations)} annotations.")
    except Exception as e:
        logging.error(f"Error while caching annotations: {str(e)}")

# Start a thread to cache annotations when the app starts
threading.Thread(target=cache_all_annotations).start()

@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    search_term = request.args.get('search', '').lower()  # Get the search term
    limit = int(request.args.get('limit', 10))  # Default to 10 results if limit is not provided
    global_source = request.args.get('global_source', '').lower()  # Get global source filter
    sketchfab_metadata = request.args.get('sketchfab_metadata', '').lower()  # Get Sketchfab-specific metadata filter

    # Direct lookup in the name index
    matched_uids = []
    for name, uids in name_index.items():
        if search_term in name:
            for uid in uids:
                annotation = cached_annotations[uid]
                # Filter based on global source
                if global_source and annotation['source'].lower() != global_source:
                    continue
                matched_uids.append(uid)
            if len(matched_uids) >= limit:
                break

    # Sketchfab metadata filtering
    if global_source == 'sketchfab' and sketchfab_metadata:
        matched_uids = [uid for uid in matched_uids if sketchfab_metadata in 
                        [tag['name'].lower() for tag in cached_annotations[uid].get('tags', [])]]

    # Prepare the response with metadata and thumbnails
    response = []
    for uid in matched_uids[:limit]:
        annotation = cached_annotations[uid]
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

@app.route('/download_model/<uid>', methods=['GET'])
def download_model(uid):
    """Download the 3D model based on its UID."""
    try:
        logging.debug(f"Received request to download model with UID: {uid}")

        # Load objects based on UID and download them
        download_dir = '/tmp/objaverse_models'  # Directory for downloaded models
        os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

        # Download the object using Objaverse's load_objects function
        objects = oxl.download_objects(uids=[uid], download_dir=download_dir)

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
