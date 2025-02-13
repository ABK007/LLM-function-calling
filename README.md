# Model Function Calling / Tool Calling

The purpose of this repo is to understand how function calling/tool calling works
using google gemini models.

Below is a brief overview of each function and an explanation of how its code works:

---

### Tool & Model Setup Functions

- **`tool_config_from_mode(mode: str, fns: Iterable[str] = ())`**

  - **Purpose:** Creates a configuration dictionary (a “tool config”) that tells the Gemini model which function‐calling mode to use (e.g., `"none"`, `"auto"`, or `"any"`) and which functions (by name) are allowed.
  - **How It Works:**  
    It builds a dictionary with a `"function_calling_config"` key containing the `mode` and the list of allowed function names (`fns`). This dictionary is then converted to the proper format using `content_types.to_tool_config`.

- **`model_setup(model_name: str, tools: list, instructions: str)`**
  - **Purpose:** Initializes the Gemini model with a specific model name, a list of tool functions, and system instructions.
  - **How It Works:**  
    It first loads environment variables (to read the API key) using `load_dotenv()` and configures the API key. Then, it creates an instance of `genai.GenerativeModel` with the provided model name, tools, and system instructions, and returns this model object.

---

### Light Control Functions (Simulation)

- **`enable_lights()`**

  - **Purpose:** Simulates enabling a lighting system.
  - **How It Works:**  
    It prints the message `"LIGHTBOT: Lights enabled."`.

- **`set_light_color(rgb_hex: str)`**

  - **Purpose:** Simulates setting the color of lights.
  - **How It Works:**  
    It prints a message with the provided hex color value (e.g., `"LIGHTBOT: Lights set to #FF5733."`).

- **`stop_lights()`**
  - **Purpose:** Simulates stopping or turning off the lights.
  - **How It Works:**  
    It prints the message `"LIGHTBOT: Lights turned off."`.

---

### Area Calculation Functions

- **`calculate_area_square(side: int) -> int`**

  - **Purpose:** Calculates the area of a square given one side’s length.
  - **How It Works:**  
    It prints a message indicating that it is calculating the area, computes the area as `side * side`, and then prints the resulting area. (Note: Although annotated to return an integer, it only prints the result.)

- **`calculate_area_rectangle(length: int, width: int) -> int`**

  - **Purpose:** Calculates the area of a rectangle given its length and width.
  - **How It Works:**  
    It prints a message stating it is calculating the area, computes the area using `length * width`, and prints the result.

- **`calculate_area_triangle(base: int, height: int)`**
  - **Purpose:** Calculates the area of a triangle using its base and height.
  - **How It Works:**  
    It prints a message about the calculation, computes the area using `(base * height) / 2`, and prints the calculated area.

---

### Model Configuration Functions

These functions demonstrate different ways to interact with the Gemini model based on the function‐calling mode.

- **`model_config_none(prompt: str, system_instructions: str, all_functions: list[Callable[..., Any]])`**

  - **Purpose:** Sets up the model in `"none"` mode, meaning the model will not trigger any function calls—it responds only with text.
  - **How It Works:**  
    It creates a tool config with mode `"none"`, initializes the model using `model_setup`, starts a chat session, sends the prompt along with the tool configuration, and prints the text response.

- **`model_config_auto(prompt: str, system_instructions: str, all_functions: list[Callable[..., Any]])`**

  - **Purpose:** Uses the `"auto"` mode where the model decides whether to call a function or simply reply in text.
  - **How It Works:**  
    Similar to the previous function, it sets the tool configuration (this time with mode `"auto"`), sets up the model, starts a chat, sends the prompt, and then prints the first part of the response (which might be either text or a function call message).

- **`model_config_any(prompt: str, system_instructions: str, all_functions: list[Callable[..., Any]], available_functions: list[Callable[..., Any]])`**

  - **Purpose:** Configures the model with `"any"` mode where the model is forced to return a function call based on the provided available functions.
  - **How It Works:**  
    It creates a tool configuration with mode `"any"` (passing the list of allowed function names), sets up the model with all functions, starts a chat session, sends the prompt, and prints the first part of the response (which is expected to be a function call message).

