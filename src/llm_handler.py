from langchain_experimental.llms.ollama_functions import OllamaFunctions
from src.tools import get_stock_price, get_company_info, calculate_moving_average

class LLMHandler:
    def __init__(self, debug_log):
        self.debug_log = debug_log
        self.model = OllamaFunctions(model="llama3.1:latest", format="json")
        self.tools = {
            "get_stock_price": get_stock_price,
            "get_company_info": get_company_info,
            "calculate_moving_average": calculate_moving_average,
        }
        self.debug_log.write("[DEBUG] LLMHandler initialized with tools")

    def process_query(self, query):
        self.debug_log.write(f"[DEBUG] Processing query: {query}")
        response = self.model.invoke(query)

        if 'function_call' in response.additional_kwargs:
            function_name = response.additional_kwargs['function_call']['name']
            arguments = response.additional_kwargs['function_call']['arguments']
            self.debug_log.write(f"[DEBUG] Invoking function: {function_name}")

            tool = self.tools.get(function_name)
            if tool:
                return tool(**arguments)
            else:
                return f"Tool {function_name} not available."
        return "Query could not be processed. Please try again."
