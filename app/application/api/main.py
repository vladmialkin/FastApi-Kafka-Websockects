from fastapi import FastAPI


def create_app():
    return FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='A simple Kafka + DDD example.',
        debug=True,
    )
