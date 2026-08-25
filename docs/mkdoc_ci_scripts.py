# ---------------------------------------------------------
# Copyright (c) 2023, Materials Data Platform Center, NIMS
#
# This software is released under the MIT License.
#
# Contributor:
#     Hayato Sonokawa
# ---------------------------------------------------------
# coding: utf-8
"""
This script is a simple template engine designed for use in Continuous Integration (CI) systems.
It provides a way to generate dynamic content based on predefined templates.
Please note that this script is not intended for use in local environments.
"""
import os
import subprocess


def pdoc(target_module_path: str, output_dir_path: str):
    current_directory = os.getcwd()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(current_directory, "container") + ":" + env.get("PYTHONPATH", "")
    subprocess.run(["pdoc", "--output-dir", output_dir_path, target_module_path, "--force"], env=env)


def generate_links_for_directory(directory: str):
    """指定されたディレクトリ内のすべてのMarkdownファイルへのリンクを生成する"""
    link_base_dir_name = directory.split("/")[1]
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.md')]
    files = [os.path.splitext(f)[0] for f in files if not "index.md" in f]
    links = [f"- [{os.path.splitext(f)[0]}]({os.path.join(link_base_dir_name, f)})" for f in files]
    print(links)
    return "\n".join(links)


def main():
    module_shared_path = "container/rdetoolkit"
    module_path = "container/modules"
    try:
        pdoc(module_shared_path, "docs")
        pdoc(module_path, "docs")
    except Exception as e:
        print(f"Error generate Document: {e}")

    # テンプレートにリンクを挿入
    module_links = generate_links_for_directory("docs/modules")
    module_shared_links = generate_links_for_directory("docs/rdetoolkit")
    with open(os.path.join('docs', 'template', 'home.md'), 'r') as file:
        markdown_content = file.read()

    document = markdown_content.format(module_links=module_links, module_shared_links=module_shared_links)
    with open("docs/home.md", "w") as f:
        f.write(document)

if __name__ == "__main__":
    main()
