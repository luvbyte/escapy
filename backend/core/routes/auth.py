from fastapi import APIRouter, Depends, HTTPException, Request, Body

from core.utils import ESException, get_escapy

from pydantic import BaseModel


# Router /module
router = APIRouter(tags=["Auth"])





