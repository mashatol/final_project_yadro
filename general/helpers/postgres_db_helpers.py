import allure

from general.clients.postgres_db import execute_postgres_select_all, execute_postgres_non_select

@allure.step("Get user by id from postgres")
def get_user_by_id_from_pg(user_id):
    query = f"""
        SELECT * 
        FROM users
        WHERE id = '{user_id}';
    """
    result = execute_postgres_select_all(query=query)

    return result

@allure.step("Get data table 'projects' by user_id from postgres")
def get_projects_by_user_id_from_pg(user_id):
    query = f"""
        SELECT *
        FROM projects
        WHERE creator_id = '{user_id}';
    """
    result = execute_postgres_select_all(query=query)

    return result

@allure.step("Get project by name from postgres")
def get_project_by_name_from_pg(project_name):
    query = f"""
        SELECT *
        FROM projects
        WHERE name = '{project_name}';
    """
    result = execute_postgres_select_all(query=query)

    return result

@allure.step("Get count of projects by user_id from postgres")
def get_count_projects_by_user_id_from_pg(user_id):
    query = f"""
         SELECT COUNT(*) as count
         FROM projects
         WHERE creator_id = '{user_id}';
    """
    result = execute_postgres_select_all(query=query)
    return result

@allure.step("Get project by id from postgres")
def get_project_by_id_from_pg(project_id):
    query = f"""
         SELECT *
         FROM projects
         WHERE id = '{project_id}';
    """
    result = execute_postgres_select_all(query=query)
    return result

@allure.step("Delete project by id from postgres")
def delete_project_by_id_from_pg(project_id):
    query = f"""
         DELETE
         FROM projects
         WHERE id = '{project_id}';
    """
    execute_postgres_non_select(query=query)
