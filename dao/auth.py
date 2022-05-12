from dao.model.user import User


class AuthUserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(User).filter(User.id == item_id).one_or_none()
        return item

    def get_one_by_username(self, item_data):
        username = item_data.get("username")
        item = self.session.query(User).filter(User.username == username).one_or_none()
        return item

    def get_all(self):
        items = self.session.query(User).all()
        return items

    def create(self, item_data):
        new_data = User(**item_data)
        self.session.add(new_data)
        self.session.commit()
        return new_data

    def update(self, new_data):
        item_id = new_data.get("id")
        item = self.session.query(User).filter(User.id == item_id).update(new_data)
        self.session.commit()

    def delete(self, item_id):
        item = self.get_one(item_id)
        self.session.delete(item)
        self.session.commit()

