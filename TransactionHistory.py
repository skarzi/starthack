class TransactionHistory:
    def __init__(self, data):
        """
        :param data: parsed json response from DB API
        """
        self.data = data

    def sort_recommendations(self, items, key_extractor):
        """ sort items by occurences in financial history """

        def rate_item(item):
            key = key_extractor(item)
            value = sum(
                [key.lower() in record["counterPartyName"].lower()
                 for record in self.data]
            )
            return value

        items = sorted(items, key=rate_item, reverse=True)
        return items
