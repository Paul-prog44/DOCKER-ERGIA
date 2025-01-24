from flask import render_template, request, Blueprint, session, jsonify, url_for
from flaskr.services.annotation_service import AnnotationService
from flask_jwt_extended import jwt_required


annotation_bp = Blueprint('annotation', __name__)

annotation_service = AnnotationService()

@annotation_bp.route('/annotations/<int:annotation_id>', methods= ['GET'])
@jwt_required()
def get_annotation(annotation_id):
    annotation = annotation_service.exec_get_annotation(annotation_id)
    return jsonify(annotation), 200

@annotation_bp.route('/annotations', methods= ['POST'])
@jwt_required()
def create_annotations():
    annotations = request.get_json()
    annotations = annotation_service.exec_add_annotation(annotations)
    return jsonify(annotations), 200