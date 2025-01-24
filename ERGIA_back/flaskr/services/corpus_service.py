from flaskr.models.corpus_model import CorpusModel

class CorpusService:

    corpus_model: CorpusModel

    def __init__(self):
        self.corpus_model = CorpusModel()

    def exec_getAllTexts(self):
        
        summaries = self.corpus_model.get_all_texts()
        return summaries
    
    def exec_selectLastText(self):
        summary = self.corpus_model.get_last_text()
        return summary
    
    def exec_addText(self, path, campaign_id):
        idText = self.corpus_model.add_text(path, campaign_id)
        return idText

    def exec_addSummary(self, path, idText, iaGenerated):
        idsummary = self.corpus_model.add_summary(path, idText, iaGenerated)
        return idsummary
    
    def exec_getSummary(self, id):
        summary = self.corpus_model.get_summary(id)
        return summary
    
    def exec_getText(self, text_id):
        text = self.corpus_model.get_text(text_id)
        return text
    
    def exec_get_texts_by_campaign_id(self, campaign_id):
        texts = self.corpus_model.get_texts_by_campaign_id(campaign_id)
        return texts
    
    def exec_get_summaries_by_text_id(self, original_text_id):
        summaries = self.corpus_model.get_summaries_by_text_id(original_text_id)
        return summaries