- **`model_config_advanced_auto(prompt: str, system_instructions: str, all_functions: list[Callable[..., Any]], available_functions: list[Callable[..., Any]])`**
  - **Purpose:** Demonstrates advanced automatic function calling, where the model proactively uses functions based on context.
  - **How It Works:**  
    It creates the tool configuration (again with `"any"` mode and allowed function names), sets up the model with the option `enable_automatic_function_calling=True`, starts a chat session, and sends the prompt. In this mode, the model is allowed to execute functions automatically if needed.

---

### Usage Summary

At the end of the code, the script:

1. Imports the necessary functions.
2. Defines a list of tool functions (area calculations).
3. Sets up a system prompt instructing the model to only perform area calculations.
4. Calls one of the configuration functions (e.g., `model_config_any`) with a prompt asking to calculate the area of a triangle with a base of 2 and a height of 4.

Each configuration function uses the tool configuration and model setup to start a conversation with Gemini, with different behavior based on the function calling mode.

---

## Functions Response:

What you’re seeing is the model’s function call response—not an error in your code. Let’s break it down:

1. ### **Function Call Response:**

   **The output**

   ```
   function_call {
     name: "calculate_area_triangle"
     args {
       fields {
         key: "height"
         value {
           number_value: 4
         }
       }
       fields {
         key: "base"
         value {
           number_value: 2
         }
       }
     }
   }
   ```

   indicates that the Gemini model determined that it should call the `calculate_area_triangle` function with the arguments `base=2` and `height=4`. This is the expected behavior when using a function-calling mode (in your case, mode `"any"`)—the model returns a proto message that describes the function call rather than executing it immediately.

2. **gRPC Timeout Warning:**  
   The message:
   ```
   WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
   E0000 ... grpc_wait_for_shutdown_with_timeout() timed out.
   ```
   is coming from the underlying gRPC library used by the Gemini API client. This warning typically indicates that the gRPC channel did not shut down as gracefully as expected. In many cases, this is a known artifact or a benign warning that doesn’t affect the core functionality of your application.

- **If You Expect Automatic Function Execution:**  
  The current `"any"` mode only guarantees that the model will _return_ a function call message. If you want the function to be automatically executed, consider using the **advanced auto mode**. For example:

  ```python
  model_config_advanced_auto(
      prompt="print area of triangle, its base is 2m and height is 4m",
      system_instructions=system_prompt,
      all_functions=tools,
      available_functions=tools,
  )
  ```

**Response**

```Calculating the area of triangle
Area of the triangle: 4.0
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1739457560.337145    9808 init.cc:232] grpc_wait_for_shutdown_with_timeout() timed out.
```

Notice that in `model_config_advanced_auto`, the chat is started with `enable_automatic_function_calling=True`. This setting should trigger the actual execution of the function (i.e., calling `calculate_area_triangle`) based on the returned function call.

- **If You Intend to Handle the Function Call Manually:**  
  You can parse the returned function call message, extract the function name and arguments, and then manually call the corresponding function in your code. This gives you complete control over the execution flow.

- **About the gRPC Warning:**  
  In many cases, this warning can be safely ignored. However, if it becomes problematic (for instance, if it leads to hanging or crashes in a production system), you might want to review the gRPC logging settings or check for any updates/patches in the Gemini client libraries.

---

### Summary

- **Output Explanation:** The output is a proto message indicating the model’s intent to call `calculate_area_triangle` with `base=2` and `height=4`.
- **gRPC Warning:** The gRPC timeout warning is a known issue and often harmless.
- **Next Steps:**
  - Use `advanced_auto` mode if you want the function to execute automatically.
  - Or, handle the function call response manually in your application.

This should help you understand the behavior and decide how to proceed with your implementation!
