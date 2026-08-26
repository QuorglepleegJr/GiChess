class AttributeModule:

    def __init__(self, **kwargs):

        self.attributes = kwargs

    def get_attribute(self, attribute):

        return self.attributes.get(attribute)