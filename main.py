import streamlit as st
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import requests
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# login to cloudinary and get your key from here - https://console.cloudinary.com/pm/c-a8f7a41e4832cf677e6d5fe5a83cff/getting-started


# Configure Cloudinary
cloudinary.config(
    cloud_name="ddqt2h08a",
    api_key="812972373143139",
    api_secret="lOIlsazZF6_Cry5l1Ta5Y0INf9w",
    secure=True
)

# Streamlit app for restoring images using Cloudinary's Generative Restore
st.title("Image Restoration with Cloudinary's Generative Restore")

# Upload image
uploaded_file = st.file_uploader("Upload an image to restore", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the file into bytes
    image_bytes = uploaded_file.getvalue()

    # Get the file extension
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Display uploaded image
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

    # Generate button for restoration
    if st.button("Restore Image"):
        try:
            # Upload the image to Cloudinary
            upload_result = cloudinary.uploader.upload(image_bytes)
            public_id = upload_result['public_id']

            # Generate the restoration image URL
            restore_effect = "gen_restore"
            restored_image_url, _ = cloudinary_url(
                f"{public_id}{file_extension}",
                effect=restore_effect
            )

            logging.info(f"Generated URL: {restored_image_url}")

            # Fetch the transformed image from the generated URL
            response = requests.get(restored_image_url)

            if response.status_code == 200:
                # Display images
                st.subheader("Compare Images")
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(image_bytes, caption="Original Image", use_column_width=True)
                with col2:
                    st.image(response.content, caption="Restored Image", use_column_width=True)
            else:
                st.error(f"Failed to fetch the restored image. Status code: {response.status_code}")
                logging.error(f"Failed to fetch image. Status code: {response.status_code}")
                logging.error(f"Response content: {response.content}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.exception("An error occurred during image processing")

        # Display the generated URL for debugging
        st.text(f"Debug - Generated URL: {restored_image_url}")
