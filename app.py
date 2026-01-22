from flask import Flask

bookpc = Flask(__name__)
bookpc.secret_key = "your_secret_key"  # change this

# import routes AFTER app is created
import login
import dashboard
import booking


login.register(bookpc)
dashboard.register(bookpc)
booking.register(bookpc)

if __name__ == "__main__":
    bookpc.run(host="0.0.0.0", port=4000, debug=True)
