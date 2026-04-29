#!/usr/bin/env python3
"""Parse AgentCore service reference JSON and group actions by subservice."""

import json
import os
import re
import urllib.request
from datetime import datetime

URL = "https://servicereference.us-east-1.amazonaws.com/v1/bedrock-agentcore/bedrock-agentcore.json"
STATE_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".agentcore-actions.json")

# Canonical subservice groupings derived from resource types.
RESOURCE_TO_SUBSERVICE = {
    "runtime": "Agent Runtime",
    "runtime-endpoint": "Agent Runtime",
    "gateway": "Gateway",
    "memory": "Memory",
    "token-vault": "Identity & Credentials",
    "workload-identity": "Identity & Credentials",
    "workload-identity-directory": "Identity & Credentials",
    "oauth2credentialprovider": "Identity & Credentials",
    "apikeycredentialprovider": "Identity & Credentials",
    "policy-engine": "Policy Engine",
    "policy": "Policy Engine",
    "policy-generation": "Policy Engine",
    "browser": "Browser",
    "browser-custom": "Browser",
    "browser-profile": "Browser",
    "code-interpreter": "Code Interpreter",
    "code-interpreter-custom": "Code Interpreter",
    "evaluator": "Evaluation",
    "online-evaluation-config": "Evaluation",
    "registry": "Tool Registry",
    "registry-record": "Tool Registry",
    "harness": "Harness",
}

# Patterns for inferring subservice from action names (fallback).
NAME_PATTERNS = [
    (r"AgentRuntime", "Agent Runtime"),
    (r"Gateway", "Gateway"),
    (r"Memory|Memories", "Memory"),
    (r"TokenVault", "Identity & Credentials"),
    (r"WorkloadIdentit", "Identity & Credentials"),
    (r"Oauth2|ApiKey|Credential|ResourceToken|ResourceOauth|ResourceApiKey",
     "Identity & Credentials"),
    (r"Policy|PolicyEngine", "Policy Engine"),
    (r"AdminPolicy", "Policy Engine"),
    (r"Browser", "Browser"),
    (r"CodeInterpreter", "Code Interpreter"),
    (r"Evaluator|OnlineEvaluation|Evaluate", "Evaluation"),
    (r"Registr", "Tool Registry"),
    (r"Harness", "Harness"),
]


def infer_subservice_from_name(action_name):
    for pattern, subservice in NAME_PATTERNS:
        if re.search(pattern, action_name):
            return subservice
    return None


def classify(actions):
    """Classify actions into subservices. Returns {subservice: [action_name, ...]}."""
    subservices = {}
    unknown = []
    for action in actions:
        name = action["Name"]
        resources = [r["Name"] for r in action.get("Resources", [])]
        props = action.get("Annotations", {}).get("Properties", {})

        if props.get("IsPermissionManagement"):
            access = "Permissions"
        elif props.get("IsTaggingOnly"):
            access = "Tagging"
        elif props.get("IsWrite"):
            access = "Write"
        elif props.get("IsList"):
            access = "List"
        else:
            access = "Read"

        matched = set()
        for r in resources:
            s = RESOURCE_TO_SUBSERVICE.get(r)
            if s:
                matched.add(s)
        if not matched:
            inferred = infer_subservice_from_name(name)
            if inferred:
                matched.add(inferred)

        entry = {"name": name, "access": access}
        if matched:
            for s in matched:
                subservices.setdefault(s, []).append(entry)
        else:
            unknown.append(entry)
    return subservices, unknown


def dedupe(acts):
    seen = set()
    unique = []
    for a in sorted(acts, key=lambda x: x["name"]):
        if a["name"] not in seen:
            seen.add(a["name"])
            unique.append(a)
    return unique


def load_previous():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None


def save_state(subservices, unknown):
    """Save current action names per subservice for diffing."""
    state = {
        "timestamp": datetime.now().isoformat(),
        "subservices": {s: sorted(set(a["name"] for a in acts)) for s, acts in subservices.items()},
        "unknown": sorted(a["name"] for a in unknown),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def print_diff(prev, subservices, unknown):
    prev_all = set()
    for names in prev["subservices"].values():
        prev_all.update(names)
    prev_all.update(prev.get("unknown", []))

    curr_all = set()
    for acts in subservices.values():
        curr_all.update(a["name"] for a in acts)
    curr_all.update(a["name"] for a in unknown)

    added = sorted(curr_all - prev_all)
    removed = sorted(prev_all - curr_all)

    if not added and not removed:
        print(f"No changes since {prev['timestamp']}")
        return

    print(f"Changes since {prev['timestamp']}:")
    for a in added:
        print(f"  + {a}")
    for a in removed:
        print(f"  - {a}")
    print()


def main():
    with urllib.request.urlopen(URL) as resp:
        data = json.loads(resp.read())

    actions = data.get("Actions", [])
    subservices, unknown = classify(actions)
    prev = load_previous()

    if prev:
        print_diff(prev, subservices, unknown)

    total = 0
    for sub in sorted(subservices):
        unique = dedupe(subservices[sub])
        print(f"\n## {sub} ({len(unique)} actions)")
        for a in unique:
            print(f"  {a['access']:12s} {a['name']}")
        total += len(unique)

    if unknown:
        print(f"\n## UNKNOWN ({len(unknown)} actions)")
        for a in unknown:
            print(f"  {a['access']:12s} {a['name']}")
        total += len(unknown)

    print(
        f"\nTotal: {total} actions across {len(subservices)} subservices", end="")
    if unknown:
        print(f" ({len(unknown)} unclassified)")
    else:
        print(" (all classified)")

    save_state(subservices, unknown)
    print(f"State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
