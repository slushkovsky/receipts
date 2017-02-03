from oauth2client import service_account

CREDENTIALS = {
  "_module": "",
  "_class": "",
  "type": "service_account",
  "project_id": "checkstar-152822",
  "private_key_id": "ce2b89e475eb687c421e800d22d642171850aae1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCmqht4GPQO+58n\n9qc1ohA+Hk8Wkwgzoj4sfyYzx9CdQ8LyUv22tk7qKv9Sr0nP52eegYKpvBFGUHAJ\nz/GQR58jrsN9QcSC5r2Yz9PVGBxHhdOLdTxRlrj76jLKjTIVLNT9cq5liUwq0cem\nYghLhH/F1WOidYs1QDs7pg3szvBMP3evfI8pB0okC8viUDgKsGp7GgWIY1tXuWwy\n6OtT2+6tRz4a5H+l/C7sdVzVYchkjBz9ZRO2nvD38Cct73pBSUGKQ7wNzo0OLvXW\nCT6J4KjsmuwwRU9LY5rGHiHfw0y/LN13Lq4Ch7e6+yN3/AzoZ09idJIMkNWMs+Vx\nIElI+BD7AgMBAAECggEAR2qvOKhgtKboDWTpQ9c9ZJDyTPcWVaHZSJH3mcquvyUR\nPWuIoqm+aSOhoxnP5FIBme9fQUKAmIPRbrL3jV7Td6PkyyDKh1k+t2OfHzokrBVR\nj/ndrgyLGg/CUf9tDZvXbP+ecY4C4HpiNg7eBRYy9mA5QJ1j2J68gxPl9aq7V8BN\njW4F0IpE2tm6IjwS+ia9omhHePJ4e2Y4lXwmh8BFFeNwZrpRfbyfrZupkm7Rt735\nDn/L1VfaQg5j1EvZ0fTnGy+98JBfHuJ8rBKXegr8Yrl1pZv8VOtTIwUHv2a+M80k\n/hwdMxE+DhNzGiD7p7tx6O+T+DgveR0T2hUXoWj6KQKBgQDQnSpzmDVrNMMbGovT\n2U23wyXqx4PUrlmmuIt9mki21XA0b8Gt6DB1uswCdJfQ39MEaLw+MdMYZVqwpG0B\nJOJqpbnk+TCKWayUey2ws5OwXQV7LhsiAHaUuN3Rw5Nt8F4jUR5xtWTSkm8nrleR\n5/v0lrsN7r5OTIdIPplej5TuHwKBgQDMhZgmypFfaYWhSvqE71gI1/gZLJ9yaEyC\ngbJOVwjjByfPf7Oc/NABCvrdfYJlpp5XxsebKGtUxtR0Wio4vJZza3/wcCDVtP76\nxPIAWC3Kdvjv+SJiKAGY+keW6Ks/Z0RHGGzXKyhWEHCgE7w4VxLVhNE31kemwJWC\noeL2S/SJpQKBgEM38R7QE55YoOlR025OnbExiz0sTnkwOKj029V76iQngAEVZYXg\nxASbTPMZmHVwOXE5QjaUHV3GAsPaJ1lwBhixD8YM2SwrGuW5Dw7ZviPcxVBcmdeJ\n6KuhKbBWYWHSSrL8h1/CQBttna1eis7zvgagruMdY2qdVBXePdLvVuCnAoGALX8u\nmLqJWlNMEdRvJHFmARmiLF973OSM2J9nffvokzB9T7CV0T+AOisqIWmRP3GwWdBz\niPWV4tcUXgnMyLBTO7vXSzJ2a3QHINv9BcyX6ylKOYAPgQxrRo+uq0h5B/K+Ap7R\nX5BPOc4Qb9vUDCh6nRsdu7EkYVkIKXY/2hCNhq0CgYBhQRq0GvFjo+t5fRWGQSCd\nApTZQxveC3IxeSQt+kD9TiHhTWl2aG97BEXR8fBtK12Wp/gdSrcz2BbqDiZmrLkd\nZaLSXyogQa5V1NEyehB0Cg/2twBTs8LzYV8bdN5rG79qV9f4vc5uDhjlBFCCi9YN\nPg5PUibTUPWYUN2kZ005RQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "550216963766-compute@developer.gserviceaccount.com",
  "client_id": "108078516928444097726",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/550216963766-compute%40developer.gserviceaccount.com"
}

GOOGLE_CREDENTIALS = service_account._JWTAccessCredentials.from_json_keyfile_dict(
    CREDENTIALS
)
