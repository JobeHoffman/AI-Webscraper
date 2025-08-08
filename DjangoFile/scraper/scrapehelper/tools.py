from langchain.tools import Tool
from dotenv import load_dotenv
from langchain_community.tools import BraveSearch
from langchain_openai import ChatOpenAI
import requests
from bs4 import BeautifulSoup

load_dotenv()

# def get_engagement_metrics(scraped_content: str):
#     pass
    
# def extract_perspectives(scraped_content: str):
#     pass

def websearch(research_question: str):
    bSearch = BraveSearch.from_search_kwargs(search_kwargs={"count": 3})
    bSearch_response = bSearch.invoke(research_question) # websearch query
    print(f"{type(bSearch_response)} is the type")
    links = []
    headers = "header"
    for entry in bSearch_response.split(','):
        if "link" in entry:
            link = entry[entry.find(":")+3:-1]
            links.append(link)

    textContent = []
    print(f"LINKS: {links}")
    for link in links:
        try:
            response = requests.get(link).content
            soup = BeautifulSoup(response, 'lxml')
            textContent.append(soup.get_text())
        except Exception as e:
            print(f"an error has occured: {e}")

    parsedContent = ""
    i = 0
    for t in textContent:
        parsedContent += f"excerpt {i}:\n{t}"
        parsedContent += "\n\n"
        i+=1

    llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14")
    messages = [
        (
            "system",
            f"""
            you are a research assistant and your research question is: {research_question}.
            You are a 1-response API. 
            Your output must strictly be provided in plain text, no markup format.
            """
        ),
        (
            "human", 
            f"""
            refer to these various excerpts and provide a thoughtful rhetorical analysis of 
            regarding this research question: {research_question} 
            make sure to consider various perspectives within: {parsedContent}. 
            """
        )
    ]

    result = llm.invoke(messages)
    return result.content

################################################################################
#TOOL DECLARATION
################################################################################

# get_engagement_metrics = Tool(
#     name = 'get_engagement_metrics',
#     func = get_engagement_metrics,
#     description = 'this tool is used to extract engagement metrics such as number of likes, comments etc.'
# )

# extract_perspectives = Tool(
#     name = "extract_perspectives",
#     func = extract_perspectives,
#     description= "this tool is used to obtain detailed perspectives/viewpoints that are helpful for rhetorical analysis"
# )

websearch = Tool(
    name = "websearcher",
    func = websearch,
    description= """
    this tool is used to search the web for content related to the user's research question
    this is useful for complex multilayer rhetorical analysis
    """
)
