from create_app import db
from typing import Sequence

class Setting(db.Model):
    __tablename__ = 'setting'
    
    
    id        = db.Column(db.Integer, primary_key=True)
    code      = db.Column(db.String(80), nullable=False)
    value     = db.Column(db.String(256),nullable=True)
    json_data = db.Column(db.String(128), nullable=True)
    datetime  = db.Column(db.TIMESTAMP, default=False)
    
    # status = db.relationship(BankStatusModel, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'        : self.id,
            'code'      : self.code,
            'value'     : self.value,
            'json_data' : self.json_data,
            'datetime'  : self.datetime
        }
        
        
    def getCode(param):
        settings = Setting.query.filter_by(code=param).first()
        return settings
    
    def getData(**filters):
        settings: Sequence[Setting] = Setting.query.filter_by(**filters).all()
        return [setting.serialize for setting in settings]
    
    def putData(data):
        db.session.commit()