from peewee import Model, UUIDField, TextField, TimestampField, ForeignKeyField
from general.clients.postgres_db_pw import push_console_db_connection

class BaseModel(Model):
    class Meta:
        database = push_console_db_connection()

class PushConsoleUsersPW(BaseModel):
    user_id = UUIDField(primary_key=True, column_name='id')
    email = TextField(column_name='email')
    role = TextField(column_name='role')
    created_at = TimestampField(column_name='created_at')
    company_name = TextField(column_name='company_name')
    salt = TextField(column_name='salt')
    password_hash = TextField(column_name='password_hash')

    class Meta:
        table_name = 'users'

class PushConsoleProjectsPW(BaseModel):
    project_id = UUIDField(primary_key=True, column_name='id')
    name = TextField(column_name='name')
    created_at = TimestampField(column_name='created_at')
    updated_at = TimestampField(column_name='updated_at')
    creator = ForeignKeyField(PushConsoleUsersPW, column_name='creator_id')

    class Meta:
        table_name = 'projects'

class PushConsoleAppsPW(BaseModel):
    app_id = UUIDField(primary_key=True, column_name='id')
    name = TextField(column_name='name')
    package_name = TextField(column_name='package_name')
    created_at = TimestampField(column_name='created_at')
    updated_at = TimestampField(column_name='updated_at')
    project = ForeignKeyField(PushConsoleUsersPW, column_name='project_id')

    class Meta:
        table_name = 'apps'

class PushConsoleTokensPW(BaseModel):
    value = TextField(column_name='value')
    created_at = TimestampField(column_name='created_at')
    project = ForeignKeyField(PushConsoleUsersPW, column_name='project_id')

    class Meta:
        table_name = 'service_tokens'