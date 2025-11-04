from app import create_app
import os

# Get configuration from environment variable or use default
config_name = os.getenv('FLASK_ENV', 'development')
config_class = f'config.{config_name.capitalize()}Config'

app = create_app(config_class)

if __name__ == '__main__':
    # Use config values for host and port
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])