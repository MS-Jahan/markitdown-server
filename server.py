import io
import os
import logging
from flask import Flask, request, abort, make_response
from werkzeug.exceptions import RequestEntityTooLarge
from markitdown import MarkItDown

# Configure logging level from environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Flask web application
app = Flask(__name__)

# Configuration from environment variables
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE_MB', '50')) * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Request timeout (for reference - actual timeout is set in gunicorn)
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT_SECONDS', '120'))

# Enable/disable MarkItDown plugins
ENABLE_PLUGINS = os.getenv('ENABLE_MARKITDOWN_PLUGINS', 'false').lower() in ('true', '1', 'yes')

# Optional: LLM configuration for image descriptions
LLM_MODEL = os.getenv('LLM_MODEL', None)  # e.g., "gpt-4o"
LLM_API_KEY = os.getenv('LLM_API_KEY', None)

# Initialize MarkItDown once (singleton pattern for performance)
# This instance is reused across requests to avoid initialization overhead
markitdown_kwargs = {'enable_plugins': ENABLE_PLUGINS}

# If LLM is configured, add it to MarkItDown initialization
if LLM_MODEL and LLM_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=LLM_API_KEY)
        markitdown_kwargs['llm_client'] = client
        markitdown_kwargs['llm_model'] = LLM_MODEL
        logger.info(f"LLM image descriptions enabled with model: {LLM_MODEL}")
    except ImportError:
        logger.warning("OpenAI library not installed. LLM features disabled.")
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {e}")

markitdown = MarkItDown(**markitdown_kwargs)

logger.info(f"Server configuration: MAX_FILE_SIZE={MAX_FILE_SIZE // 1024 // 1024}MB, "
            f"REQUEST_TIMEOUT={REQUEST_TIMEOUT}s, ENABLE_PLUGINS={ENABLE_PLUGINS}")

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle files that exceed the size limit."""
    return f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024} MB.", 413

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring systems."""
    return "Markitdown server is running.", 200

@app.route('/health', methods=['GET'])
def readiness_check():
    """
    Readiness probe for Kubernetes/container orchestrators.
    Verifies that the service is ready to handle requests.
    """
    try:
        # Quick sanity check - ensure MarkItDown instance is available
        if markitdown is None:
            return "Service not ready", 503
        return {"status": "ready", "service": "markitdown-server"}, 200
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {"status": "not ready", "error": str(e)}, 503

@app.route('/convert', methods=['POST'])
def convert_file():
    """
    Accepts a file upload and converts it to Markdown using the markitdown library.

    This implementation uses stream-based processing to minimize memory usage
    and avoid creating temporary files on disk.
    """
    # Verify that a file was included in the request
    if 'file' not in request.files:
        abort(400, 'No file part was found in the request.')

    uploaded_file = request.files['file']

    # Verify that a file was selected
    if uploaded_file.filename == '':
        abort(400, 'No file was selected for uploading.')

    # Validate filename is provided
    if not uploaded_file.filename:
        abort(400, 'Invalid filename.')

    logger.info(f"Processing file: {uploaded_file.filename}")

    try:
        # Use convert_stream with the file-like object directly
        # This avoids writing to disk and reduces memory overhead
        # The stream must be a binary file-like object
        file_stream = io.BytesIO(uploaded_file.read())

        # Set a filename hint for better format detection
        # markitdown uses the file extension to determine the converter
        result = markitdown.convert_stream(
            file_stream,
            file_extension=uploaded_file.filename.rsplit('.', 1)[-1] if '.' in uploaded_file.filename else None
        )

        # Extract the markdown content from the result
        markdown_content = result.text_content

        # Create response with appropriate headers
        response = make_response(markdown_content, 200)
        response.headers['Content-Type'] = 'text/markdown; charset=utf-8'

        # Add cache control headers to prevent caching of dynamic content
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        logger.info(f"Successfully converted file: {uploaded_file.filename}")
        return response

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Conversion failed for {uploaded_file.filename}: {str(e)}", exc_info=True)

        # Return a user-friendly error message
        error_message = f"Failed to convert file: {str(e)}"
        abort(500, error_message)

if __name__ == "__main__":
    # This block is only used for local development
    # In production, use Gunicorn (see Dockerfile CMD)
    logger.warning("Running Flask development server. Use Gunicorn for production!")
    app.run(host='0.0.0.0', port=8080, debug=False)
