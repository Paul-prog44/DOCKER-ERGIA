from flaskr.models.original_text_model import OriginalTextModel
from werkzeug.exceptions import BadRequest, NotFound


class OriginalTextService :

    def __init__(self):
        self.original_text_model = OriginalTextModel()

    def exec_get_original_texts_by_campaign_id(self, campaign_id):
        list_original_texts = self.original_text_model.get_original_text_by_campaign_id(campaign_id)
        return list_original_texts