name: Publish SEO Content

on:
  # Runs every day at 09:00 UTC. Edit the cron expression to change schedule.
  # Cron syntax: minute hour day month day-of-week
  schedule:
    - cron: "0 9 * * *"

  # Lets you trigger a run manually from the Actions tab in GitHub, useful
  # for testing without waiting for the schedule.
  workflow_dispatch: {}

jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run the agent pipeline
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GROQ_MODEL: ${{ vars.GROQ_MODEL }}
          WP_URL: ${{ secrets.WP_URL }}
          WP_USERNAME: ${{ secrets.WP_USERNAME }}
          WP_APP_PASSWORD: ${{ secrets.WP_APP_PASSWORD }}
          PUBLISH_STATUS: ${{ vars.PUBLISH_STATUS }}
          STORE_NICHE: ${{ vars.STORE_NICHE }}
        run: python crew.py

      # Uploads the full run transcript as a downloadable artifact, even
      # if the run was blocked by the Moderator, so you can review it from
      # the Actions tab without checking logs.
      - name: Upload run output
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-output
          path: output/last_run.txt
          retention-days: 14
