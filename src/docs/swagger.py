template = {
    "swagger": "2.0",
    "info": {
        "title": "antriin.id API",
        "description": "API for antriin.id project",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "BasicAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Basic auth, using username & password. Example: \"Authorization: {username} & {password}\""
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}