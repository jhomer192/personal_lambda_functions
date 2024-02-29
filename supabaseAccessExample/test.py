import os
from supabase import create_client, Client
#heres supabase python, I installed as pip install supabase --user
#https://www.redswitches.com/blog/set-environment-variables-in-macos/#:~:text=To%20set%20a%20permanent%20environment,can%20open%20the%20file%20~%2F.
#set them then restart computer
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
#in order to authenticate we have to create user accounts
email: str = os.environ.get("SUPABASE_EMAIL")
password: str = os.environ.get("SUPABASE_PASSWORD")
response = supabase.auth.sign_in_with_password({"email" : email, "password": password})
#supabase has sql query creator on website that uses AI, you can convert those to the python version



response = supabase.table('Client').select("*").execute()
print(response)