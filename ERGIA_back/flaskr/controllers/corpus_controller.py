import json
import os
from flask import render_template, request, Blueprint, session, jsonify, url_for
import zipfile

from flaskr.services.corpus_service import CorpusService
from flaskr.mappers.impl.corpus_mapper import CorpusMapper
from flask_jwt_extended import jwt_required

corpus_bp = Blueprint('corpus', __name__)

mapper = CorpusMapper()

corpus_service = CorpusService()
TARGET_DIRECTORY = os.path.expanduser("~/Desktop/CorpusSAE")
os.makedirs(TARGET_DIRECTORY, exist_ok=True)

@corpus_bp.route('/corpus', methods=['GET'])
@jwt_required()
def corpus():
    corpus_info = corpus_service.exec_getAllTexts()
    return corpus_info

    
@corpus_bp.route('/summary/<int:summary_id>', methods=['GET'])
@jwt_required()
def read_summary(summary_id):
    try:

        summary = corpus_service.exec_getSummary(summary_id)
        
        if not summary:
            return jsonify({"error": "Résumé introuvable"}), 404

        relative_path = summary[0]["path"]
        if not relative_path:
            return jsonify({"error": "Chemin introuvable pour ce résumé"}), 404

        absolute_path = os.path.join(TARGET_DIRECTORY, relative_path)

        if not os.path.isfile(absolute_path):
            return jsonify({"error": "Fichier introuvable"}), 404

        with open(absolute_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return jsonify({
            "summary_id": summary_id,
            "path": relative_path,
            "content": content
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@corpus_bp.route('/text/<int:text_id>', methods=['GET'])
def read_Text(text_id):
    try:

        text = corpus_service.exec_getText(text_id)
        
        if not text:
            return jsonify({"error": "Résumé introuvable"}), 404
        
        relative_path = text[0]["path"]
        if not relative_path:
            return jsonify({"error": "Chemin introuvable pour ce résumé"}), 404

        absolute_path = os.path.join(TARGET_DIRECTORY, relative_path)

        if not os.path.isfile(absolute_path):
            return jsonify({"error": "Fichier introuvable"}), 404

        with open(absolute_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return jsonify({
            "text_id": text_id,
            "path": relative_path,
            "content": content
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@corpus_bp.route('/texts/<int:campaign_id>', methods=['GET'])
def get_texts_by_campaign_id(campaign_id):
    try:

        texts = corpus_service.exec_get_texts_by_campaign_id(campaign_id)
        for text in texts:
            print(text)
        if not texts:
            return jsonify({"error": "Aucun texte trouvé pour cette campagne"}), 404

        results = []

        for text in texts:
            text_id = text.get("id_original_text")
            relative_path = text.get("path")

            if not relative_path:
                results.append({
                    "text_id": text_id,
                    "error": "Chemin introuvable pour ce résumé"
                })
                continue

            absolute_path = os.path.join(TARGET_DIRECTORY, relative_path)

            if not os.path.isfile(absolute_path):
                results.append({
                    "text_id": text_id,
                    "error": "Fichier introuvable"
                })
                continue

            try:
                with open(absolute_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                results.append({
                    "text_id": text_id,
                    "path": relative_path,
                    "content": content
                })
            except Exception as e:
                results.append({
                    "text_id": text_id,
                    "error": f"Erreur lors de la lecture du fichier: {str(e)}"
                })

        return jsonify(results), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@corpus_bp.route('/summaries/<int:original_text_id>', methods=['GET'])
def get_summaries_by_campaign_id(original_text_id):
    try:

        texts = corpus_service.exec_get_summaries_by_text_id(original_text_id)
        if not texts:
            return jsonify({"error": "Aucun texte trouvé pour cette campagne"}), 404

        results = []

        for text in texts:
            print(text)
            id_summary = text.get("id_summary")
            relative_path = text.get("path")
            original_text_id = text.get("original_text_id")
            annotator_id = text.get("annotator_id")

            if not relative_path:
                results.append({
                    "id_summary": id_summary,
                    "error": "Chemin introuvable pour ce résumé"
                })
                continue

            absolute_path = os.path.join(TARGET_DIRECTORY, relative_path)

            if not os.path.isfile(absolute_path):
                results.append({
                    "id_summary": id_summary,
                    "error": "Fichier introuvable"
                })
                continue

            try:
                with open(absolute_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                results.append({
                    "id_summary": id_summary,
                    "path": relative_path,
                    "content": content,
                    "annotator_id": annotator_id
                })
            except Exception as e:
                results.append({
                    "id_summary": id_summary,
                    "error": f"Erreur lors de la lecture du fichier: {str(e)}"
                })

        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500