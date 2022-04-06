#  Copyright (c) Message4U Pty Ltd 2014-2022
#
#  Except as otherwise permitted by the Copyright Act 1967 (Cth) (as amended from time to time) and/or any other
#  applicable copyright legislation, the material may not be reproduced in any format and in any way whatsoever
#  without the prior written consent of the copyright owner.
import os

import psycopg2


def get_db_password() -> str:
    return os.getenv('DB_PASSWORD')


def get_db_endpoint() -> str:
    return os.getenv('DB_ENDPOINT')


def get_db_user() -> str:
    return os.getenv('DB_USER')


def get_connection():
    return psycopg2.connect(
        database="pbs-db",
        user=get_db_user(),
        password=get_db_password(),
        host=get_db_endpoint(),
        port='5432'
    )


def insert_new_column(style_id, booking_id, original_image_url, edited_image_url):
    conn = None
    result = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = '''
            insert into style_tracking (style_id, booking_id, original_image_url, edited_image_url)
            values (%s, %s, %s, %s);
        '''
        cur.execute(query, (style_id, booking_id, original_image_url, edited_image_url))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:  # pylint: disable=broad-except
        print(error)
    if conn is not None:
        conn.close()
    return result
