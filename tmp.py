from Course import *

session = Session()
get_session(session)

Course.loadByCourse("CST31208", "184020-002", session).select(session)