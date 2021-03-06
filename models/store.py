from db import db

class StoreModel(db.Model):  #the things in this class are saving and retrieving from a db, creates a mapping between db and obj
    __tablename__='stores'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))

    items=db.relationship("ItemModel",lazy='dynamic') #since a relationship is created , whenever a store model is created an object in the item model db is created that matches the store id. So to avoid it 'lazy' is used.
     

    def __init__(self,name):
        self.name=name
        
        
    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]} # .all is used because when lazy is used self.items is not a list of items, it is a query builder that has the ability to look into the items table

    @classmethod
    def find_by_name(cls,name):
       return cls.query.filter_by(name=name).first() #returns first row with the matching name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()