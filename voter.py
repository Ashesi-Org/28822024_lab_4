# from https://pythonbasics.org/flask-rest-api/  
import json
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/voters', methods=['POST'])
def create_voter():
    record = json.loads(request.data)
    with open('./tmp/voter.txt', 'r') as f:
        voter = f.read()
    if not voter:
        records = [record]
    else:
        records = json.loads(voter)
        election_id = str(uuid.uuid4())
        record['id'] = election_id
        records.append(record) 
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/voters', methods=['GET'])
def query_records():
    id = request.args.get('id')
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['id'] == id:
                return jsonify(record)
        return jsonify({'error': 'data not found'}), 404

@app.route('/voters', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['id'] == record['id']:
            r['email'] = record['email']
            r['name'] = record['name']
            r['year'] = record['year']
            r['major'] = record['major']
        new_records.append(r)
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

@app.route('/voters', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    new_records = []
    with open('./tmp/voter.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['id'] == record['id']:
                continue
            new_records.append(r)
    with open('./tmp/voter.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

#---------------------------------Election-------------------------------

@app.route('/elections', methods=['POST'])
def create_election():
    record = json.loads(request.data)
    
    with open('./tmp/election.txt', 'r') as f:
        election = f.read()
    if not election:
        records = [record]
        election_id = str(uuid.uuid4())
        record['id'] = election_id
    else:
        records = json.loads(election)
        election_id = str(uuid.uuid4())
        record['id'] = election_id
        records.append(record)  
    with open('./tmp/election.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/elections', methods=['GET'])
def get_elections():
    id = request.args.get('id')
    with open('./tmp/election.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['id'] == id:
                return jsonify(record)
        return jsonify({'error': 'data not found'}), 404

@app.route('/elections', methods=['DELETE'])
def delete_election():
    record = json.loads(request.data)
    new_records = []
    with open('./tmp/election.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['id'] == record['id']:
                continue
            new_records.append(r)
    with open('./tmp/election.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

#--------------------------------voting-------------------------------

@app.route('/elections/voters', methods=['POST'])
def cast_election():
    election_data = json.loads(request.data)
    new_election_data = []

    with open('./tmp/voter.txt', 'r') as f:
        voter = f.read()
        voters_req = json.loads(voter)

        # Get the voter ID from the request data
        voter_id = election_data['name']

        # Verify that the voter is registered for this election
        for r in voters_req:
                if r['id'] != voter_id:
                    return jsonify({'error': 'You are not registered to vote in this election.'}), 400

    with open('./tmp/election.txt', 'r') as f:
        election = f.read()
        election_req = json.loads(election)

        election_id = election_data['voter_id']
        # Verify that the candidate is valid and on the ballot
    for el in election_req:
            if el['id'] != election_id:
                return jsonify({'error': 'Invalid Election.'}), 400
            else:
                for election_val in election_req:
                    if election_val["id"] == election_id:

                        for position in election_val.get('positions'):
                            
                            if position.get("name") in election_data["vote"]:
                                if election_data["name"] in position.get("voters"):
                                    return jsonify({'error': 'Already voted.'}), 400
                                pos = position.get("name")
                                for cand in position['candidates']:
                                    if cand["name"] == election_data["vote"].get(pos):
                                        print(cand['results'])
                                        cand['results'] = int(cand.get("results")) + 1
                                        position.get("voters").append(election_data["name"])

                                       
    with open('./tmp/election.txt', 'w') as f:
        f.write(json.dumps(election_req, indent=2))
    return jsonify(election_req)

app.run(debug=True)