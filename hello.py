from functions_config import (
    model_config_none,
    model_config_auto,
    model_config_any,
    model_config_advanced_auto,
)

from functions_mathbot import (
    calculate_area_rectangle,
    calculate_area_square,
    calculate_area_triangle,
)

tools = [calculate_area_triangle, calculate_area_rectangle, calculate_area_square]

system_prompt = """
You are a helpful engineer. You can calculate the area of square, triangle and rectangle. 
Do not perform any other tasks."""

# model_config_none(prompt="what can you do?", system_instructions=system_prompt, all_functions=tools)

model_config_advanced_auto(
    prompt="print area of triangle, its base is 2m and height is 4m ",
    system_instructions=system_prompt,
    available_functions=tools,
    all_functions=tools,
)
