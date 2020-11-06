from app import create_app
import app.settings.cf as cf

import warnings
warnings.filterwarnings("ignore", message="Numerical issues were encountered ")

app = create_app('prod')

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host=cf.host, port=cf.port)
