from application.models import User

def course_list(user_id):
    classes = list(User.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'enroll', 
                        'localField': 'user_id', 
                        'foreignField': 'user_id', 
                        'as': 'e1'
                    }
                }, {
                    '$unwind': {
                        'path': '$e1', 
                        'includeArrayIndex': 'e1_id', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'courses', 
                        'localField': 'e1.courseId', 
                        'foreignField': 'course_id', 
                        'as': 'e2'
                    }
                }, {
                    '$unwind': {
                        'path': '$e2', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }, {
                    '$sort': {
                        'e2.course_id': 1
                    }
                }
            ]))

    return classes