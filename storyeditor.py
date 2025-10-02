# story_builder.py
import json, os

DB = "story.json"

def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return {"start": {"text":"Your story begins...", "options":{}}}

def save(data):
    json.dump(data, open(DB,"w"), indent=2)

def play(data):
    node = "start"
    while True:
        n = data.get(node)
        if not n:
            print("Missing node:", node); break
        print("\n" + n["text"] + "\n")
        opts = n.get("options", {})
        if not opts:
            print("The end.")
            break
        for i,(k,v) in enumerate(opts.items(),1):
            print(f"{i}. {k}")
        choice = input("Choose: ").strip()
        try:
            idx = int(choice)-1
            key = list(opts.keys())[idx]
            node = opts[key]
        except:
            print("Invalid choice; try again.")

def edit(data):
    while True:
        cmd = input("\n(edit) add/view/connect/play/quit: ").strip().lower()
        if cmd == "add":
            name = input("Node id: ").strip()
            text = input("Text: ").strip()
            data[name] = {"text": text, "options": {}}
            save(data)
            print("Added.")
        elif cmd == "view":
            for k,v in data.items():
                print("-", k, "->", list(v.get("options",{}).items()))
        elif cmd == "connect":
            src = input("From node id: ").strip()
            if src not in data: print("No such node."); continue
            label = input("Option label shown to player: ").strip()
            dst = input("To node id: ").strip()
            if dst not in data: print("No such destination."); continue
            data[src].setdefault("options", {})[label] = dst
            save(data); print("Connected.")
        elif cmd == "play":
            play(data)
        elif cmd == "quit":
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    story = load()
    print("Branching Story Builder / Player")
    edit(story)
