import requests


class Main:

    def __init__(self, lesson_id, rol_id, user_list):
        self.url = 'MOODLE URL'
        self.token = "MOODLE TOKEN"
        self.lessonID = lesson_id
        self.rolID = rol_id
        self.user_list = user_list
        
        self.i = 0
        for user in user_list:
            self.i+=1
            print(self.i)
            self.cohort_add(user)

    def get_user_id(self,user):
        params = {
            "wstoken": self.token,
            "wsfunction": "core_user_get_users",
            "moodlewsrestformat": "json",
            "criteria[0][key]": "username",
            "criteria[0][value]": user
        }
        response = ""
        try:
            response = self.post_curl(self.url, params)
            for item in response['users']:
                id = item['id']
                return id
        except:
            return "Hatalı getUserId Fonksiyonu"

    def post_curl(self, url, params):
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        req = requests.post(url, headers=headers, data=params)
        result = req.json()
        return result

    def enrol_course(self,user):
        __user_id = self.get_user_id(user)
        params = {
            'wstoken': self.token,
            'wsfunction': 'enrol_manual_enrol_users',
            'moodlewsrestformat': 'json',
            'enrolments[0][roleid]': int(self.rolID),
            'enrolments[0][userid]': int(__user_id),
            'enrolments[0][courseid]': int(self.lessonID),
        }

        try:
            response = self.post_curl(self.url, params)
            print(response)
        except:
            print("Hatalı enrolCourse Fonksiyonu")

        return response

    def cohort_add(self,user):
        __user_id = self.get_user_id(user)
        params = {
            'wstoken': self.token,
            'wsfunction': 'core_cohort_add_cohort_members',
            'moodlewsrestformat': 'json',
            'members[0][cohorttype][type]': 'id',
            'members[0][usertype][type]': 'id',
            'members[0][cohorttype][value]': '18',
            'members[0][usertype][value]': f'{__user_id}'
        }
        try:
            response = self.post_curl(self.url, params)
            print(response)
        except:
            print("Hatalı enrolCourse Fonksiyonu")

        return response


if __name__ == '__main__':  

    file = open('data.txt', 'r')
    arr = file.readlines()
    file.close()
    user_list = []

    for item in arr:
        user_list.append(item.replace('\n',''))


    script = Main(12427, 5, user_list)
