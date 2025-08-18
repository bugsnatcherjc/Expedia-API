from app.middleware.session import SessionMiddleware

# Add this to your main.py
app.add_middleware(SessionMiddleware)
