import socket
import ssl
from OpenSSL import SSL


def get_supported_ssl_versions(hostname, port=443):
    supported_versions = []
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Retrieve the negotiated protocol version
                protocol_version = ssock.version()
                supported_versions.append(protocol_version)

    except ssl.SSLError as e:
        raise ssl.SSLError(f"SSL Error: {e}")

    except socket.gaierror as e:
        raise socket.gaierror(f"Connection Error: {e}")

    return supported_versions


def get_ssl_certificate(hostname, port=443):
    try:
        # Create an SSL/TLS connection
        context = SSL.Context(SSL.TLSv1_2_METHOD)
        ssock = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        ssock.set_tlsext_host_name(hostname.encode())
        ssock.connect((hostname, port))
        ssock.do_handshake()

        # Retrieve the certificate
        cert = ssock.get_peer_certificate()

        # Close the SSL/TLS connection
        ssock.shutdown()
        ssock.close()

        return cert

    except ssl.SSLError as e:
        raise ssl.SSLError(f"SSL Error: {e}")

    except socket.gaierror as e:
        raise socket.gaierror(f"Connection Error: {e}")

    return None


def print_ssl_info(supported_versions, cert_info):
    if supported_versions:
        print("SSL/TLS Protocols:")
        for version in supported_versions:
            print(f"Version: {version}")

    if cert_info:
        print("SSL Certificate:")
        print(f"Signature Algorithm: {cert_info.get_signature_algorithm().decode()}")
        print(f"RSA Key Strength:    {cert_info.get_pubkey().bits()}")


def scan_website_ssl(domain):
    try:
        supported_versions = get_supported_ssl_versions(domain)
        cert_info = get_ssl_certificate(domain)

        print("SSL/TLS Protocols:")
        for version in supported_versions:
            print(f"Version: {version}")

        if cert_info:
            print("\nSSL Certificate:")
            print(f"Signature Algorithm: {cert_info.get_signature_algorithm().decode()}")
            print(f"RSA Key Strength:    {cert_info.get_pubkey().bits()}")

        return supported_versions, cert_info

    except (ssl.SSLError, socket.gaierror) as e:
        print(f"Error: {e}")
        return None, None


if __name__ == "__main__":
    domain = input("Enter the URL to scan (e.g., example.com): ")
    scan_website_ssl(domain)
