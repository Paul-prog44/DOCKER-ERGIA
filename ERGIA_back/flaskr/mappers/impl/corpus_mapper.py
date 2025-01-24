from flaskr.entities.corpus.corpus_response_dto import CorpusResponseDTO
from flaskr.mappers.i_mapper import Mapper


class CorpusMapper(Mapper):
    def map(self, json) -> dict:
        print(json)
        json_item = dict(json[0][0])
        print(json)
        mapped_item = CorpusResponseDTO()
        mapped_item.id_original_text = json_item['id_original_text']
        mapped_item.path = json_item['path']
        mapped_item.campaign_id = json_item['campaign_id']
        return mapped_item.__dict__