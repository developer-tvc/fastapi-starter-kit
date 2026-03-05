"""FastAPI application entry-point."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Starter Kit",
    description="A simple FastAPI starter project.",
    version="0.1.0",
)


@app.get("/", tags=["Health"])
def root():
    """Health-check / welcome endpoint."""
    return {"message": "FastAPI Starter Kit"}
