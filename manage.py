from app import create_app
import app.settings.cf as cf

app = create_app('dev')

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host=cf.host, port=cf.port)
