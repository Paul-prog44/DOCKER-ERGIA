from flaskr.entities.scus.create_scu_request_dto import CreateScuRequestDTO
from flaskr.models.scu_model import ScuModel


class ScuService:

    scu_model: ScuModel

    def __init__(self):
        self.scu_model = ScuModel()

    def exec_get_all_scus(self):
        return self.scu_model.get_all_scu()

    def exec_create_scu(self, scu_data: CreateScuRequestDTO):
        return self.scu_model.create_scu(scu_data)
