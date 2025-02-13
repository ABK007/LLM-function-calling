from google.generativeai.types import content_types
from collections.abc import Iterable
import google.generativeai as genai
from dotenv import load_dotenv
import os




def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )


def model_setup(model_name: str, tools: list, instructions: str):
    """basic llm model object configuration"""
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        model_name, tools=tools, system_instruction=instructions
    )

    return model


def enable_lights():
    """Turn on the lighting system."""
    print("LIGHTBOT: Lights enabled.")


def set_light_color(rgb_hex: str):
    """Set the light color. Lights must be enabled for this to work."""
    print(f"LIGHTBOT: Lights set to {rgb_hex}.")


def stop_lights():
    """Stop flashing lights."""
    print("LIGHTBOT: Lights turned off.")


def model_config_none(prompt: str):
    """Model Function calling when the function_calling_mode is `None`. 
    The model will only respond in text """

    tool_config = tool_config_from_mode("none")
    model = model_setup(
        "gemini-2.0-flash",
        tools=[enable_lights, set_light_color, stop_lights],
        instructions="""You are a helpful lighting system bot. 
                        You can turn lights on and off, and you can set the color. 
                        Do not perform any other tasks.""",
    )

    chat = model.start_chat()
    response = chat.send_message(
        prompt, tool_config=tool_config
    )

    print(response.text)
    

def model_config_auto(prompt: str):
    """Model Function calling when the function_calling_mode is `Auto`. The model will decide
    whether to respond by calling function or text only"""
    
    model = model_setup(
        "gemini-2.0-flash",
        tools=[enable_lights, set_light_color, stop_lights],
        instructions="""You are a helpful lighting system bot. 
                        You can turn lights on and off, and you can set the color. 
                        Do not perform any other tasks.""",
    )

    chat = model.start_chat()

    tool_config = tool_config_from_mode("auto")

    response = chat.send_message(prompt, tool_config=tool_config)
    print(response.parts[0])


def model_config_any(prompt:str):
    """Model Function calling when the function_calling_mode is `any`. 
    The model will always respond by calling functions from given list. """
    
    available_fns = ["set_light_color", "stop_lights"]

    
    model = model_setup(
        "gemini-2.0-flash",
        tools=[enable_lights, set_light_color, stop_lights],
        instructions="""You are a helpful lighting system bot. 
                        You can turn lights on and off, and you can set the color. 
                        Do not perform any other tasks.""",
    )

    chat = model.start_chat()

    tool_config = tool_config_from_mode("any", available_fns)

    response = chat.send_message(prompt, tool_config=tool_config)
    print(response.parts[0])
    

def model_config_advanced_auto(prompt:str):
    """Model Function calling when the function_calling_mode is `any`. 
    The model can proactively utilize functions based on 
    the context of the conversation. """
    
    available_fns = ["enable_lights"]
    tool_config = tool_config_from_mode("any", available_fns)
    
    model = model_setup(
        "gemini-2.0-flash",
        tools=[enable_lights, set_light_color, stop_lights],
        instructions="""You are a helpful lighting system bot. 
                        You can turn lights on and off, and you can set the color. 
                        Do not perform any other tasks.""",
    )

    auto_chat = model.start_chat(enable_automatic_function_calling=True)
    auto_chat.send_message(prompt, tool_config=tool_config)
    
    