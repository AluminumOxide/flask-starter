Config = {
        "test": {
            "environment":"test",
            "SQLALCHEMY_DATABASE_URI": "sqlite:////tmp/test.db",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        },
        "dev": {
            "environment":"dev",
            "SQLALCHEMY_DATABASE_URI": "sqlite:////tmp/dev.db",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        },
}

