from config.connection import init_db

def setup_db():
    init_db()
    print("Database initialized successfully!")

if __name__ == "__main__":
    setup_db() 