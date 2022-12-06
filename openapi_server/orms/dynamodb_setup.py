from openapi_server.orms.user import DbUser

if not DbUser.exists():
    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
