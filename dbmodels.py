import ulid
from sqlalchemy import Column, Integer, String, DateTime, Index, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UnverifiedCodes(Base):
    __tablename__ = 'unverified_codes'

    id = Column(String(26), primary_key=True, unique=True)
    user = Column(String(50), nullable=False)
    code = Column(String(8), nullable=False)
    r_batch = Column(String(50), index=True, nullable=False)
    time = Column(DateTime)

    __table_args__ = (
        Index('ix_code_user', 'code', 'user'),
    )

    def __init__(self, user, code, time, r_batch=None):
        self.id = str(ulid.new())
        self.user = user
        self.code = code
        self.time = time
        self.r_batch = r_batch

    def get(self, key, default=None):
        return getattr(self, key, default)


class VerifiedCodes(Base):
    __tablename__ = 'verified_codes'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(26), index=True, unique=True)
    user = Column(String(50), nullable=False, index=True)
    code = Column(String(8), nullable=False, index=True)
    r_batch = Column(String(50))
    time = Column(DateTime)
    b_email = Column(String(50))
    b_name = Column(String(50))
    b_phone = Column(String(15))
    b_source = Column(String(50))
    b_city = Column(String(100))
    v_time = Column(DateTime, index=True)

    def __init__(self, id, user, code, b_email, b_name, b_phone, b_source, r_batch, v_time=None, time=None,
                 b_city=None):
        self.id = id
        self.user = user
        self.code = code
        self.r_batch = r_batch
        self.time = time
        self.b_email = b_email
        self.b_name = b_name
        self.b_phone = b_phone
        self.b_source = b_source
        self.v_time = v_time
        self.b_city = b_city

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __repr__(self):
        return f"VerifiedCodes(id={self.id!r}, user={self.user!r}, code={self.code!r}, " \
               f"r_batch={self.r_batch!r}, p_name={self.p_name!r}, p_batch={self.p_batch!r}, " \
               f"time={self.time!r}, b_email={self.b_email!r}, b_name={self.b_name!r}, " \
               f"b_phone={self.b_phone!r}, b_source={self.b_source!r}, b_city={self.b_city!r}, " \
               f"v_time={self.v_time!r})"


class BatchRequest(Base):
    __tablename__ = 'batch_request'

    id = Column(String(26), primary_key=True)
    user = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    p_name = Column(String(200))
    p_batch = Column(String(200))

    def __init__(self, id, user, count, time, p_name=None, p_batch=None):
        self.id = id
        self.user = user
        self.count = count
        self.time = time
        self.p_name = p_name
        self.p_batch = p_batch
