import datetime
import math
import traceback

import docx

from models.file_model import FileObject
from services import stripe_service


def save_file(filename="", encodedBinFile=None, user_id=None):
    try:
        newFile = FileObject(file_name=filename, file=encodedBinFile, user_id=user_id)
        newFile.save()

        return newFile

    except Exception as e:
        print("Failed to save File:", e)
        traceback.print_exc()


def check_user_has_access_based_on_threshold_and_wordcount(user_id: str, file):
    doc = docx.Document(file)

    # get wordcount of the file
    wordcount = sum(len(para.text.split()) for para in doc.paragraphs)

    print(
        f"User {user_id} has {wordcount} words in their file")

    tier_to_upload_threshold: {int, int} = {
        0: 30,
        1: 100,
        2: math.inf
    }

    tier_to_wordcount_threshold: {int, int} = {
        0: 2000,
        1: 10000,
        2: math.inf
    }

    try:
        sub_details = stripe_service.get_subscription_details(user_id)
        sub_tier = int(sub_details["tier"])
        print("User has subscription tier", sub_tier)
    except Exception as e:
        print("Error when getting subscription details:", e)
        raise e

    # check the subscription tier
    if wordcount >= tier_to_wordcount_threshold[sub_tier]:
        print("File surpasses the wordcount threshold")
        return False, "Wordcount threshold reached"

    # check the upload threshold
    try:
        uploads_this_week = get_user_uploads_this_week(user_id)
        if uploads_this_week >= tier_to_upload_threshold[sub_tier]:
            print("User has reached the upload threshold")
            return False, "Upload threshold reached"

    except stripe_service.InternalServerError:
        return False, "Internal Server Error"

    return True, None


def get_user_uploads_this_week(user_id):
    return (FileObject.objects(
                user_id=user_id,
                created_at__gte=datetime.datetime.now() - datetime.timedelta(days=7))
            .count())
