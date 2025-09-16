from flask import Blueprint, jsonify, render_template
from .models import User, Project, File, Image
from neomodel import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/tokens')
def list_tokens():
    users = User.nodes.all()
    tokens = [{'google_id': user.google_id, 'name': user.name} for user in users]
    return jsonify(tokens)

@main.route('/projects')
def list_projects():
    projects = Project.nodes.all()
    project_list = [{'name': project.name} for project in projects]
    return jsonify(project_list)

@main.route('/files/<project_name>')
def list_files(project_name):
    project = Project.nodes.first(name=project_name)
    if project:
        files = project.files.all()
        file_list = [{'name': file.name} for file in files]
        return jsonify(file_list)
    return jsonify({'error': 'Project not found'}), 404

@main.route('/images/<google_id>')
def list_images(google_id):
    query = """
    MATCH (u:User {google_id: $google_id})-[:UPLOADED]->(i:Image {width: 200})
    RETURN i.url AS url
    """
    results, meta = db.cypher_query(query, {'google_id': google_id})
    images = [{'url': result[0]} for result in results]
    return jsonify(images)

@main.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@main.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500