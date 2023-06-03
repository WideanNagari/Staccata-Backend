from app.model.users import Users
from app.model.faq import FAQ
from app.model.reports import Reports
from app.model.performances import Performances

from app import app, db
from app.model import response

from faker import Faker
import random

@app.route('/api/seeds/<records>', methods=['POST'])
def seed(records):
    faker = Faker()
    
    try:
        user = Users(username="guest", email="guest@ggmail.com", password="123")
        user.setPassword("123")
        arr_username = []
        arr_username.append("guest")
        db.session.add(user)
        for i in range(int(records)):
            username = faker.user_name()
            password = "123"
            email = (username.split()[0])+"@ggmail.com"
            piano = random.randint(0, 10)
            guitar = random.randint(0, 10)
            report = random.randint(0, 10)

            user = Users(username=username, email=email, password=password, file_converted_piano=piano, file_converted_guitar=guitar, report_sent=report)
            user.setPassword(password)
            db.session.add(user)
            arr_username.append(username)

        db.session.commit()

        for i in range(int(records)):
            question = faker.sentence()
            answer = faker.sentence()

            faq = FAQ(question=question, answer=answer)
            db.session.add(faq)
        db.session.commit()

        ids = Users.query.with_entities(Users.id).all()
        arr_id = []
        for i in ids:
            arr_id.append(i[0])

        for i in range(int(records)):
            title = faker.sentence()
            description = faker.sentence()
            reporter = random.randint(0, len(arr_id)-1)
            
            report = Reports(title=title, description=description, reporter=arr_id[reporter], reporter_name=arr_username[reporter])
            db.session.add(report)
        db.session.commit()

        arr_music = ["Piano", "Guitar"]
        for i in range(int(records)):
            like_status = random.randint(0, 1)
            u = random.choice(arr_id)
            title2 = faker.sentence()
            duration = random.randint(10, 200)
            initial = random.randint(0, 1)
            target = int(not initial)
            link="x"

            performance = Performances(user=u, title=title2, duration=duration, initial=arr_music[initial], target=arr_music[target], 
                                        gdrive_link=link, like_status=like_status)
            db.session.add(performance)
        db.session.commit()

        return response.success({}, "success")
    except Exception as e:
        return response.badRequest({}, str(e))