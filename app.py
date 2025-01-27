# import os
# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from rembg import remove
# from PIL import Image
# import io
# import requests
# from io import BytesIO

# app = Flask(__name__)
# CORS(app)

# @app.route('/remove-bg', methods=['POST'])# this is backend route to remove bg
# def remove_bg():
#     try:
#         print(f"Request files: {request.files}")
#         print(f"Request form data: {request.form}")

#         if 'file' in request.files:
#             file = request.files['file']
#             if file.filename == '':
#                 return jsonify({'error': 'No selected file'}), 400

#             print(f"Received file: {file.filename}")
#             input_image = Image.open(file)

#         elif 'url' in request.form:
#             url = request.form['url']
#             print(f"Received URL: {url}")
#             try:
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status()  
#                 input_image = Image.open(BytesIO(response.content))
#             except requests.exceptions.RequestException as e:
#                 return jsonify({'error': 'Failed to fetch image from the provided URL', 'details': str(e)}), 400
#             except IOError as e:
#                 return jsonify({'error': 'Invalid image format from the URL', 'details': str(e)}), 400

#         else:
#             return jsonify({'error': 'No file or URL provided'}), 400
#         output_image = remove(input_image)
#         output_stream = io.BytesIO()
#         output_image.save(output_stream, format="PNG")
#         output_stream.seek(0)
#         return send_file(output_stream, mimetype='image/png', as_attachment=True, download_name='result.png')

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({'error': str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5002)
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import requests
from io import BytesIO
import hashlib
app = Flask(__name__)
cache=Cache(app,config={'CACHE_TYPE':'RedisCache','CACHE_REDDIS_URL':'redis://localhost:6379/0'}) #this is using for cache of the 
#redis used in  cache

CORS(app)

@app.route('/remove-bg', methods=['POST'])# this is backend route to remove bg
def remove_bg():
    try:
        print(f"Request files: {request.files}")
        print(f"Request form data: {request.form}")

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            print(f"Received file: {file.filename}")
            input_image = Image.open(file)

        elif 'url' in request.form:
            url = request.form['url']
            print(f"Received URL: {url}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  
                input_image = Image.open(BytesIO(response.content))
            except requests.exceptions.RequestException as e:
                return jsonify({'error': 'Failed to fetch image from the provided URL', 'details': str(e)}), 400
            except IOError as e:
                return jsonify({'error': 'Invalid image format from the URL', 'details': str(e)}), 400

        else:
            return jsonify({'error': 'No file or URL provided'}), 400
        cache_result=cache.get(cache_key)
        if cache_result:
            return
        output_image = remove(input_image)
        output_stream = io.BytesIO()
        output_image.save(output_stream, format="PNG")
        output_stream.seek(0)
        return send_file(output_stream, mimetype='image/png', as_attachment=True, download_name='result.png')

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
