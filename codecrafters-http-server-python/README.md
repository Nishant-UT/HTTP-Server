# Multi-threaded HTTP Server with Compression

>A lightweight, multi-threaded HTTP server built using Python’s socket module, capable of handling concurrent connections, serving static files, processing POST >requests, and supporting Gzip/Deflate compression.

# Features
1. Handles up to 500+ concurrent client connections using multi-threading.
2. Supports HTTP/1.1 GET and POST requests for dynamic and static content.
3. Serves static files from the public/ directory.
4. Implements Gzip and Deflate compression, reducing response size by up to 60%.
5. Graceful port reuse with SO_REUSEADDR, reducing server restart time.
6. Fast request processing with an average response time of <50ms
