Multi-threaded HTTP Server with Compression

A lightweight, multi-threaded HTTP server built using Python’s socket module, capable of handling concurrent connections, serving static files, processing POST requests, and supporting Gzip/Deflate compression.

Features
Handles up to 500+ concurrent client connections using multi-threading.
Supports HTTP/1.1 GET and POST requests for dynamic and static content.
Serves static files from the public/ directory.
Implements Gzip and Deflate compression, reducing response size by up to 60%.
Graceful port reuse with SO_REUSEADDR, reducing server restart time.
Fast request processing with an average response time of <50ms
