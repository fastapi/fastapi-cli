from fastapi import FastAPI

no_openapi = FastAPI(openapi_url=None)


@no_openapi.get("/")
def no_openapi_root():
    return {"message": "single file no_openapi"}


none_docs = FastAPI(docs_url=None, redoc_url=None)


@none_docs.get("/")
def none_docs_root():
    return {"message": "single file none_docs"}


no_docs = FastAPI(docs_url=None)


@no_docs.get("/")
def no_docs_root():
    return {"message": "single file no_docs"}


no_redoc = FastAPI(redoc_url=None)


@no_redoc.get("/")
def no_redoc_root():
    return {"message": "single file no_redoc"}


full_docs = FastAPI()


@full_docs.get("/")
def full_docs_root():
    return {"message": "single file full_docs"}


custom_docs = FastAPI(docs_url="/custom-docs-url", redoc_url="/custom-redoc-url")


@custom_docs.get("/")
def custom_docs_root():
    return {"message": "single file custom_docs"}
