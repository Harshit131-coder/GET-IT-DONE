# Get it done

This repository contains the Django application source. Local databases and uploaded
media are intentionally excluded from Git.

## Configuration

Set the environment variables listed in `.env.example` before starting Django.
That file is a reference template; Django does not load it automatically.

- Set `DJANGO_SECRET_KEY` to a unique, random value. A temporary key is generated
  automatically only when `DJANGO_DEBUG` is enabled.
- Set `DJANGO_DEBUG=false` and provide `DJANGO_SECRET_KEY` outside local development.
- Configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` for PostgreSQL.
- Set `PAYPAL_RECEIVER_EMAIL` for payment processing.
