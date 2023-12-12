from app.pet_profile import bp
from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from werkzeug.utils import secure_filename
from openai import OpenAI
from app.models.petProfile import PetProfile
from app.extensions import db

# Setting up connection string and blob service client for Azure Blob Storage
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = "photos"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

# Setting up OpenAI client with API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Route for handling profile info submission
@bp.route('/submit_pet_profile', methods=['POST'])
@login_required
def submit_pet_profile():
    # Form submission handling
    name = request.form.get('name')
    pet_type = request.form.get('type')
    age = request.form.get('age')
    breed = request.form.get('breed')
    weight = request.form.get('weight')

    # Convert age and weight to the appropriate type and handle potential conversion errors
    try:
        age = int(age)
        weight = float(weight)
    except ValueError:
        flash('Invalid input for age or weight. Please enter a number.', 'error')
        return redirect(url_for('pet_profile.pet_profile'))  # Make sure this is the correct function name for redirect

    # Check if the current user already has a pet profile
    existing_pet_profile = PetProfile.query.filter_by(user_email=session['email']).first()

    if existing_pet_profile:
        # Update existing record
        existing_pet_profile.name = name
        existing_pet_profile.age = age
        existing_pet_profile.weight = weight
        existing_pet_profile.pet_type = pet_type
        existing_pet_profile.breed = breed
        db.session.commit()
        flash('Pet profile updated successfully!', 'success')
    else:
        # Create a new PetProfile instance and save it to the database
        new_pet_profile = PetProfile(name=name, pet_type=pet_type, age=age, breed=breed, weight=weight,
                                     user_email=session['email'])
        db.session.add(new_pet_profile)
        db.session.commit()
        flash('Pet profile created successfully!', 'success')

    return redirect(url_for('pet_profile.pet_profile'))


# Route for handling pet profile page, requiring login
@bp.route('/mypet', methods=["GET", "POST"])
@login_required
def pet_profile():
    # Defining the blob name using the user's email for uniqueness
    blob_name = "pet_" + secure_filename(session['email'])
    file_url = get_blob_url(blob_name)  # Retrieve the URL of the pet image from Azure Blob Storage
    pet_data = {"type": "", "breed": ""}  # Initialize pet data dictionary

    # Retrieve existing metadata if available
    temp = get_blob_meta_data(blob_name)
    if temp:
        pet_data = temp

    # Query for the current user's pet profile
    user_pet_profile = PetProfile.query.filter_by(user_email=session['email']).first()

    # Check if a new image was uploaded and recognized successfully
    if request.method == "POST" and 'pet_photo' in request.files:
        file = request.files["pet_photo"]
        if file:
            file.filename = blob_name
            upload_to_azure(file)
            try:
                if file_url:
                    # Using OpenAI's image recognition service to determine pet type and breed
                    response = client.chat.completions.create(
                        model="gpt-4-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text",
                                     "text": "Just tell me the type and the breed of the animal in the photo only in this format: {'type': 'type', 'breed': 'breed'}"},
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

                new_pet_data = eval(response.choices[0].message.content)
                set_blob_meta_data(new_pet_data, blob_name)

                # If a pet profile exists, update it with the new recognition data
                if user_pet_profile:
                    user_pet_profile.pet_type = new_pet_data['type']
                    user_pet_profile.breed = new_pet_data['breed']
                    db.session.commit()

                # Also update the pet_data dictionary to reflect the new values
                pet_data['type'] = new_pet_data['type']
                pet_data['breed'] = new_pet_data['breed']

            except Exception as e:
                print(e)

    # If a pet profile exists, use it to pre-populate the form
    if user_pet_profile:
        # Update pet_data with existing profile info, if not already updated by new recognition data
        pet_data.setdefault('name', user_pet_profile.name)
        pet_data.setdefault('type', user_pet_profile.pet_type)
        pet_data.setdefault('age', user_pet_profile.age)
        pet_data.setdefault('breed', user_pet_profile.breed)
        pet_data.setdefault('weight', user_pet_profile.weight)
        

    return render_template('PetProfile.html', file_url=file_url, pet_data=pet_data)


# Function to upload files to Azure Blob Storage
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


# Function to get the URL of a blob in Azure Blob Storage
def get_blob_url(blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client.url


# Function to set metadata for a blob in Azure Blob Storage
def set_blob_meta_data(meta_data, blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.set_blob_metadata(meta_data)


# Function to get metadata of a blob from Azure Blob Storage
def get_blob_meta_data(blob_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    try:
        metadata = blob_client.get_blob_properties().metadata
        return metadata
    except Exception as e:
        return
