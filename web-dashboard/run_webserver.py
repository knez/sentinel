from waitress import serve
import dashboard

# bind on all interfaces
host = '0.0.0.0'
# change to 80 for production use
port = 8080

print(f'Serving on http://{host}:{port}')
serve(dashboard.create_app(), host=host, port=port)
