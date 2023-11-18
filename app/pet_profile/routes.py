from app.pet_profile import bp
from flask import render_template, request, session
from flask_login import login_required, current_user
import os   
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from werkzeug.utils import secure_filename
from openai import OpenAI


connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# connect_str = ""
container_name = "photos"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

# client = OpenAI(api_key="")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@bp.route('/mypet', methods=["GET", "POST"])
@login_required
def pet_profile():
    blob_name = "pet_" + secure_filename(session['email'])
    file_url = get_blob_url(blob_name)
    pet_data = {"type": "", "breed": ""}

    if request.method == "POST":
        file = request.files["pet_photo"]
        if file:
            file.filename = blob_name# + file.filename.split(".")[-1]
            upload_to_azure(file)
            #file_url = get_blob_url(secure_filename(file.filename))

        try:
            if file_url:
                response = client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Just tell me the type and the breed of the animal in the photo only in this format: {'type': 'type', 'breed': 'breed'}"},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"{file_url}",
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )

            pet_data = eval(response.choices[0].message.content)
            set_blob_meta_data(pet_data, blob_name)

        except Exception as e:
            print(e)

    temp = get_blob_meta_data(blob_name)
    print(temp)
    if temp:
        pet_data = temp

    return render_template('PetProfile.html', file_url=file_url, pet_data=pet_data)


def upload_to_azure(file):
    container_client = blob_service_client.get_container_client(container=container_name)
    if hasattr(file, "filename"):
        blob_name = secure_filename(file.filename)
    else:
        blob_name = secure_filename(file)
    
    blob_client = container_client.get_blob_client(blob_name)
    try:
        blob_client.delete_blob()
    except ResourceNotFoundError:
        pass

    blob_client = container_client.get_blob_client(blob_name)
    try:
        blob_client.upload_blob(file)
        blob_properties = blob_client.get_blob_properties()
        blob_properties.cache_control = "max-age=0.01"
    except Exception as e:
        print(e)

def get_blob_url(blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client.url

def set_blob_meta_data(meta_data, blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.set_blob_metadata(meta_data)

def get_blob_meta_data(blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    try:
        metadata = blob_client.get_blob_properties().metadata
        return metadata
    except Exception as e:
        return None
    