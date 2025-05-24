def cors_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response

    return middleware
