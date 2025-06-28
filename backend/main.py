import uvicorn

# import ssl


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="localhost",
        port=8000,
        reload=True,
        # TODO: add valid SSL certificates
        # ssl_keyfile="./config/key.pem",
        # ssl_certfile="./config/cert.pem",
        # ssl_version=ssl.PROTOCOL_TLSv1_2
    )
