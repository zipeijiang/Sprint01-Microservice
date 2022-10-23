import pymysql
import random
import os


class UserInfo:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        conn = pymysql.connect(
            user='admin',
            password='1145140424',
            host='sprint1cs6156.cne7f5zyjwgm.us-east-1.rds.amazonaws.com',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_id(id):

        sql = """
        SELECT * FROM user.user where id=%s
        """
        conn = UserInfo._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result
    
    @staticmethod
    def login(email, pw):

        action = """
        SELECT * FROM user.user WHERE password=%s AND email=%s
        """
        conn = UserInfo._get_connection()
        cur = conn.cursor()
        cur.execute(action,(pw,email))
        response = cur.fetchone()

        if response!=None:
            return {'status':200, 'body':{
                            "id":response['id'],
                            "message":"login success"
                    }}
        else:
            return {'status':400, 'body':{
                            "message":"incorrect email or password"
                    }}

    @staticmethod
    def signUp(lname, fname, email, password, phone):

        if (len(password)<6):
            return {'status':400, 'body':{
                                "message":"password should be at least 6 characters long"
                            }}
        action_check_uniqueEM = "SELECT * FROM user.user WHERE email=%s"
        action_check_uniqueID = "SELECT * FROM user.user WHERE id=%s"
        action_insert_new_record = 'INSERT INTO user.user VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIME(), CURRENT_TIME())'
        action_get_id_by_email = "SELECT * FROM user.user WHERE email=%s"

        conn = UserInfo._get_connection()
        cur = conn.cursor()

        id = lname.lower() + str(random.randint(0, 10)) +fname.lower()
        while(True):    # check id uniqueness
            cur.execute(action_check_uniqueID, (id)) 
            response = cur.fetchall() 
            if len(response)>0:
                id = lname.lower() + str(random.randint(100, 1000)) +fname.lower()
            else:
                break

        cur.execute(action_check_uniqueEM, (email)) 
        response = cur.fetchone()
        if response!= None: 
            return {'status':400, 'body':{
                            "message":"email already exists"
                        }}

        cur.execute(action_insert_new_record, (id, lname, fname, email, password, phone))
        conn.commit()
        cur.execute(action_get_id_by_email, (email))
        
        response = cur.fetchone()
        return {'status':200, 'body':{
                            "id":response['id'],
                            "message":"create user success"
                    }}

    @staticmethod
    def updatePassword(id, new, old):
        
        action0 = "SELECT * FROM user.user WHERE id=%s"
        action1 = "UPDATE user.user SET password=%s WHERE id=%s"

        conn = UserInfo._get_connection()
        cur = conn.cursor()

        cur.execute(action0, (id))
        res = cur.fetchone()
        if res==None:  
            return {'status':400, 'body':{
                        "message":"user does not exist"
                    }}
        oldpassword = res['password'] 
        if oldpassword != old: 
            return {'status':400, 'body':{
                        "message":"incorrect password"
                    }}
        cur.execute(action1, (new, id))
        conn.commit()
        return {'status':200, 'body':{
                        "message":"update password success"
                    }}
