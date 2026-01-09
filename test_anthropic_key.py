#!/usr/bin/env python3
"""
Test Anthropic API Key directly without CrewAI
This script tests if the API key is valid and what models are accessible
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

def test_anthropic_key():
    """Test Anthropic API key and list available models"""
    
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY not found in environment variables")
        return False
    
    print("="*60)
    print("Testing Anthropic API Key")
    print("="*60)
    print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
    # Initialize Anthropic client
    try:
        client = Anthropic(api_key=api_key)
        print("✅ Anthropic client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Anthropic client: {e}")
        return False
    
    # Test with different Claude models (from newest to oldest)
    models_to_test = [
        # Potential Claude 4.x models (future/testing)
        "claude-sonnet-4-5-20250929",
        "claude-4-opus",
        "claude-4-sonnet",
        
        # Claude 3.5 Sonnet versions (latest confirmed)
        "claude-3-5-sonnet-20241022",  # Latest Claude 3.5 Sonnet (Oct 2024)
        "claude-3-5-sonnet-20240620",  # Claude 3.5 Sonnet (June 2024)
        "claude-3-5-sonnet-latest",    # Latest alias
        
        # Claude 3 Opus
        "claude-3-opus-20240229",      # Claude 3 Opus (Feb 2024)
        
        # Claude 3 Sonnet
        "claude-3-sonnet-20240229",    # Claude 3 Sonnet (Feb 2024)
        
        # Claude 3 Haiku (fastest, most affordable)
        "claude-3-haiku-20240307",     # Claude 3 Haiku (Mar 2024)
    ]
    
    print("\n" + "="*60)
    print("Testing Claude Models")
    print("="*60)
    
    successful_model = None
    
    for model in models_to_test:
        print(f"\n🔍 Testing model: {model}")
        try:
            # Try a simple message
            message = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Hi"}
                ]
            )
            print(f"  ✅ SUCCESS! Model '{model}' is accessible")
            print(f"  📝 Response: {message.content[0].text}")
            successful_model = model
            break  # Stop after first successful model
        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "not_found" in error_str:
                print(f"  ❌ Model not found (404)")
            elif "401" in error_str or "authentication" in error_str.lower():
                print(f"  ❌ Authentication error - Invalid API key")
                return False
            elif "403" in error_str or "permission" in error_str.lower():
                print(f"  ❌ Permission denied - API key doesn't have access to this model")
            else:
                print(f"  ❌ Error: {error_str}")
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    if successful_model:
        print(f"\n✅ SUCCESS! Working model found: {successful_model}")
        print(f"\n💡 Update your server.py to use:")
        print(f'   model="anthropic/{successful_model}"')
        return True
    else:
        print("\n❌ FAILURE: No accessible Claude models found")
        print("\n🔍 Possible issues:")
        print("   1. API key may be invalid or expired")
        print("   2. API key may not have access to any Claude models")
        print("   3. Account may need to add payment method")
        print("   4. API tier may not include these models")
        print("\n💡 Visit https://console.anthropic.com/ to check your account")
        return False

if __name__ == "__main__":
    try:
        success = test_anthropic_key()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
