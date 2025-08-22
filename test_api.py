#!/usr/bin/env python3
"""
Simple test script for ResearchRAG API
"""

import requests
import json

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_upload_url():
    """Test uploading a paper via URL."""
    try:
        # Test with a simple arXiv paper
        url = "https://arxiv.org/abs/2301.00001"
        
        data = {"url": url}
        response = requests.post("http://localhost:8000/upload-paper", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful: {result}")
            return result.get("paper_id")
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return None

def test_summary(paper_id):
    """Test getting paper summary."""
    try:
        response = requests.get(f"http://localhost:8000/summary/{paper_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Summary retrieved: {result['title']}")
            return True
        else:
            print(f"❌ Summary failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Summary test failed: {e}")
        return False

def test_chat(paper_id):
    """Test chatting with paper."""
    try:
        data = {"query": "What is the main contribution of this paper?"}
        response = requests.post(
            f"http://localhost:8000/chat/{paper_id}", 
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def main():
    print("🧪 Testing ResearchRAG API...")
    
    # Test health
    if not test_health():
        print("❌ Backend not running. Please start it first.")
        return
    
    # Test upload
    print("\n📄 Testing paper upload...")
    paper_id = test_upload_url()
    
    if paper_id:
        print(f"\n📊 Testing summary for paper {paper_id}...")
        test_summary(paper_id)
        
        print(f"\n💬 Testing chat for paper {paper_id}...")
        test_chat(paper_id)
    
    print("\n🎉 API tests completed!")

if __name__ == "__main__":
    main()
