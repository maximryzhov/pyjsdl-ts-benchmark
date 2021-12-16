#! python
import os
import sys
from subprocess import call
import shutil

template = """<!doctype html>
<meta charset="utf-8">
<html>
<body style="background-color:black">
<div id="__panel__"></div>
{0}
</body>
</html>
"""

target_dir = "__target__"

def main(filename):
    compile_result = call(["transcrypt", "-n", filename])
    # 0 is successfull result
    if compile_result == 0:
        name = os.path.splitext(filename)[0]
        tag = f'<script type="module" src="{name}.js"></script>'
        txt = template.format(tag)
        print(f"Saving HTML file to {target_dir}")
        with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
            print(txt, file=f)
        
        for filename in os.listdir("public"):
            source = os.path.join("public", filename)
            dest = os.path.join(target_dir, filename)
            print(f"Copying {filename} to public")
            shutil.copy(source, dest)

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        pass
