from minicode.tools.schema import build_schema
from minicode.tools.registry import register_tool


def tool(func):

    tool_def = build_schema(func)

    register_tool(
        name=tool_def["name"],
        description=tool_def["description"],
        schema=tool_def["parameters"],
        func=func,
    )

    return func
