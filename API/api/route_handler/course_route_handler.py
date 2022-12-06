from flask_login import current_user

from lib.config import loader
from lib.mongo.connection import MongoConnection

from bson.objectid import ObjectId
import json
import random
import string

def course_get(request):
    course_id = request.args.get("course_id")
    mongo = MongoConnection()
    course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})

    if not course:
        return json.dumps({"error": "Requested course does not exist."}), 400

    # auth levels: owner => public => student private
    if course["owner"] == ObjectId(current_user.get_id()):
        return _course_get_as_owner(course)

    if course["public"]:
        return _course_get_as_public(course)

    return _course_get_as_private_student(course)


def course_create(request):
    payload = json.loads(request.data)
    course_name = payload["courseName"]
    course_short_description = payload["courseShortDescription"]
    is_course_public = payload["isCoursePublic"]
    magic_join_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

    # 'None' is used as the option for no course during project creation, this
    # we need to make it not allowed as a course name.
    if course_name == "None":
        return json.dumps({"error": "'None' is not allowed as a course name. Please use a different name."}), 400

    mongo = MongoConnection()
    existing_course = mongo.db.courses.find_one({"name": course_name, "owner": ObjectId(current_user.get_id())})
    if existing_course:
        return json.dumps({"error": "You already have a course with this name. Please use a different name."}), 400

    mongo.db.courses.insert_one({
        "name": course_name,
        "short_description": course_short_description,
        "magic_join_key": magic_join_key,
        "public": is_course_public,
        "owner": ObjectId(current_user.get_id()),
    })

    host_domain = loader.load_server_config()["host_domain"]
    magic_join_url = f"{host_domain}/course/join/{magic_join_key}"

    return json.dumps({"magic_join_url": magic_join_url}), 200


def course_join(request):
    payload = json.loads(request.data)
    magic_join_key = payload["magicJoinKey"]

    mongo = MongoConnection()

    course = mongo.db.courses.find_one({"magic_join_key": magic_join_key})
    if not course:
        return json.dumps({"error": "Requested course does not exist."}), 400

    if course["owner"] == ObjectId(current_user.get_id()):
        return json.dumps({"error": "User cannot enroll in a course they own."}), 400

    existing_enrollment = mongo.db.course_enrollments.find_one({"user": ObjectId(current_user.get_id()), "course": course["_id"]})
    if existing_enrollment:
        return json.dumps({"error": "User already enrolled in course."}), 400

    mongo.db.course_enrollments.insert_one({
        "course": course["_id"],
        "user": ObjectId(current_user.get_id()),
    })

    return json.dumps({"course_name": course["name"]}), 200


def course_list_all(request):
    """All courses a user is enrolled in, owns, or public courses"""
    mongo = MongoConnection()

    enrollments = list(mongo.db.course_enrollments.find({"user": ObjectId(current_user.get_id())}))
    course_ids = [c["course"] for c in enrollments]

    all_courses = list(mongo.db.courses.find({"$or": [
        {"public": True},
        {"owner": ObjectId(current_user.get_id())},
        {"_id": {"$in": course_ids}}
    ]}))
    
    formatted_courses = list(map(_format_course, all_courses))
    return json.dumps({"courses": formatted_courses}), 200


def course_list_user(request):
    mongo = MongoConnection()
    enrollments = list(mongo.db.course_enrollments.find({"user": ObjectId(current_user.get_id())}))
    course_ids = [c["course"] for c in enrollments]
    courses = list(mongo.db.courses.find({"_id": {"$in": course_ids}}))
    formatted_courses = list(map(_format_course, courses))
    return json.dumps({"courses": formatted_courses}), 200


def course_list_owner(request):
    mongo = MongoConnection()
    owned_courses = list(mongo.db.courses.find({"owner": ObjectId(current_user.get_id())}))
    formatted_courses = list(map(_format_course, owned_courses))
    return json.dumps({"courses": formatted_courses}), 200


def _format_course(course):
    mongo = MongoConnection()
    num_learners = len(list(mongo.db.course_enrollments.find({"course": course["_id"]})))
    host_domain = loader.load_server_config()["host_domain"]
    magic_join_url = f"{host_domain}/course/join/{course['magic_join_key']}"

    return {
        "_id": str(course["_id"]),
        "name": course["name"],
        "short_description": course["short_description"],
        "magic_join_url": magic_join_url,
        "magic_join_key": course["magic_join_key"],
        "num_learners": num_learners,
        "course_url": f"/course/view/{str(course['_id'])}",
        "owner": str(course["owner"]),
        "is_owner": course["owner"] == ObjectId(current_user.get_id())
    }


def _course_get_as_owner(course):
    return _course_get_as_public(course)


def _course_get_as_public(course):
    formatted_course = _format_course(course)
    return json.dumps({"course": formatted_course}), 200


def _course_get_as_private_student(course):
    mongo = MongoConnection()
    enrollment = mongo.db.course_enrollments.find_one({"user": ObjectId(current_user.get_id()), "course": course["_id"]})
    if not enrollment:
        return json.dumps({"error": "User not enrolled in private course."}), 400

    formatted_course = _format_course(course)
    privatized_course = _filter_private_course_fields(formatted_course)
    return json.dumps({"course": privatized_course}), 200


def _filter_private_course_fields(course):
    del course["magic_join_url"]
    del course["magic_join_key"]
    return course
