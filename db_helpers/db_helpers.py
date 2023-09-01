from flask import Flask, request, jsonify
from db_utils.connection import mongo
from user_auth.helpers import get_logged_user_info
from flask_restful import Resource, reqparse, Api
from datetime import datetime
app = Flask(__name__)

from user_auth.helpers import get_logged_user_info


def save_prediction_with_answers(data_dict, prediction):
    data_dict["user_id"] = get_logged_user_info()["objectId"]
    data_dict["prediction"] = prediction
    data_dict["timestamp"] = datetime.now()
    collection = mongo.db.final_output  # Replace with your collection name
    inserted_id = collection.insert_one(data_dict).inserted_id
    return jsonify({'message': 'Data added successfully', 'inserted_id': str(inserted_id)})


def get_predictions():
    user_id = get_logged_user_info()["objectId"]
    collection = mongo.db.final_output

    # Query MongoDB to retrieve documents with the specified user_id
    # cursor = collection.find({"user_id": user_id})
    #
    # # Initialize a list to store the predictions
    # predictions = []
    #
    # # Iterate through the cursor to extract the predictions
    # for document in cursor:
    #     prediction = document.get("prediction")
    #     if prediction is not None:
    #         predictions.append(prediction)
    #
    # # Return the list of predictions as a JSON response
    # return jsonify(predictions)
    cursor = collection.find({"user_id": user_id})

    # Initialize variables to track the latest prediction and timestamp
    latest_prediction = None
    latest_timestamp = None

    # Get the current timestamp using datetime.now()
    now = datetime.now()

    # Iterate through the cursor to find the latest prediction
    for document in cursor:
        prediction = document.get("prediction")
        timestamp_str = document.get("timestamp")  # Assuming there's a "timestamp" field
        if prediction is not None and timestamp_str is not None:
            # Compare the timestamp (assuming it's already a datetime object) with the current time
            time_difference = now - timestamp_str
            if latest_timestamp is None or time_difference.total_seconds() < latest_timestamp:
                latest_prediction = prediction
                latest_timestamp = time_difference.total_seconds()

    # Return the latest prediction as a JSON response
    if latest_prediction is not None:
        return jsonify({"latest_prediction": latest_prediction})
    else:
        return jsonify({"message": "No predictions found for the user"})
