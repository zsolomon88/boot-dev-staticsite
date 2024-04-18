class HTMLNode:
    def __init__(self, tag, value="", children=[], props={}) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str = props_str + f" {key}=\"{value}\""
        return props_str
    
    def __repr__(self) -> str:
        html_string = f"<{self.tag}{self.props_to_html()}>"
        if len(self.children) > 0:
            for child in self.children:
                html_string = html_string + str(child)
        else:
            html_string = html_string + f"{self.value}"

        html_string = html_string + f"</{self.tag}>"

        return html_string
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}) -> None:
        super().__init__(tag, value, [], props)
    
    def to_html(self):
        if not self.value:
            return f"<{self.tag}{self.props_to_html()} />"
            #raise ValueError("All leaf nodes require a value")
        
        return f"{self.value}" if not self.tag else f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes need a tag")
        
        if len(self.children) <= 0:
            raise ValueError("Parent nodes need 1 or more children")
        
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string = html_string + child.to_html()
        html_string = html_string + f"</{self.tag}>"

        return html_string