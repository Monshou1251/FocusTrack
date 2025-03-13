import uvicorn
import ssl


if __name__ == "__main__":
    uvicorn.run(
        app = "app.main:app",
        host = "0.0.0.0",
        port=443,
        reload=True,
        ssl_keyfile="./config/key.pem",
        ssl_certfile="./config/cert.pem",
        ssl_version=ssl.PROTOCOL_TLSv1_2
    )


