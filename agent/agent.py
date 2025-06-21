"""Example: Agno Agent with Finance tools

This example shows how to create an Agno Agent with tools (YFinanceTools) and expose it in an AG-UI compatible way.
"""

from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from fastapi.middleware.cors import CORSMiddleware
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv
import os
load_dotenv()

agent = Agent(
  model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
  tools=[
    YFinanceTools(
      stock_price=True, analyst_recommendations=True, stock_fundamentals=True
    ), 
    DuckDuckGoTools()
  ],
  show_tool_calls=True,
  description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
  instructions="Format your response using markdown and use tables to display data where possible.",
)

agui_app = AGUIApp(
  agent=agent,
  name="Investment Analyst",
  app_id="investment_analyst",
  description="An investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
)

app = agui_app.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
  agui_app.serve(app="agent:app", port=8000, reload=True)
