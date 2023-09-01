from user_auth.auth_helper import app
from db_helpers.db_helpers import save_prediction_with_answers, get_predictions
from flask import request


#
# @app.before_request
# @app.route('/prediction', methods=['GET'])
# def some_existing_route():
#     ab_tk = get_logged_user_info()
#     obj_id = ab_tk["objectId"]
#     print("objid", obj_id)
#     return ab_tk
@app.route('/testSaveAnswers', methods=['POST'])
def test_save_method():
    answer_dict = request.json
    pred = 0.1
    save_prediction_with_answers(answer_dict, pred)
    return {"message": "Records saved successfully"}, 201

@app.route('/getPredictions', methods=['get'])
def test_get_preds():
    preds = get_predictions()
    return preds

if __name__ == '__main__':
    app.run(debug=True)
