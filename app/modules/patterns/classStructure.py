from create_app import db
from typing import Sequence
from datetime import datetime, timedelta, date
import logging, textwrap
logging.basicConfig(level=logging.DEBUG)

class PatternsClass(db.Model):
    __tablename__ = 'patterns'
    
    
    id                  = db.Column(db.Integer,     primary_key=True)
    patterns            = db.Column(db.String(25),  nullable=False)
    history             = db.Column(db.String(51),  nullable=True)
    multipler           = db.Column(db.String(2),   nullable=False)
    quantity            = db.Column(db.Integer,     default=0)
    average             = db.Column(db.Integer,     default=0)
    best_record_id      = db.Column(db.Integer,     nullable=True)
    datetime            = db.Column(db.DateTime,    default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    datetime_update     = db.Column(db.DateTime,    nullable=True)
    
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'patterns'        : self.patterns,
            'history'         : self.history,
            'multipler'       : self.multipler,
            'quantity'        : self.quantity,
            'average'         : self.average,
            'best_record_id'  : self.best_record_id,
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update
        }
        
        
    @classmethod
    def getPatternsPut(cls, id):
        patterns = PatternsClass.query.filter_by(id=id).first()
        return patterns
    
    @classmethod
    def getPatternsMultiple(cls, patterns, multipler):
        patterns = PatternsClass.query.filter_by(
            multipler=multipler, 
            patterns=patterns
        ).first()
        
        return patterns.serialize
    
    @classmethod
    def getPatternsMultiplePut(cls, patterns, multipler):
        patterns = PatternsClass.query.filter_by(
            multipler=multipler, 
            patterns=patterns
        ).first()
        
        return patterns
    
    @classmethod
    def getPatternsLast(cls, multipler):
        patterns = PatternsClass.query.filter(
            PatternsClass.datetime_update.isnot(None),
            PatternsClass.multipler == multipler
        ).order_by(PatternsClass.datetime_update.desc()).first()
        
        if patterns is not None:
            return patterns.serialize
        
        return patterns
    
    @classmethod
    def getData(cls, **filters):
        patterns: Sequence[PatternsClass] = PatternsClass.query.filter_by(**filters).all()
        response = list()
        for pattern in patterns:
            aux = {
                'id'             : pattern.id,
                'patterns'       : '-'.join(textwrap.wrap(pattern.patterns , 5)),
                'patternsVector' : textwrap.wrap(pattern.patterns , 5),
                'quanty'         : pattern.quantity,
                'average'        : pattern.average
            }
            
            response.append(aux)
            
        return response
    
    @classmethod
    def getPatternsLike(cls, multipler, search):
        patterns = PatternsClass.query.filter(
            PatternsClass.patterns.like(search),
            PatternsClass.multipler == multipler
        ).order_by(PatternsClass.quantity.desc()).limit(3).all()
        
        response = list()
        for pattern in patterns:
            aux = {
                'id'             : pattern.id,
                'patterns'       : '-'.join(textwrap.wrap(pattern.patterns , 5)),
                'patternsVector' : textwrap.wrap(pattern.patterns , 5),
                'quantity'       : pattern.quantity,
                'average'        : pattern.average
            }
            
            response.append(aux)
            
        return response
    
    @classmethod
    def putData(cls, data):
        db.session.commit()
        return data.serialize
        
    @classmethod
    def post(cls, **cols):
        patterns = cls(**cols)
        db.session.add(patterns)
        db.session.commit()
        return patterns.serialize
    
    @classmethod
    def postData(cls, **cols):
        patterns = PatternsClass.query.filter_by(patterns=cols["patterns"], multipler=cols["multipler"]).first()
        if patterns is not None:
            return patterns.serialize
        
        return cls.post(**cols)
    
    
class PatternsHistoryClass(db.Model):
    __tablename__ = 'patterns_history'
    
    
    id                  = db.Column(db.Integer,     primary_key=True)
    patterns_id         = db.Column(db.String(25),  nullable=False)
    history             = db.Column(db.String(51),  nullable=True)
    multipler           = db.Column(db.String(2),   nullable=False)
    quantity            = db.Column(db.Integer,     default=0)
    average             = db.Column(db.Integer,     default=0)
    datetime            = db.Column(db.DateTime,    default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'patterns_id'     : self.patterns_id,
            'history'         : self.history,
            'multipler'       : self.multipler,
            'quantity'        : self.quantity,
            'average'         : self.average,
            'datetime'        : self.datetime,
        }
        
    @classmethod
    def getPatternsIdHistory(cls, patterns_id):
        patternsHistory = PatternsHistoryClass.query.filter(
            PatternsHistoryClass.history.isnot(None),
            PatternsHistoryClass.patterns_id == patterns_id
        ).order_by(PatternsHistoryClass.quantity.desc()).limit(3).all()
        
        response = list()
        for patternHistory in patternsHistory:
            aux = {
                'id'             : patternHistory.id,
                'prev'           : '-'.join(textwrap.wrap(patternHistory.history.split('-')[0] , 5)), 
                'vectorPrev'     : textwrap.wrap(patternHistory.history.split('-')[0] , 5),
                'post'           : '-'.join(textwrap.wrap(patternHistory.history.split('-')[1] , 5)), 
                'vectorPost'     : textwrap.wrap(patternHistory.history.split('-')[1] , 5),
                'quantity'       : patternHistory.quantity,
            }

            response.append(aux)
            
        return response
    
        
    @classmethod
    def getPatternsIdHistoryLast(cls, multipler, search):
        patterns = PatternsHistoryClass.query.filter(
            PatternsHistoryClass.history.like(search),
            PatternsHistoryClass.multipler == multipler
        ).order_by(PatternsHistoryClass.quantity.desc()).limit(3).all()
        
        response = list()
        for pattern in patterns:
            aux = {
                'id'             : pattern.id,
                'history'        : pattern.history,
                'quantity'       : pattern.quantity,
            }
            
            response.append(aux)
            
        return response