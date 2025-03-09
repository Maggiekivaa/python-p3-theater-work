from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import Base  

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String(100), nullable=False)

    auditions = relationship('Audition', backref='role', lazy='dynamic')

    def actors(self):
        """Returns a list of actors for this role"""
        return [audition.actor for audition in self.auditions]

    def locations(self):
        """Returns a list of locations for this role's auditions"""
        return [audition.location for audition in self.auditions]

    def lead(self):
        """Returns the first hired actor for the role or a message if not hired"""
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0].actor
        return 'no actor has been hired for this role'

    def understudy(self):
        """Returns the second hired actor for the role or a message if not hired"""
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1].actor
        return 'no actor has been hired for understudy for this role'


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def call_back(self):
        """Changes the hired status to True (hiring the actor)"""
        self.hired = True
        from . import db  
        db.session.commit()
