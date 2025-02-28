from langchain_community.tools import TavilySearchResults
import os

os.environ["TAVILY_API_KEY"] = "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"
tool = TavilySearchResults(
    max_results=10,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

print(tool.invoke({"query": "Try to search for the tution fees of the faculty of computer and information science in Ain Shams University which is located in Cairo,Egypt for egyptains students."}))

