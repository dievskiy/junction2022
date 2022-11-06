data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../function-sign"
    output_path = "../function.zip"
}

resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name
}

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "function" {
    name                  = "function-trigger-on-gcs"
    description           = "DocuSign API function"
    runtime               = "python310"

    available_memory_mb   = 256
    trigger_http                 = true
    https_trigger_security_level = "SECURE_ALWAYS"
    timeout                      = 60

    # Get the source code of the cloud function as a Zip compression
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.zip.name

    entry_point           = "send_nda_email"

    environment_variables = {
      PRIVATE_KEY = var.private_key
    }
    #event_trigger {
    #    event_type = "google.storage.object.finalize"
    #    resource   = "${var.project_id}-input"
    #}
}
