class FeatureMan:
    def __init__(self):
        self.option_name = "Manual"
        self.option_content = self.content()
        self.order = 3

    def content(self):
        return """Information about th manual inside the manual: to be recursive"""