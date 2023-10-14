from flask import Flask, jsonify, request
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


@app.route('/ai/health-check', methods=['GET'])
def hello():
    return jsonify(message="Working")


@app.route('/ai/skills-match', methods=['POST'])
def post_example():
    try:
        # Get the JSON data from the request
        similar_skills = []
        skills_similarities = []
        match_skills_similarities = []

        # Process the JSON data (you can perform any necessary operations here)
        jdata = request.get_json()
        senior_skills = jdata['senior_skills']
        junior_skill = jdata['junior_skill']
        similarity_threshold = jdata['similarity_threshold']

        print("senior_skills: " + str(senior_skills))
        print("junior_skill: " + str(junior_skill))

        # Tokenize the working area
        working_area_tokens = nlp(junior_skill.lower())

        # Calculate similarity between skills and the working area
        for skill in senior_skills:
            skill_tokens = nlp(skill.lower())
            similarity = skill_tokens.similarity(working_area_tokens)
            print(str(skill) + ": " + str(similarity))
            # You can adjust the similarity threshold as needed
            if similarity > similarity_threshold:
                similar_skills.append(skill)
                match_skills_similarities.append(similarity)
            skills_similarities.append(similarity)
            # Respond with a JSON response
        response = {'MATCH_SKILL': similar_skills,
                    'MATCH_SKILL_SIMILARITY': sum(match_skills_similarities) / len(match_skills_similarities),
                    "SIMILARITY": sum(skills_similarities) / len(skills_similarities)}
        return jsonify(response), 200  # HTTP status code 200 (OK)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # HTTP status code 400 (Bad Request)


if __name__ == '__main__':
    app.run(debug=True)
