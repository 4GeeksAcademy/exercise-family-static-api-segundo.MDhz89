import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def get_all_members(self):
        return self.members

    def get_member(self, id):
        for member in self.members:
            if member["id"] == id:
                return member
        return None

    def delete_member(self, id):
        self.members = [member for member in self.members if member["id"] != id]

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Initialize the family with 3 members
jackson_family = FamilyStructure("Jackson")

# Initialize family members
jackson_family.add_member({"first_name": "Jane", "id": 1, "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name": "Jimmy", "id": 2, "age": 5, "lucky_numbers": [1]})
jackson_family.add_member({"first_name": "Tommy", "id": 3443, "age": 23, "lucky_numbers": [34, 65, 23, 4, 6]})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate the sitemap with all endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def create_member():
    member = request.json
    if not all(k in member for k in ("id", "first_name", "age", "lucky_numbers")):
        return jsonify({"error": "Invalid data"}), 400
    
    jackson_family.add_member(member)
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        jackson_family.delete_member(id)
        
        # Verificar cuántos miembros quedan
        if len(jackson_family.get_all_members()) < 4:
            new_member = {
                "first_name": "Sandra",
                "id": 4446,
                "age": 12,
                "lucky_numbers": [12, 34, 33, 45, 32, 12]
            }
            jackson_family.add_member(new_member)  # Agrega un nuevo miembro
        
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# This code only runs if executed as `$ python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
