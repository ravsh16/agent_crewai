# CrewAI Server - Setup & Debugging Guide

## 🐛 Issues Fixed

This server has been debugged and the following issues were resolved:

1. **HuggingFace LLM Compatibility** - Replaced `langchain_huggingface.HuggingFaceEndpoint` with CrewAI's native `LLM` class
2. **Missing Dependencies** - Installed `litellm` and `fastmcp` packages
3. **Version Conflicts** - Resolved openai version conflicts between litellm and crewai
4. **MCP Server Initialization** - Fixed MCPServer import issues

## ⚙️ Configuration Required

### Current Issue: Invalid API Token

The server is running but requires a valid HuggingFace API token. The current token in `.env` is invalid or incomplete.

### Option 1: Use HuggingFace (Current Setup)

1. **Get a HuggingFace API Token:**
   - Go to https://huggingface.co/settings/tokens
   - Create a new token (read access is sufficient)
   - Token format: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

2. **Update `.env` file:**
   ```bash
   HUGGINGFACEHUB_API_TOKEN=hf_your_actual_token_here
   ```

3. **Get a Serper API Key (for web search):**
   - Go to https://serper.dev/
   - Sign up and get an API key
   - Update `.env`:
   ```bash
   SERPER_API_KEY=your_serper_api_key_here
   ```

### Option 2: Use OpenAI Instead

If you prefer to use OpenAI, modify `server.py`:

```python
# Replace the HuggingFace LLM configuration with:
llm = LLM(
    model="openai/gpt-4o-mini",  # or gpt-4, gpt-3.5-turbo
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=512
)
```

Then update `.env`:
```bash
OPENAI_API_KEY=sk-your_openai_key_here
```

### Option 3: Use Ollama (Local, Free)

For a completely local setup without API keys:

1. **Install Ollama:**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Or download from https://ollama.com
   ```

2. **Pull a model:**
   ```bash
   ollama pull llama3.1
   # or
   ollama pull qwen2.5
   ```

3. **Update `server.py`:**
   ```python
   # Replace the HuggingFace LLM configuration with:
   llm = LLM(model="ollama/llama3.1")
   ```

4. **No API keys needed!**

## 🚀 Running the Server

1. **Start the server:**
   ```bash
   cd /Users/ravi/langgraph/CrewAI
   python server.py
   ```

2. **Run tests:**
   ```bash
   # In a new terminal
   python test_server.py
   ```

3. **Use the client:**
   ```bash
   python client.py --query "What is artificial intelligence?"
   ```

## 📋 Test Results

Current status:
- ✅ Server starts successfully
- ✅ Health check passes (http://0.0.0.0:8000/)
- ❌ Predict endpoint fails due to invalid API token

## 🔧 Server Details

- **URL:** http://0.0.0.0:8000
- **Endpoint:** POST http://0.0.0.0:8000/predict
- **Request Format:**
  ```json
  {
    "query": "your question here"
  }
  ```
- **Response Format:**
  ```json
  {
    "output": {
      "raw": "response text here",
      ...
    }
  }
  ```

## 📦 Dependencies Installed

- `litellm` - For LLM provider integration
- `fastmcp` - For MCP server support
- `crewai` - Multi-agent framework
- `litserve` - Server framework

## 🎯 Next Steps

1. Choose your preferred LLM option (HuggingFace, OpenAI, or Ollama)
2. Update the `.env` file with valid API keys OR modify `server.py` to use Ollama
3. Restart the server
4. Run `python test_server.py` to verify everything works
5. Use `python client.py --query "your question"` to interact with the server

## 💡 Recommendation

For the easiest setup without API key hassles, use **Option 3 (Ollama)**. It's completely free, runs locally, and doesn't require any API tokens!
