import urllib.request
import ssl
import os
 
# URL to access
url = "https://4.237.224.16"
 
# Certificate file (optional, since we disable verification)
cert_file = r"C:/Fortinet_CA_SSL.cer"
 
# Ensure the certificate file exists (optional check)
if not os.path.exists(cert_file):
    print(f"Warning: Certificate file '{cert_file}' not found. Proceeding without it.")
 
# Create a custom SSL context with the most lenient settings
context = ssl.create_default_context()
context.check_hostname = False  # Must disable before CERT_NONE
context.verify_mode = ssl.CERT_NONE  # Disable all certificate checks
 
# (Optional) Load the certificate (but verification is disabled)
try:
    context.load_verify_locations(cert_file)
except Exception as e:
    print(f"Warning: Could not load certificate (proceeding anyway): {e}")
 
# Make the request
try:
    response = urllib.request.urlopen(url, context=context)
    print("Success! Response:")
    print(response.read().decode())
except Exception as e:
    print(f"Error accessing {url}: {e}")