import qrcode
import os
import firebase_admin
from firebase_admin import credentials ,firestore

cred = credentials.Certificate("flowius-project.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

collection_ref = db.collection('Project').document('mXAIgIpVQuiSycXr0s2V').collection('HouseHold')
docs = collection_ref.stream()
data_list = []
key_list=[]
data={}
for doc in docs:
    data_list.append(doc.id)
    if 'ownerName' in doc.to_dict():
        key_list.append(doc.to_dict()['ownerName'])
def generate_qr_codes(key,data, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate QR codes for each data string in the list
    for  key, data in  zip(key,data):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate the QR code image
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        img.save(os.path.join(output_dir, f"{key}{data}.png"))

# Example usage:

output_dir = "qr_codes_uat_new"
generate_qr_codes(key_list,data_list, output_dir)
