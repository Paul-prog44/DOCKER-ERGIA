from flaskr.entities.users.user_response_dto import UserResponseDTO
from flaskr.mappers.i_mapper import Mapper


class UserMapper(Mapper):
    def map(self, json) -> dict:
        # print(json)
        json_item = dict(json[0][0])
        # print(json_item)
        mapped_item = UserResponseDTO()
        mapped_item.email = json_item['email']
        mapped_item.id_user = json_item['id_user']
        mapped_item.first_name = json_item['firstname']
        mapped_item.last_name = json_item['lastname']
        return mapped_item.__dict__