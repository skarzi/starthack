class TransactionHistory:
    def __init__(self, data):
        """
        :param data: parsed json response from DB API
        """
        self.data = data

    def sort_recommendations(self, items, key_extractor=None):
        """ sort items by occurences in financial history """

        def rate_item(item):
            if key_extractor:
                key = key_extractor(item)
            else:
                key = item
            value = sum(
                [key.lower() in record["counterPartyName"].lower()
                 for record in self.data]
            )
            return value

        items = sorted(items, key=rate_item, reverse=True)
        return items
