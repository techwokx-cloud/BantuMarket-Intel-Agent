"""
Bright Data MCP Server Integration
Enables Claude to access live web data autonomously via Bright Data APIs
Track 2: Finance & Market Intelligence
"""

import os
import requests
import json
from typing import Dict, Any, List
from anthropic import Anthropic

class BrightDataMCP:
    """MCP Server wrapper for Bright Data web access"""
    
    def __init__(self):
        self.enabled = os.getenv("BRIGHT_DATA_MCP_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("BRIGHT_DATA_API_KEY")
        self.zone = os.getenv("BRIGHT_DATA_MCP_ZONE", "serp_api1")
        self.customer_id = os.getenv("BRIGHT_DATA_CUSTOMER_ID")
        self.web_unlocker_enabled = os.getenv("BRIGHT_DATA_WEB_UNLOCKER", "true").lower() == "true"
    
    def is_configured(self) -> bool:
        """Check if MCP is properly configured"""
        return self.enabled and bool(self.api_key)
    
    def get_claude_tools(self) -> List[Dict[str, Any]]:
        """Tools available to Claude via MCP Server"""
        if not self.is_configured():
            return []
        
        return [
            {
                "name": "web_search",
                "description": "Search the live web using Bright Data SERP API for real-time data on African commodity markets, pricing, suppliers, regulatory updates, and competitive intelligence",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for market intelligence (e.g., 'Shea butter prices Ghana 2024')"
                        },
                        "market": {
                            "type": "string",
                            "description": "Target market/country (Ghana, Nigeria, Kenya, etc.)"
                        },
                        "data_type": {
                            "type": "string",
                            "enum": ["prices", "suppliers", "tariffs", "regulations", "competitors"],
                            "description": "Type of market data needed"
                        }
                    },
                    "required": ["query", "market"]
                }
            },
            {
                "name": "get_competitor_data",
                "description": "Get real-time competitor pricing and market position data from African markets",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "commodity": {
                            "type": "string",
                            "description": "Commodity name (Shea Butter, Cocoa, Maize, etc.)"
                        },
                        "market": {
                            "type": "string",
                            "description": "Target market/country"
                        },
                        "competitors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of competitor names to track"
                        }
                    },
                    "required": ["commodity", "market"]
                }
            },
            {
                "name": "get_regulatory_updates",
                "description": "Get latest AfCFTA tariff changes and regulatory compliance updates for African trade",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "Country code or name (Ghana, Nigeria, Kenya, etc.)"
                        },
                        "product": {
                            "type": "string",
                            "description": "Product or commodity being checked"
                        },
                        "include_tariffs": {
                            "type": "boolean",
                            "description": "Include tariff schedule information"
                        }
                    },
                    "required": ["country"]
                }
            },
            {
                "name": "get_port_activity",
                "description": "Get real-time port activity, shipping rates, and logistics data for African ports",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "port": {
                            "type": "string",
                            "description": "Port name or city (Lagos, Tema, Mombasa, Abidjan, etc.)"
                        },
                        "data_type": {
                            "type": "string",
                            "enum": ["throughput", "cargo_cost", "wait_time", "shipping_routes"],
                            "description": "Type of port data"
                        }
                    },
                    "required": ["port"]
                }
            },
            {
                "name": "get_currency_rates",
                "description": "Get real-time currency exchange rates for African currencies vs USD",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "currencies": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Currency codes (GHS, NGN, KES, ZAR, XOF, etc.)"
                        }
                    },
                    "required": ["currencies"]
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool via Bright Data APIs"""
        if not self.is_configured():
            return {"error": "MCP Server not configured", "status": "error"}
        
        try:
            if tool_name == "web_search":
                return self._web_search(
                    tool_input.get("query"),
                    tool_input.get("market"),
                    tool_input.get("data_type", "prices")
                )
            elif tool_name == "get_competitor_data":
                return self._get_competitors(
                    tool_input.get("commodity"),
                    tool_input.get("market"),
                    tool_input.get("competitors", [])
                )
            elif tool_name == "get_regulatory_updates":
                return self._get_regulations(
                    tool_input.get("country"),
                    tool_input.get("product"),
                    tool_input.get("include_tariffs", True)
                )
            elif tool_name == "get_port_activity":
                return self._get_port_activity(
                    tool_input.get("port"),
                    tool_input.get("data_type", "throughput")
                )
            elif tool_name == "get_currency_rates":
                return self._get_currency_rates(
                    tool_input.get("currencies", ["GHS", "NGN", "KES"])
                )
            else:
                return {"error": f"Unknown tool: {tool_name}", "status": "error"}
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": tool_name
            }
    
    def _web_search(self, query: str, market: str, data_type: str = "prices") -> Dict[str, Any]:
        """Execute web search via Bright Data SERP API"""
        try:
            # Build search URL
            search_query = f"{query} {market}"
            
            # Add data type specificity
            if data_type == "tariffs":
                search_query += " tariff AfCFTA"
            elif data_type == "suppliers":
                search_query += " suppliers exporters"
            elif data_type == "regulations":
                search_query += " regulations compliance"
            elif data_type == "competitors":
                search_query += " competitors market share"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "zone": self.zone,
                "url": f"https://www.google.com/search?q={search_query.replace(' ', '+')}",
                "format": "raw",
                "proxy_zone": "residential",
                "browser": "true" if self.web_unlocker_enabled else "false",
                "handle_bot_detection": self.web_unlocker_enabled
            }
            
            response = requests.post(
                "https://api.brightdata.com/request",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.json() if response.headers.get('content-type') == 'application/json' else response.text[:1000],
                    "query": search_query,
                    "market": market,
                    "data_type": data_type,
                    "web_unlocker_used": self.web_unlocker_enabled
                }
            else:
                return {
                    "status": "error",
                    "error": f"API returned {response.status_code}",
                    "query": search_query
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": "web_search"
            }
    
    def _get_competitors(self, commodity: str, market: str, competitors: List[str]) -> Dict[str, Any]:
        """Get competitor data via web search"""
        try:
            competitor_queries = [
                f"{competitor} {commodity} prices {market}" 
                for competitor in competitors
            ]
            
            results = []
            for query in competitor_queries[:3]:  # Limit to 3 searches
                result = self._web_search(query, market, "competitors")
                results.append(result)
            
            return {
                "status": "success",
                "commodity": commodity,
                "market": market,
                "competitor_data": results,
                "competitors_analyzed": len(competitor_queries)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": "get_competitor_data"
            }
    
    def _get_regulations(self, country: str, product: str = None, include_tariffs: bool = True) -> Dict[str, Any]:
        """Get regulatory and tariff information"""
        try:
            search_queries = [
                f"AfCFTA tariff {country} {product or ''}"
            ]
            
            if include_tariffs:
                search_queries.append(f"{country} tariff schedule 2024")
            
            search_queries.append(f"{country} trade regulations export compliance")
            
            results = []
            for query in search_queries:
                result = self._web_search(query, country, "regulations")
                results.append(result)
            
            return {
                "status": "success",
                "country": country,
                "product": product,
                "regulatory_data": results,
                "queries_executed": len(search_queries)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": "get_regulatory_updates"
            }
    
    def _get_port_activity(self, port: str, data_type: str) -> Dict[str, Any]:
        """Get port activity and shipping information"""
        try:
            search_queries = {
                "throughput": f"{port} port throughput cargo volume {data_type}",
                "cargo_cost": f"{port} shipping rates cargo cost",
                "wait_time": f"{port} port waiting time congestion",
                "shipping_routes": f"{port} shipping routes trade lanes"
            }
            
            query = search_queries.get(data_type, search_queries["throughput"])
            result = self._web_search(query, port, "prices")
            
            return {
                "status": "success",
                "port": port,
                "data_type": data_type,
                "port_data": result
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": "get_port_activity"
            }
    
    def _get_currency_rates(self, currencies: List[str]) -> Dict[str, Any]:
        """Get currency exchange rates"""
        try:
            rates = {}
            
            for currency in currencies:
                query = f"{currency} USD exchange rate today"
                result = self._web_search(query, "Africa", "prices")
                rates[currency] = result
            
            return {
                "status": "success",
                "currencies": currencies,
                "exchange_rates": rates
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool": "get_currency_rates"
            }


def create_autonomous_agent():
    """Create Claude agent with MCP Server access for autonomous market research"""
    
    mcp = BrightDataMCP()
    
    if not mcp.is_configured():
        return None
    
    client = Anthropic()
    
    def run_agent(user_query: str) -> str:
        """Run autonomous market research agent
        
        Claude will autonomously:
        1. Parse the market question
        2. Decide which tools to use
        3. Execute searches via Bright Data
        4. Synthesize findings
        5. Provide recommendations
        """
        
        messages = [
            {
                "role": "user",
                "content": f"""You are an autonomous market research agent for African commodity trading.
                
Your task: {user_query}

You have access to live web data via Bright Data. Use these tools to:
1. Search for current market prices and trends
2. Monitor competitor activity
3. Check regulatory updates and tariffs
4. Analyze port activity and logistics
5. Track currency movements

Be thorough, cite sources, and provide actionable insights."""
            }
        ]
        
        tools = mcp.get_claude_tools()
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            response = client.messages.create(
                model="claude-opus-4-20250805",
                max_tokens=4096,
                tools=tools,
                messages=messages
            )
            
            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                tool_use = next(
                    (block for block in response.content if block.type == "tool_use"),
                    None
                )
                
                if tool_use:
                    # Execute the tool
                    result = mcp.execute_tool(tool_use.name, tool_use.input)
                    
                    # Add Claude's response and tool result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": json.dumps(result, default=str)
                            }
                        ]
                    })
                else:
                    break
            else:
                # Claude finished reasoning
                break
        
        # Extract final response
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text
        
        return final_text if final_text else "Agent completed analysis but provided no text response."
    
    return run_agent


# Utility function for Streamlit integration
def is_mcp_available() -> bool:
    """Check if MCP Server is available and configured"""
    mcp = BrightDataMCP()
    return mcp.is_configured()
