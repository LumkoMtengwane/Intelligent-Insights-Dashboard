from azure.storage.blob import BlobServiceClient
import os
import uuid
from datetime import datetime


def _get_blob_container():
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "images")
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()
    return container_client



def upload_image(file_path, name):
    try:
        container = _get_blob_container()
        with open(file_path, "rb") as data:
            container.upload_blob(name, data, overwrite=True)
        return {"success": True, "message": f"Uploaded {name} successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def upload_chart(fig, chart_name=None):
    """Export a Plotly figure to PNG and upload it to Azure Blob Storage."""
    try:
        img_bytes = fig.to_image(format="png", width=1200, height=600)

        if chart_name is None:
            chart_name = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.png"
        elif not chart_name.endswith(".png"):
            chart_name += ".png"

        container = _get_blob_container()
        container.upload_blob(chart_name, img_bytes, overwrite=True)

        account_name = os.getenv("AZURE_STORAGE_BLOB_NAME", "lumkoaiblob")
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "images")
        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{chart_name}"

        return {"success": True, "url": blob_url, "name": chart_name}
    except Exception as e:
        return {"success": False, "error": str(e)}
