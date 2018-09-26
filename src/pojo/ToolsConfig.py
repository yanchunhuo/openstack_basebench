class ToolsConfig:
    def __init__(self):
        self.cleanup_keyword = None

    @property
    def cleanup_keyword(self):
        return self.cleanup_keyword

    @cleanup_keyword.setter
    def cleanup_keyword(self,cleanup_keyword):
        self.cleanup_keyword=cleanup_keyword