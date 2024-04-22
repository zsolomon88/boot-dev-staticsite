import os, shutil
from textnode import TextNode, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    #text_node = TextNode("This is a text node", "bold", "http://www.boot.dev")
    #print(text_node)
    from_path = "content"
    dest_path = "public"
    template_path = "template.html"
    copy_dir("static", "public")
    generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        markdown_file = open(from_path)
        markdown_text = markdown_file.read()
        markdown_file.close()
    except OSError as e:
        print(e)
        return
    
    html_nodes = markdown_to_html_node(markdown_text)

    title = extract_title(html_nodes)
    if not title:
        raise Exception("Invalid markdown, no title")

    try:
        template_file = open(template_path)
        template_text = template_file.read()
        template_file.close()
    except OSError as e:
        print(e)
        return
    
    template_with_title = template_text.replace("{{ Title }}", title)
    template_with_content = template_with_title.replace("{{ Content }}", html_nodes.to_html())

    try:
        dest_file = open(dest_path, mode="w")
        dest_file.write(template_with_content)
        dest_file.close()
    except OSError as e:
        print(e)
        return    


def extract_title(html_node):
    if html_node.tag == "h1":
        return html_node.children[0].value
    
    for child in html_node.children:
        title = extract_title(child)
        if title != None:
            return title
        
    return None

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    file_list = os.listdir(dir_path_content)
    for file in file_list:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        if os.path.isfile(os.path.join(dir_path_content, file)):
            file_name = file.split(".")
            dest_name = f"{file_name[0]}.html"
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, dest_name))


def copy_dir(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    if not os.path.exists(source):
        raise FileNotFoundError("Source path does not exist")
    
    file_list = os.listdir(source)
    for file in file_list:
        if os.path.isfile(os.path.join(source, file)):
            shutil.copy(os.path.join(source, file), os.path.join(dest, file))
        if os.path.isdir(os.path.join(source, file)):
            copy_dir(os.path.join(source, file), os.path.join(dest, file))


        



main()