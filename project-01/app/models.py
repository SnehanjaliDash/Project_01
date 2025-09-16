from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, config

# Configure Neo4j connection
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

class User(StructuredNode):
    google_id = StringProperty(unique_index=True)
    name = StringProperty()
    uploaded_images = RelationshipTo('Image', 'UPLOADED')

class Project(StructuredNode):
    name = StringProperty(unique_index=True)
    files = RelationshipTo('File', 'CONTAINS')

class File(StructuredNode):
    name = StringProperty()
    project = RelationshipFrom(Project, 'CONTAINS')

class Image(StructuredNode):
    url = StringProperty()
    width = IntegerProperty()
    uploaded_by = RelationshipFrom(User, 'UPLOADED')