# separation_anxiety_tracker
Tracking training progress for my dog's separation anxiety, based on Julie Naismith's be right back method

To scrape data from the [app](https://berightbackapp.io/), login and use developer console to find the session cookie.
Put this in a secrets.yml file (follow the example [here](secrets_example.yml)

## Overall progress
See progress [here](https://max-sa-training.streamlit.app/)


TODO
- [X] Read raw data from google sheets
- [ ] Add in warmup support (figure out how to scrape from BRB app)
- [ ] DB hosting?
- [ ] Automated read of hosted DB (daily? cron from google sheets?)
- [ ] do not duplicate DB entries
- [ ] check for rating
- [X] Streamlit?
