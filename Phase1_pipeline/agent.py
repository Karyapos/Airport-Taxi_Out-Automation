from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import pandas as pd
import json
import subprocess

if len(sys.argv)!= 2 :
    print("Usasge: python agent.py <path_to_csv>")
    sys.exit(1)
csv = sys.argv[1]
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command and return stdout",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_json",
            "description": "Read a JSON file and return its contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_python_and_run",
            "description": "Write a python script to disk and execute it",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "code":     {"type": "string", "description": "Full python code to write"}
                },
                "required": ["filename", "code"]
            }
        }
    }
]

def run_tool(name, args):
    if name == "run_shell":
        result = subprocess.run(args["command"], shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr

    if name == "read_json":
        with open(args["filepath"]) as f:
            return json.dumps(json.load(f), indent=2)

    if name == "write_python_and_run":
        with open(args["filename"], "w") as f:
            f.write(args["code"])
        result = subprocess.run(["python", args["filename"]], capture_output=True, text=True)
        return result.stdout + result.stderr
    
system = """
You are a helping tool of a data analyst, you will be provided a csv file and you will execute
a pipeline producing in the end some plots. You have 3 tools run_shell,read_json, 
and write_python_and_run.
For any plots you will be asked to provide use:
-White background
-Color combinations around #708C60 and #C4E7B1 for darker and lighter purposes.
-Name axis' names after columns names but instead of _ put space(" ")
-Write and run a matplotlib script (use matplotlib.use('Agg'), savefig not plt.show)
-Keep it simple and direct

Your tasks are:
-Run the main pipeline: main.py with the csv file
-Read the outliers_report.json file to see which columns are flaged and print the results 
with small explanatory text, presenting the rows that are possible outliers. (If outliers_report.json 
is empty print nothing, ignore the rest of your tasks and just create a histogram of taxi_out 
save as taxi_out_report.png)
-According to the outliers_report.json create a png file that has scatterplots for each column 
flagged vs taxi_out and in the end a histogram of taxi_out. All together as one png file
saved as report.png
"""
messages = [
    {"role": "system", "content": system},
    {"role": "user",   "content": f"Run the pipeline on {csv} and create the plots."}
]

print("Agent starting...\n")

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        messages=messages
    )

    msg = response.choices[0].message
    messages.append(msg)

    # done
    if msg.tool_calls is None:
        print(msg.content)
        break

    for tc in msg.tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments)
        print(f"→ {name}({args})")
        result = run_tool(name, args)
        print(f"  {result[:200]}\n")   

        messages.append({
            "role":         "tool",
            "tool_call_id": tc.id,
            "content":      result
        })