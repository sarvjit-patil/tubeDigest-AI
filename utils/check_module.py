import sys
import os
import importlib.util

def check_module(module_name):
    print(f"Checking module: {module_name}")
    try:
        spec = importlib.util.find_spec(module_name)
        if spec:
            print(f"  Found at: {spec.origin}")
            if spec.submodule_search_locations:
                print(f"  Is package, locations: {spec.submodule_search_locations}")
        else:
            print("  Not found.")
    except Exception as e:
        print(f"  Error: {e}")

check_module("youtube_transcript_api")
check_module("youtube_transcript_api._api")
