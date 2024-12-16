#!/usr/bin/env python
import sys
import warnings
import os
from dotenv import load_dotenv

from crew import TrendContent

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("Welcome to the Content Crew!")
    # Collect user inputs
    category = input("Please enter the category: ")
    productinfo = input("Please enter the productinfo: ")
    channel = input("Please enter the channel: ")
    notes = input("Please enter some further notes: ")

    print("\n--- Input Data ---")
    print(f"Category: {category}")
    print(f"Product Info: {productinfo}")
    print(f"Channel: {channel}")
    print(f"Notes: {notes}\n")

    inputs = {
        "category": category,
        "productinfo": productinfo,
        "channel": channel,
        "notes": notes
    }
    try:
        TrendContent().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"Error running the crew: {e}")

run()

