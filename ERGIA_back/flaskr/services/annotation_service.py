from flaskr.models.annotation_model import AnnotationModel
from flaskr.services.scu_service import ScuService

scu_service = ScuService()

class AnnotationService:

    def __init__(self):
        self.annotation_model = AnnotationModel()
        

    def exec_get_all_annotations(self):
        """
        Récupère toutes les annotations.
        """
        annotations = self.annotation_model.get_all_annotations()
        return annotations

    def exec_get_annotation(self, annotation_id):
        """
        Récupère une annotation spécifique par son ID.
        """
        annotation = self.annotation_model.get_annotation(annotation_id)
        return annotation

    def exec_add_annotation(self, annotations):
        """
        Ajoute une nouvelle annotation à un résumé.
        """

        for annotation in annotations:
            scu_id = scu_service.exec_create_scu(annotation['scu'])
            self.annotation_model.create_annotation(
                scu_id[0]['id_scu'], 
                annotation['color'], 
                annotation['summary_id'], 
                annotation['index'], 
                annotation['length'], 
                annotation['creator'])
            
        return annotations

    def exec_update_annotation(self, annotation_id, scu, comment):
        """
        Met à jour une annotation existante avec de nouvelles informations.
        """
        updated = self.annotation_model.update_annotation(annotation_id, scu, comment)
        return updated

    def exec_delete_annotation(self, annotation_id):
        """
        Supprime une annotation spécifique par son ID.
        """
        deleted = self.annotation_model.delete_annotation(annotation_id)
        return deleted
