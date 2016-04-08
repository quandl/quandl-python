from .model_list import ModelList


class PaginatedList(ModelList):
    def has_more_results(self):
        return self.meta['total_pages'] > self.meta['current_page']
