# Copy this file to .env and fill in your real values.
# .env is in .gitignore -- never commit real secrets.

# Groq API (free tier) - https://console.groq.com/keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=groq/llama-3.3-70b-versatile

# WordPress / WooCommerce site
WP_URL=https://yourstore.com
WP_USERNAME=your-wp-admin-username
# Create this under WP Admin > Users > Profile > Application Passwords
# Do NOT use your real login password here.
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# "draft" while you're testing, "publish" once you trust the pipeline
PUBLISH_STATUS=draft

# Free-text context to steer the Researcher agent's topic ideas
STORE_NICHE=wellness and natural supplements e-commerce store
