from flask import Blueprint, jsonify, request
import json
from functools import wraps
import random
import jwt

with open('conf.json', 'r') as f:
    SECRET_KEY = json.load(f)
    
with open('characters.json', 'r') as f:
    characters = json.load(f)
    
login_bp = Blueprint('login', __name__)
characters_bp = Blueprint('characters', __name__)

SECRET_KEY = SECRET_KEY.get('SECRET_KEY')

#home
@characters_bp.route('/')
def home():
    return "API de Game of Thrones"


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated_function

#1.characters/ limit y skip
@characters_bp.route('/characters', methods=['GET'])
def get_characters():
    try:
        limit = int(request.args.get('limit')) if request.args.get('limit') else None
        skip = int(request.args.get('skip')) if request.args.get('skip') else 0
    except ValueError:
        return jsonify({"error": "The 'limit' and 'skip' parameters must be numbers"}), 400

    if limit is not None:
        if skip >= len(characters):
            return jsonify({"error": "The value of 'skip' is greater than the number of available characters"}), 400
        paginated_characters = characters[skip:skip + limit]
    else:
        paginated_characters = random.sample(characters, min(20, len(characters)))

    return jsonify(paginated_characters)

# 2. /characters/45
@characters_bp.route('/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):

    character_found = None
    for character in characters:
        if character['id'] == id:
            character_found = character
            break 
    
    if character_found is None:
        return jsonify({"error": "Character not found"}), 404

    return jsonify(character_found)

# 3./filtered/?name=...

@characters_bp.route('/characters/filtered', methods=['GET'])
def get_filtered_characters():
    
    name_filter = request.args.get('name', '').lower()
    house_filter = request.args.get('house', '').lower()
    animal_filter = request.args.get('animal', '').lower()
    symbol_filter = request.args.get('symbol', '').lower()
    nickname_filter = request.args.get('nickname', '').lower()
    role_filter = request.args.get('role', '').lower()
    strength_filter = request.args.get('strength', '').lower()
    age_more_than = request.args.get('age_more_than', None)
    age_less_than = request.args.get('age_less_than', None)
    death_filter = request.args.get('death', None)

    filtered_characters = characters
    
    if name_filter != '':
        new_list = []
        for character in filtered_characters:
            if name_filter in (character.get('name') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if house_filter != '':
        new_list = []
        for character in filtered_characters:
            if house_filter in (character.get('house') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if animal_filter != '':
        new_list = []
        for character in filtered_characters:
            if animal_filter in (character.get('animal') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if symbol_filter != '':
        new_list = []
        for character in filtered_characters:
            if symbol_filter in (character.get('symbol') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if nickname_filter != '':
        new_list = []
        for character in filtered_characters:
            if nickname_filter in (character.get('nickname') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if role_filter != '':
        new_list = []
        for character in filtered_characters:
            if role_filter in (character.get('role') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    if strength_filter != '':
        new_list = []
        for character in filtered_characters:
            if strength_filter in (character.get('strength') or '').lower():
                new_list.append(character)
        filtered_characters = new_list

    # age_more_than=25
        
    if age_more_than:
        try:
            age_more_than = int(age_more_than)
            new_list = []
            for character in filtered_characters:
                if character.get('age') is not None and character['age'] >= age_more_than:
                    new_list.append(character)
            filtered_characters = new_list
        except ValueError:
            return jsonify({"error": "The value of 'age_more_than' must be a number."}), 400

    # age_less_than=50
    
    if age_less_than:
        try:
            age_less_than = int(age_less_than)
            new_list = []
            for character in filtered_characters:
                if character.get('age') is not None and character['age'] <= age_less_than:
                    new_list.append(character)
            filtered_characters = new_list
        except ValueError:
            return jsonify({"error": "The value of 'age_less_than' must be a number."}), 400

    # death=true or death=false
    
    if death_filter is not None and death_filter != "":
        new_list = []
        if death_filter.lower() == 'true':
            for character in filtered_characters:
                if character.get('death') is not None:
                    new_list.append(character)
        elif death_filter.lower() == 'false':
            for character in filtered_characters:
                if character.get('death') is None:
                    new_list.append(character)
        else:
            return jsonify({"error": "The value of 'death' must be 'true' or 'false'."}), 400
        filtered_characters = new_list


# sorting=name&order=sort_des or sorting=name&order=sort_asc
    
    sort_by = request.args.get('sorting', '').lower()  
    order = request.args.get('order', 'sort_asc').lower() 

    if sort_by:
        try:
            filtered_characters = sorted(filtered_characters, key=lambda x: (x.get(sort_by) is None, x.get(sort_by)),reverse=(order == 'sort_des'))
        except KeyError:
            return jsonify({"error": f"Cannot sort by field '{sort_by}'."}), 400

    return jsonify(filtered_characters)

# new_character

@characters_bp.route('/characters', methods=['POST'])
@token_required
def add_character(current_user):
    new_character_data = request.get_json()

    if not new_character_data:
        return jsonify({"error": "No data sent"}), 400

    required_fields = ['name', 'house', 'animal', 'symbol', 'nickname', 'role', 'strength']
    for field in required_fields:
        if field not in new_character_data or not isinstance(new_character_data[field], str) or not new_character_data[field].strip():
            return jsonify({"error": f"Field '{field}' is required and must be a non-empty string."}), 400

    if 'age' in new_character_data and not isinstance(new_character_data['age'], int):
        return jsonify({"error": "Field 'age' must be a number."}), 400

    if 'death' in new_character_data and new_character_data['death'] is not None:
        if not isinstance(new_character_data['death'], int):
            return jsonify({"error": "Field 'death' must be a number or null."}), 400

    new_id = max([character['id'] for character in characters], default=0) + 1 
    new_character_data['id'] = new_id

    characters.append(new_character_data)

    return jsonify(new_character_data), 201


# update_character character/22
@characters_bp.route('/characters/<int:id>', methods=['PUT'])
@token_required
def update_character(current_user,id):
    updated_data = request.get_json()

    character = next((c for c in characters if c['id'] == id), None)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    if not updated_data:
        return jsonify({"error": "No data sent"}), 400

    #fields that can be updated
    
    updatable_fields = ['name', 'house', 'animal', 'symbol', 'nickname', 'role', 'strength', 'age', 'death']

    for field in updatable_fields:
        if field in updated_data:
            if field in ['name', 'house', 'animal', 'symbol', 'nickname', 'role', 'strength']:
                if not isinstance(updated_data[field], str) or not updated_data[field].strip():
                    return jsonify({"error": f"Field '{field}' must be a non-empty string."}), 400
            if field == 'age':
                if not isinstance(updated_data[field], int):
                    return jsonify({"error": "Field 'age' must be a number."}), 400
            if field == 'death':
                if updated_data[field] is not None and not isinstance(updated_data[field], int):
                    return jsonify({"error": "Field 'death' must be a number or null."}), 400

            character[field] = updated_data[field]

    return jsonify(character), 200

# delete character = character/16

@characters_bp.route('/characters/<int:id>', methods=['DELETE'])
@token_required
def delete_character(current_user,id):

    character = next((c for c in characters if c['id'] == id), None)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    characters.remove(character)

    return jsonify({"message": f"Character with id {id} has been deleted."}), 200

login_bp = Blueprint('login', __name__)