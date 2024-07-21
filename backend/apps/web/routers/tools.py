from fastapi import Depends, FastAPI, HTTPException, status, Request
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import json

from apps.web.models.tools import Tools, ToolForm, ToolModel, ToolResponse
from apps.web.utils import load_toolkit_module_by_id

from utils.tools import get_tools_specs
from constants import ERROR_MESSAGES

from importlib import util
import os

from config import DATA_DIR


TOOLS_DIR = f"{DATA_DIR}/tools"
os.makedirs(TOOLS_DIR, exist_ok=True)


router = APIRouter()

############################
# GetToolkits
############################


@router.get("/", response_model=List[ToolResponse])
async def get_toolkits():
    toolkits = [toolkit for toolkit in Tools.get_tools()]
    return toolkits


############################
# ExportToolKits
############################


@router.get("/export", response_model=List[ToolModel])
async def get_toolkits():
    toolkits = [toolkit for toolkit in Tools.get_tools()]
    return toolkits


############################
# CreateNewToolKit
############################


@router.post("/create", response_model=Optional[ToolResponse])
async def create_new_toolkit(
    request: Request, form_data: ToolForm
):
    if not form_data.id.isidentifier():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only alphanumeric characters and underscores are allowed in the id",
        )

    form_data.id = form_data.id.lower()

    toolkit = Tools.get_tool_by_id(form_data.id)
    if toolkit == None:
        toolkit_path = os.path.join(TOOLS_DIR, f"{form_data.id}.py")
        try:
            with open(toolkit_path, "w") as tool_file:
                tool_file.write(form_data.content)

            toolkit_module = load_toolkit_module_by_id(form_data.id)

            TOOLS = request.app.state.TOOLS
            TOOLS[form_data.id] = toolkit_module

            specs = get_tools_specs(TOOLS[form_data.id])
            toolkit = Tools.insert_new_tool(form_data, specs)

            if toolkit:
                return toolkit
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ERROR_MESSAGES.FILE_EXISTS,
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT(e),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.ID_TAKEN,
        )


############################
# GetToolkitById
############################


@router.get("/id/{id}", response_model=Optional[ToolModel])
async def get_toolkit_by_id(id: str):
    toolkit = Tools.get_tool_by_id(id)

    if toolkit:
        return toolkit
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateToolkitById
############################


@router.post("/id/{id}/update", response_model=Optional[ToolModel])
async def update_toolkit_by_id(
    request: Request, id: str, form_data: ToolForm
):
    toolkit_path = os.path.join(TOOLS_DIR, f"{id}.py")

    try:
        with open(toolkit_path, "w") as tool_file:
            tool_file.write(form_data.content)

        toolkit_module = load_toolkit_module_by_id(id)

        TOOLS = request.app.state.TOOLS
        TOOLS[id] = toolkit_module

        specs = get_tools_specs(TOOLS[id])

        updated = {
            **form_data.model_dump(exclude={"id"}),
            "specs": specs,
        }

        print(updated)
        toolkit = Tools.update_tool_by_id(id, updated)

        if toolkit:
            return toolkit
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error updating toolkit"),
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


############################
# DeleteToolkitById
############################


@router.delete("/id/{id}/delete", response_model=bool)
async def delete_toolkit_by_id(request: Request, id: str):
    result = Tools.delete_tool_by_id(id)

    if result:
        TOOLS = request.app.state.TOOLS
        del TOOLS[id]

    return result
